# ITRGA DETERMINATION — BO-B-AUDIT
## Audit-Integrity Fix: Eliminate Silent Audit Loss Under Concurrency

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-AUDIT.txt` |
| Build Order | `BO-B-AUDIT` (Operator-authorized 2026-08-21) |
| Predecessors | B-00 → B-07 · X-01 · F-00 (F-00 CLOSED — APPROVED WITH OBSERVATIONS) |
| Date | 2026-08-21 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced in my custody)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED** — all 7 declared artifacts present, all 7 hashes match |
| Patch `b_audit.patch.txt` sha256 | `6ade497e…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) — and it applied onto my *drifted* register state, proving the register-in-patch corrective works |
| Patch composition | 5 files (4 modified + 1 new), zero frontend |
| **Register-in-patch (OBS-F00-3 corrective)** | **CONFIRMED** — the register hunk is a pure-addition append (new rows, no edits to historical rows), shipped inside the patch itself, and it applied cleanly onto my drifted register. This is the exact mechanism I demanded. |
| Root cause evidence | **Reproduced byte-identically** — `sqlite3.OperationalError: no such savepoint: sa_savepoint_1` under the exact two-session/StaticPool interleaving; both loss modes (concurrent commit → `append=None`, concurrent rollback → `audit_rows=0`) captured |
| Fix mechanism | **Real** — decoupled `_write_and_verify` (dedicated short-lived session + same-connection read-back), one retry, durable `AuditWriteFailureRecord` marker with its own verified write path |
| New tests (6) | **6/6 passed** (incl. concurrent-rollback-never-loses, retry-then-land, durable-marker, no-500, decoupled-survives-rollback) |
| **Full backend suite** | **552 passed** — matches report (552) |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 requirement | Status |
|-------------------|--------|
| Concurrency test reproduces "no such savepoint" pre-fix | ✓ byte-identical repro + 6/6 fail-first |
| Root cause stated with evidence | ✓ five-step invalidation sequence, evidenced (StaticPool shared connection → pysqlite merge → unserialized file-sqlite → savepoint orphaned → swallow) |
| Fix applied; mechanism chosen + justified | ✓ decoupled writer + retry + marker, with the irreducible-silent-loss-window argument |
| Post-fix: row lands or durable marker under the same scenario | ✓ test-pinned |
| Audit failure never 500s the endpoint | ✓ regression test-pinned (incl. raising marker path) |
| Register rows in the patch | ✓ pure-addition hunk, verified in my custody |
| Full suite green | ✓ 552 passed |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **The bug was real and is now genuinely fixed.** The reproduction captured the exact production error and both silent-loss modes; the fix eliminates the audit path's exposure to the business-transaction lifecycle entirely. The read-back verification is the key insight — it detects the *silent* merged-transaction loss (where the commit "succeeds" as a no-op), which a naive retry would miss.

2. **The endpoint-safety invariant held.** The one thing I insisted must not regress — "audit failure must never 500 the endpoint" — is pinned by a dedicated test covering even the marker-path-failure case.

3. **The register drift is now repaired at the mechanism level.** The append-only register convention (register ships in every patch as pure-addition) means no future register hunk can fail on a drifted recipient. This is the structural fix for OBS-F00-3 that I asked for, and I verified it directly (the patch applied onto my drifted register).

4. **The one semantic change is disclosed and acceptable.** Audit rows now commit independently of the business transaction — an audit row may persist for an operation that later rolls back. This is the *correct* behavior for an accountability trail (security standard §5.7 records observed activity) and it also eliminates the pre-existing inverse loss. The DA disclosed it and pinned it as intended.

## 4. Deviations — reviewed and accepted

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `db/models/audit.py` + `__init__.py` outside §6 list | Accepted — the §11 schema mechanism requires them; disclosed + justified |
| D2 | Marker table schema addition (create_all, not alembic) | Accepted — contemplated by §11; no existing row shape changed |
| D3 | `db/session.py` NOT touched | Accepted — the dedicated writer used the existing factory seam |
| D4 | Audit semantic shift (independent commit) | Accepted — disclosed, pinned, correct for accountability |
| D5 | Register hunk pure-addition | Accepted — the OBS-F00-3 corrective mechanism |

## 5. Residual (recorded, non-blocking)

The **business-write** transaction-merging for file-based SQLite (and the `ws.py`/`live_service.py` direct-factory sessions) remains — correctly out of this unit's scope. The audit path no longer depends on that class, but a future hardening unit should serialize file-sqlite business writes the way the test harness already does. Noted, not blocking.

## 6. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; byte-identical repro; root cause evidenced; decoupled-verified-writer fix proven; register-in-patch corrective verified in my custody; 6/6 new + 552/552 full suite |
| Observations | Residual file-sqlite business-write serialization (future unit); the two carried observations (RR moderates, remote custody decision) remain at Operator level |
| Next authorization state | **BO-B-AUDIT CLOSED** — the register-in-patch convention is now standing. Remaining before F-01: the **Operator-level remote-custody decision** (OBS-F00-3's second half). F-01 may proceed in parallel once that decision is recorded. |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-B-AUDIT |

## 7. Record

- Patch: `6ade497ec07e9d06c063740d1a47fa03807fa5c4f1e6388ba7f5e3294b65d795`
- 6/6 new tests · 552/552 full suite · register-in-patch verified
- Root cause + fix: silent audit loss eliminated, endpoint-safety preserved

> **We don't guess. We prove.** The audit backbone is now durable: rows land or leave a queryable marker, never vanish silently, and the endpoint still never 500s. And the register-in-patch convention — verified working against my own drifted clone — has begun the OBS-F00-3 repair exactly as required. Approved.

**End of ITRGA Determination BO-B-AUDIT**
