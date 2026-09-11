# ITRGA DETERMINATION — BE-3 P2 STATUS TRANSITION · APPLY ACT · FINAL (001)

Determination ID: `ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001`
Date: 2026-08-31
Authority: `BO-V2-BE-3-P2-TRANS-001` §6; OD-005 (`AXIOM-V2-OD-BE-3-P2-005`); `ITRGA-DET-V2-BE-3-P2-TRANS-FINAL-001` (mechanism proven on the gate evidence database)
Evidence:
- Apply record: `operator-evidence/BE-3-P2-transition/BE-3-P2-TRANS-APPLY-RUN-V5.txt` (attempt V5, 2026-08-31 14:09:15 +03:00 — migration applied ONCE; verdict FAIL at B7 on PGF-012, an ITRGA check defect)
- Verify record: `operator-evidence/BE-3-P2-transition/BE-3-P2-TRANS-VERIFY-RUN-V1.txt` (run 1 of the verify act, 2026-08-31 14:40:05 +03:00 — **VERIFY VERDICT: PASS**)
- Assessments/plans: `ITRGA-ASS-V2-BE-3-P2-TRANS-APPLY-RUN-V5` (D1–D7; PGF-012 closed §9); `ITRGA-PLAN-V2-BE-3-P2-TRANS-VERIFY-001`; `ITRGA-PLAN-V2-BE-3-P2-TRANS-APPLY-002` (§9–§11)

## 1. Determination

**As of 2026-08-31 14:40:05 +03:00, the end state of `BO-V2-BE-3-P2-TRANS-001` §6 is IN FORCE on the application's working SQLite database, fully evidenced (Level I, on the machine):**

`v2_md_provider` (provider `twelvedata`):

| Column | Value | Evidence |
|---|---|---|
| `source_status` | `contract_tested` | verify B4 (exact) |
| `entitlement_status` | `verified` | verify B4 (exact) |
| `persistence_permitted` | `false` (SQLite rendering `0`) | verify B4 (exact) |

