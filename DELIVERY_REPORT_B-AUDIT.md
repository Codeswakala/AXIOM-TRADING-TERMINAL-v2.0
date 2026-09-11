# DELIVERY REPORT — BO-B-AUDIT
## Audit-Integrity Fix: Eliminate Silent Audit Loss Under Concurrency

| Item | Value |
|------|-------|
| Build Order | `BO-B-AUDIT` (Operator directive 2026-08-21: "proceed with the recommended fixes") |
| Predecessors | B-00 → B-07 · X-01 · F-00 (F-00 CLOSED — APPROVED WITH OBSERVATIONS, ITRGA 2026-08-21) |
| Implementer | Development Authority (DA) |
| Deliverable class | Backend hardening unit (chain position 31) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-B-AUDIT §2: B-AUDIT.1 reproduction, B-AUDIT.2 root cause,
B-AUDIT.3 fix (mechanism chosen + justified), B-AUDIT.4 verification — with the
§9 register-in-patch binding satisfied (see §7). §3 exclusions honored: no audit
content/schema change beyond the durability mechanism, no new runtime
dependency, no invariant weakening, no frontend changes, no repo publication.
§6 allowed files plus two disclosed additions (D1/D2 below — the §11 schema
mechanism's natural home).

## 2. What changed (files + SHAs + chain position)

Patch `b_audit.patch` — **chain position 31**, 5 files (4 modified + 1 new),
zero frontend files. Applies clean onto `34f4c62` + elements 1–30; post-apply
cmp 5/5; the register hunk additionally proven to apply onto a drifted
(baseline-era) register state. Patch sha256:
`6ade497ec07e9d06c063740d1a47fa03807fa5c4f1e6388ba7f5e3294b65d795`.

| File | Change |
|---|---|
| `backend/app/repositories/audit_repository.py` | The fix: decoupled verified audit writer (§5), one retry, durable failure marker, guarded marker path |
| `backend/app/db/models/audit.py` | `AuditWriteFailureRecord` model (D1 — the §11 schema mechanism's home) |
| `backend/app/db/models/__init__.py` | Marker model registration (D1) |
| `backend/tests/test_b_audit_concurrency.py` | **New** — 6 tests (repro contract, retry, marker, schema pin, no-500, decoupling) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows — **in the patch** as a pure-addition hunk (§7) |

## 3. Reproducing test (pre-fix evidence)

**Fail-first run: 6/6 failed against the pre-fix code** (`b_audit_prefix.log`).
The empirical reproduction (`scripts/b_audit_repro_investigation.py`, run log in
the evidence folder) drives the exact dev configuration — file SQLite +
StaticPool (one shared connection), two sessions — and reproduces the
production error **byte-identically**:

```
audit append failed category=SECURITY action=auth.ws_ticket_issued
err=(sqlite3.OperationalError) no such savepoint: sa_savepoint_1
[SQL: RELEASE SAVEPOINT sa_savepoint_1]
```

with both loss modes captured: the concurrent session **committing** mid-append
leaves `append=None` (the row surviving only as the other request's
side-effect), and the concurrent session **rolling back** mid-append loses the
row outright (`audit_rows=0`) — silent, endpoint still 200.

## 4. Root cause (the exact invalidation sequence)

1. **Engine:** `_engine_kwargs` gives every SQLite URL `poolclass=StaticPool` —
   all sessions share ONE DBAPI connection.
2. **Driver:** pysqlite's legacy transaction control silently suppresses a
   second session's `BEGIN` while a transaction is active — concurrent
   sessions' "transactions" MERGE into the one real transaction.
3. **Serialization:** the W3-U08.1 `sqlite_staticpool_serialization` lock
   covers only `:memory:` URLs — file-based dev SQLite runs unserialized
   (and `ws.py`/`live_service.py` use direct factory sessions bypassing the
   lock entirely).
4. **Audit layer (the failing point):** `AuditRepository.append` wrote inside
   `begin_nested()` on the business session → real `SAVEPOINT sa_savepoint_1`
   + INSERT, then `RELEASE` at context exit. A concurrent session's
   COMMIT/ROLLBACK landing between the INSERT and the RELEASE releases the
   savepoint out from under the append → `sqlite3.OperationalError: no such
   savepoint: sa_savepoint_1`.
5. **Swallow layer:** append caught the exception and returned `None` — the
   row loss was silent; the endpoint kept returning 200.

## 5. Fix mechanism + justification

**Chosen: decoupled verified writer (BO mechanism (b)) + one retry ((a)) +
durable failure marker ((c)).** Justification: with the merged-transaction
reality, ANY same-session mechanism retains an irreducible silent-loss window
(a concurrent rollback after the savepoint release, before the request's own
commit, loses the row with no error anywhere). Decoupling removes the audit
path's exposure to the business transaction lifecycle entirely:

- **Write:** short-lived dedicated session — `add → flush → commit →
  same-connection read-back verification`. The verification detects BOTH the
  orphaned-savepoint error AND the merged-rollback silent loss (where the
  commit "succeeds" as a no-op).
- **Retry:** one additional attempt on any failure or failed verification.
- **Durable marker:** persistent failure → `AuditWriteFailureRecord` row in the
  new `audit_write_failure_records` table (itself written through a verified
  dedicated session; the marker path is additionally guarded so even a
  marker-path bug can never 500 the endpoint; the structured error log remains
  the final fallback). Queryable at the DB level; no new API surface (out of
  the allowed-files list).
- **Consequence disclosed:** audit rows now commit independently of the
  business transaction. An audit row may persist for a business operation that
  later rolls back — acceptable for an accountability trail (security standard
  §5.7 records observed activity) — and it eliminates the pre-existing inverse
  loss (business rollback silently discarding the audit row).
- **Residual disclosed:** the shared-connection transaction MERGING for
  business writes remains (file-SQLite serialization + the `ws.py`/
  `live_service.py` direct-factory sessions are a future unit — outside this
  BO's allowed files). The audit path itself no longer depends on that class.

## 6. Durability + no-500 regression evidence

| BO criterion | Test | Result |
|---|---|---|
| Concurrent-rollback scenario: row lands or durable marker | `test_b_audit_concurrent_rollback_never_loses_row_or_is_silent` | **Pass** (row lands via retry+verify under the exact production interleaving) |
| Retry lands the row | `test_b_audit_append_retries_then_lands` | **Pass** (exactly 2 attempts, 1 row) |
| Persistent failure → durable marker | `test_b_audit_persistent_failure_writes_durable_marker` | **Pass** (marker with category/action/actor/resource ids/correlation id/failure_reason/attempts=2; audit_events 0 — nothing fabricated) |
| Marker queryable/schema-registered | `test_b_audit_failure_marker_model_registered_in_metadata` | **Pass** |
| Audit failure never 500s (incl. raising marker path) | `test_b_audit_append_failure_never_500s_endpoint` | **Pass** (login + ws-ticket both 200 under hard audit-storage failure) |
| Decoupled writer survives business rollback | `test_b_audit_decoupled_writer_survives_business_rollback` | **Pass** (intended semantic, pinned) |

Postfix run: **6/6 passed** (`b_audit_postfix.log`).

## 7. Register rows in patch (OBS-F00-3 corrective — confirmed)

The patch's register hunk is a **zero-context pure-addition hunk** (15 appended
lines; no `-` lines; no context): the rows for this unit (TD-B-AUDIT-UNIT,
TD-F00-UNIT-STATUS, OBS-F00-1-STATUS, OBS-F00-3-STATUS, OBS-F00-4,
TD-REGISTER-APPEND-ONLY-CONVENTION) ship inside the patch itself — not merely
described. Mechanism verified two ways in the transcript: exact-position
application onto the chain-30 register (cmp byte-identical) **and** application
onto the 34f4c62 baseline-era register (the drifted-state proof — git's offset
fallback appends the rows at EOF). The register is now append-only: historical
rows are never rewritten in patches, so no future register hunk can fail on a
drifted recipient. This begins the OBS-F00-3 repair; restoring a verifiable
remote chain remains an Operator-level custody decision.

## 8. Test evidence (executed)

- Workspace full backend suite: **552 passed** (546 floor + 6 new), 185.36s,
  exit 0 — `b_audit_fullsuite.log`.
- Clone-side (gold standard): pristine `34f4c62` → 31 elements → **552 passed**,
  163.60s, exit 0 — `b_audit_cloneside.log`.
- Fail-first prefix: 6/6 failed — `b_audit_prefix.log`; postfix 6/6 —
  `b_audit_postfix.log`.
- Ruff: clean on all changed files.

## 9. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `app/db/models/audit.py` + `app/db/models/__init__.py` touched — outside the §6 allowed-files list | Required by the §11 schema mechanism (the durable-marker table needs its model home + metadata registration; no alternative exists inside the allowed list). Disclosed and justified per §11. |
| D2 | Marker table schema addition (`audit_write_failure_records`) | Contemplated by §11 ("no schema migration unless the durable-failure-marker mechanism requires one — then disclosed and justified"). This is a metadata addition (dev schema via create_all), not an alembic migration; no existing row shape changed. |
| D3 | `db/session.py` NOT touched despite §6 allowing it | The dedicated writer uses the existing `get_session_factory` seam directly; no session.py change was needed. State the non-change for completeness. |
| D4 | Audit semantic shift (rows commit independently of the business transaction) | Disclosed in §5; pinned as intended behavior by a dedicated test. |
| D5 | Register hunk emitted as pure-addition (append-only) | The OBS-F00-3 corrective mechanism; historical register rows are never rewritten in patches from this unit onward (TD-REGISTER-APPEND-ONLY-CONVENTION row in the patch). |

## 10. Transmission manifest (relay-accurate, CA-TRANSMIT-1)

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/b_audit_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `b_audit_transmission/b_audit.patch.txt` | `6ade497ec07e9d06c063740d1a47fa03807fa5c4f1e6388ba7f5e3294b65d795` |
| 2 | `b_audit_transmission/b_audit_applycheck_transcript.txt` | `42452c535db455cfbce0812a0c8e263cbe5dc1157f2b3f513485e0b2031db38d` |
| 3 | `b_audit_transmission/b_audit_cloneside.log.txt` | `6e20478128e2e283e7269c931cbe080a77c2574e85fd1af5a8f88a0b568684cd` |
| 4 | `b_audit_transmission/b_audit_fullsuite.log.txt` | `b7796e8ef7b6e26e5a981735b99f3c8526920f695be25f5b730e8ae4368a6de0` |
| 5 | `b_audit_transmission/b_audit_postfix.log.txt` | `81c760fc3f07ad6675baf147038ed0214d42a2d3bab2d8399fbe16f0cf4c40dc` |
| 6 | `b_audit_transmission/b_audit_prefix.log.txt` | `4e6cfb25cc21e013b8d1c894e29fdc221a041a04ed8437041d0e0d51f1b848d4` |
| 7 | `b_audit_transmission/b_audit_repro_investigation.log.txt` | `047dd3a15ed24a582679d8be96320bae445861876e3565ee6b105369ba696a3e` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