- **Status history:** exactly 2 rows, each **byte-exact** by content-based comparison (PGF-012-corrected; middle dot compared in Python via `chr(183)` and byte-verified `\xc2\xb7` in the transcript): genesis `NULL → architecture_candidate` (`BO-V2-BE-3-P1-001`; evidence `AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0 / ITRGA-DET-V2-BE-3-PLAN-001`) and transition `architecture_candidate → contract_tested` (authority `BO-V2-BE-3-P2-TRANS-001`; evidence `ITRGA-DET-V2-BE-3-P2-FINAL-001 · run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83`).
- **Audit:** exactly the `provider.status_transition.start` and `provider.status_transition.complete` rows, byte-exact details (verify B6: `PASS:audit_rows_exact`).
- **Immutability guards:** intact — 5/5 spot-checks refused with the exact SQLite guard messages (provider UPDATE/DELETE; history UPDATE/DELETE); the four guard triggers present (verify B1/B7). The machine's v2 trigger count is 12 — the four guards plus the BE-1/BE-2 triggers created by the accepted 0038/0039 migrations (recorded, Level I; no assertion required).
- **Authority:** `AXIOM_TD_TRANSITION_AUTHORITY_REF` inactive (UNSET; lifecycle closed: UNSET → SET to the exact BO string for the single apply → UNSET).
- **Revision:** `alembic current` = `20260829_0042 (head)`.
- **Drift:** `alembic check` at head = **exactly** the 9-token inherited V1 drift set (added `audit_write_failure_records` + 2 indexes; removed 6 indexes); **zero** V2/P2/transition tokens (now Level I on the real database — the unknown the apply act's plan carried).
- **File state:** `backend\axiom_dev.db` — 1,310,720 bytes; last write **2026-08-31 14:09:55 +03:00** (during the apply act — nothing has written to the file since); sha256 `0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006` (identical at verify B1 and act end — the verify act changed nothing); `journal_mode=delete`; no sidecars; `integrity_check=ok`; SQLite 3.50.4.
- **Recovery anchor:** `axiom_dev.db.pre-0042-20260831140931.bak` — **proven to be the very file the apply act created**: its sha256 `6db478ee7464a004d1188fa242ce40e2d397abb75ea027792063e74fb8620895` matches the apply record exactly (both records); valid SQLite, integrity ok. It holds the pre-modification baseline (`20260717_0037`) and is the credential-free rollback anchor.

## 2. Basis (evidence chain)

1. **Applied once.** The apply record shows `Running upgrade 20260825_0041 -> 20260829_0042` with the head confirmed; 0042's in-migration invariants (accepted source: P-1…P-8 gates, guard drop → UPDATE + one history append → guard recreate, `_verify_guard_present`, `_verify_transition_consistent`, atomic start/complete audit) mean any failure would have left the database at `20260825_0041`. It did not.
2. **The apply's B7 FAIL was an ITRGA check defect, not a state defect** (PGF-012: position-based history check over a uuid4 TEXT primary key; dry-run fidelity gap). The verify act — read-only, PGF-012-corrected — closed all six evidence gaps the FAIL left open, and passed.
3. **Provenance re-anchored in both acts** (migration on disk = `af77a63f…`, the accepted Revision-2 value).
4. **Baseline fact (recorded, no correction required):** the working database was at `20260717_0037` before the act (within the plan's tolerance); the act's B4 chain applied the real 0038–0041 migrations, creating the V2 table set on the working database.
5. **Dialect posture (unchanged, per record):** the gate evidence databases (PostgreSQL) remain in their proven/reversal-proven states as the record of the mechanism; the working database (SQLite, per the DA workspace's dialect posture) is now the in-force state.
6. **Credential law held throughout:** no credential of any kind was read, set, or used by any act; every operator capture is scanned CLEAN; the Four Secrets remain untouched; no provider network call occurred.

## 3. Programme state

- **Provider ladder:** `contract_tested` — **in force** on the working database (history 2, persistence false, guards intact, authority inactive, head 0042).
- **`integrated` and beyond:** a new, separately governed chain (its own build order, its own Operator decision, its own ITRGA review; the transition authority string is BO-specific and was consumed by this act).
- **`persistence_permitted` remains `false`:** enabling persistence is a separate, later-governed act.
- **Backend band:** the BE-3 P2 status-transition act is **complete and closed**. **BE-4 (Market Context, Chart Intelligence, Research Read Models) remains gated on a new Operator directive** — none is on record.
- **Frontend:** remains blocked per the sequencing directive; the unblock decision is the Operator's.
- **Git/GitHub:** deferred clean custody — no repository source change was made by any act of this chain (OD-005 item 4 respected throughout).

## 4. Findings register (transition chain, ITRGA-owned) — ALL CLOSED

| Finding | Subject | Closure (dated) |
|---|---|---|
| PGF-007 | Target dialect assumed (PG) without verification | RUN-V1 assessment, 2026-08-29 |
| PGF-008 | Quoted input not normalized at 0B | RUN-V2 assessment §8, 2026-08-29 |
| PGF-009 | Compound braced expansion (PS 5.1 literal-variable class) | RUN-V3 assessment, 2026-08-29 |
| PGF-010 | `version()` vs `sqlite_version()` | Dry-run record `ITRGA-DRYRUN-V2-BE-3-P2-TRANS-APPLY-PACK-V4-V5` §3, 2026-08-29 (caught before operator impact) |
| PGF-011 | Issuance lacked a byte-identity self-check | RUN-V4 assessment §9, 2026-08-31 |
| PGF-012 | Position-based history check over a uuid4 PK; dry-run fidelity gap | RUN-V5 assessment §9, 2026-08-31 |

All LOW. Every abort in the chain occurred at a fail-fast gate before side effects — with the single exception of the apply itself, which is now proven and fully verified. Plain-ownership record: five consecutive instrument defects (PGF-008…012) were ITRGA's; the verification discipline (deterministic audit → AST parse → full dry run → MD5 self-check on the machine) was built up in response and is now standing practice.

## 5. Residuals (Operator's discretion; no ITRGA action required)

- **Backup anchor retention/disposal** — the Operator's discretion under this record; retention is recommended until the transition act is formally accepted.
- **Inherited V1 drift (9 tokens)** — outside this act's scope; reconciling the working database with the V1 model, if desired, is a separately governed change (new Operator decision).
- **Next programme step (BE-4; FE unblock)** — the Operator's decisions; BE-4 requires a new Operator directive before ITRGA issues any plan or instrument.

— ITRGA, 2026-08-31
