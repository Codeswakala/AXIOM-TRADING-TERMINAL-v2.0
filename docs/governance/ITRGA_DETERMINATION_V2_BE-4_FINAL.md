# ITRGA DETERMINATION — AXIOM V2 BE-4 BAND CLOSURE: MARKET CONTEXT, CHART INTELLIGENCE, RESEARCH READ MODELS (FINAL)

Determination ID: `ITRGA-DET-V2-BE-4-FINAL-001`
Date: 2026-09-02
Authority: `AXIOM-V2-OD-BE-4-006` (chain start) · `AXIOM-V2-OD-BE-4-007` (SD-1 = A, SD-2 = A) · `AXIOM-V2-OD-BE-4-008` (Build Order authorization; R-1…R-5 binding) · `BO-V2-BE-4-001` · `AXIOM-V2-BE-ROADMAP-001` (Band BE-4, exit evidence) · role per `AXIOM_ITRGA_MASTER_ONBOARDING` §1/§35/§37 (review authority; closed-determination vocabulary; no self-authorization — this determination is the review act itself; it creates no new authority and authorizes no repository change)

Evidence corpus (all archived byte-identical in the ITRGA workspace; credential scan CLEAN on every item):

| Item | ID / record | md5 | Level |
|---|---|---|---|
| Design plan | `AXIOM-V2-BE-4-DA-PLAN-001` v1.0.0 (`docs/plans/V2_BE-4_DESIGN_PLAN.md`) | `856460a3b782bbcf14b3bea0bd3eb394` | III (approved as input) |
| Delivery report | `AXIOM-V2-BE-4-DR-001` (`docs/evidence/BE-4/DELIVERY_REPORT_V2_BE-4.md`) | `6d1fe7d99ff65f67ff082e4cc49520bf` | III (verified against annexes) |
| Source transcript | `AXIOM-V2-BE-4-TRANSCRIPT-001` (15-file manifest; 0043 section) | `e8b22ca0ee4f8070053dbcf5065a1fd4` | II |
| Resubmission cover | `docs/evidence/BE-4/V2_BE-4_RESUBMISSION_COVER.md` | `e0fb087408ebd82b621f13b6ba65f2c6` | III |
| API transcript | `docs/evidence/BE-4/V2_BE-4_API_TRANSCRIPT.txt` (CG-1 closure) | `85f9ad33a1ccfe7f0924891f066ca749` | **I** (executed endpoint evidence) |
| Test-run transcript | `docs/evidence/BE-4/V2_BE-4_TESTRUN_TRANSCRIPT.txt` (CG-2 closure) | `110d9475f97f35679ee22c14a60eab20` | II |
| Plan review | `ITRGA-REV-V2-BE-4-PLAN-001` (APPROVED WITH OBSERVATIONS; R-1…R-5 binding) | — | review record |
| Delivery review | `ITRGA-REV-V2-BE-4-DELIVERY-001` — **CLOSED — FINAL: APPROVED (2026-09-01; §10)** | — | review record |
| Verify run 1 (V1 pack, PASS) | `BE-3-P2-TRANS-VERIFY-RUN-V1.txt`, 2026-08-31 14:40:05 +03:00 | `a3b9dbdc30a312cb9159d550b92a3895` | **I** (operator machine) |
| Verify run 2 (V1 pack, FAIL at B2) | `BE-3-P2-TRANS-VERIFY-RUN-V2.txt`, 2026-09-01 17:42:35 +03:00 | `60aefc52ebdb51dfed2790f195529531` | **I** |
| Verify run 3 (V2 pack, FAIL at B9) | `BE-3-P2-TRANS-VERIFY-RUN-V3.txt`, 2026-09-01 18:20:38 +03:00 | `11cd29574dd2677485f39e6ad9f89ccd` | **I** |
| Verify run 4 (superseded V2 pack re-executed, FAIL at B9) | `BE-3-P2-TRANS-VERIFY-RUN-V4.txt`, 2026-09-01 19:34:28 +03:00 | `44efa32f82d4000a4d997ce6b6d743cd` | **I** |
| **Verify run 5 (V3 pack, PASS)** | `BE-3-P2-TRANS-VERIFY-RUN-V5.txt`, 2026-09-02 10:14:47 +03:00 | `7a6954686f6e4e559da53789f15e53aa` | **I** — closing evidence |
| V3 dry-run battery (5-case matrix) | `DRY-RUN-V8-VERIFY-PACK-V3.txt` | `d750512c998205bf97af75a269060c43` | II |
| Apply record + recovery anchor | `BE-3-P2-TRANS-APPLY-RUN-V5.txt`; anchor sha256 `6db478ee7464a004d1188fa242ce40e2d397abb75ea027792063e74fb8620895` | — | **I** |

## 1. Determination

**As of verify run 5 — 2026-09-02 10:14:47 +03:00, `VERIFY VERDICT: PASS` on the V3 instrument (`52c24352883f4291633950df08cd36a6`) — the BE-4 band is CLOSED.**

**DETERMINATION: APPROVED WITH OBSERVATIONS.**

1. The BE-4 delivery is **APPROVED**: the delivery review is closed FINAL: APPROVED (2026-09-01); completeness gap CG-1 closed at Level I (executed API transcript) and CG-2 closed at Level II (executed test output, 789-test reconciliation); all Build Order requirements D-1…D-7 are evidenced as satisfied; binding refinements R-1…R-5 satisfied; guardrails BG-1…BG-12 pass.
2. Stage 8 step 2 (the verify re-run of the in-force working-DB end state) is **CLOSED**: verify run 5 (V3 pack) PASS — B1–B9 all pass; the in-force state of the applied transition end state was re-proven end-to-end on the Operator machine, including byte-level no-touch of the working database.
3. The qualifier **WITH OBSERVATIONS** attaches to exactly one open item: the OBS-9 Operator accounting (the nature and source of the 2026-09-01 17:26 +03:00 repository bulk-write operation). The band's exit evidence is proven in full regardless; the accounting, when provided, closes OBS-9 administratively (it is a record-completeness item, not an exit-evidence item). All other observations are recorded/closed in §6.
4. ITRGA-owned finding PGF-014 (two defects in verify pack V2) is **CLOSED** on this determination — both closure criteria met in verify run 5 (see §5).
5. No repository changes are authorized by this determination. No new Operator decision is consumed by it. The next programme step (any of the §7 acts) requires a new Operator decision.

## 2. Exit-evidence assessment (roadmap Band BE-4 — per BO-V2-BE-4-001 §8, SD-2 = A treatment)

| Roadmap exit-evidence item | Status | Evidence |
|---|---|---|
| Deterministic/reproducibility tests | **SATISFIED** | D-5 group 1 executed within the 789-test run (Level II, CG-2); R-1 idempotency proven at Level I (repeat `POST /market-context/compute` → `reused_existing: true`; `GET /reports` total 1; determinism anchor) |
| Temporal-integrity tests | **SATISFIED** | D-5 group 2 executed within the 789-test run; `as_of`/`created_at` contract enforced in tests and visible in the Level I API transcript |
| Lineage: output → source snapshot + computation version | **SATISFIED** | D-5 group 3 executed + Level I: `input_snapshot_id`, `input_content_hash`, `engine_versions`, `engine_versions_hash` on `v2_market_context_report`; `engine_versions_hash` `1e0bad5cb13f9a86bc7ff513c2d46fda4d0abe3818fba0623a9717c3d0c50c42`; R-5 one-line provenance citations |
| Direct **API** evidence of facts vs interpretation | **SATISFIED** (Level I, CG-1) | Final path `/api/v1/v2/market-context/*`; claim distribution `{'fact': 9, 'derived_observation': 6, 'contextual_interpretation': 1}`; predictions 0; six BE-1 states executed; R-4 rule-table outcomes observed |
| Direct **browser** evidence | **RECORDED RESIDUAL by Operator decision** | OD-007, SD-2 = A: API-level closure; browser evidence to be verified at the FE band / X-01 joint gate (§7 item 1) |
| Guardrails BG-1…BG-12 · R-1…R-5 · no-touch · full suite green | **SATISFIED** | Review FINAL: APPROVED; verify run 5 PASS (no-touch: working DB byte-identical, sha256-verified); 789 passed / 0 failed / 0 error |

## 3. Working database — in-force state (proven on the Operator machine, verify run 5)

`C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db` — **unchanged by the BE-4 band; verified no-touch at the byte level across verify runs 1, 3, 4 and 5:**

| Property | Value (run 5, Level I) |
|---|---|
| Size | 1,310,720 B |
| Last write | 2026-08-31 14:09:55 +03:00 (the apply act; unchanged) |
| SHA-256 | `0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006` (byte-identical to the apply-act in-force value) |
| Integrity / journal / sidecars | `integrity_check` ok · journal_mode `delete` · no `-wal`/`-shm` |
| Engine | SQLite 3.50.4 |
| v2 triggers | 12 (the four transition guard triggers + BE-3 P2 set; the six 0043 guard triggers are **absent** — 0043 not applied, consistent with 12 vs the expected 18 post-0043) |
| Current revision | `20260829_0042` (repository head `20260831_0043` recorded, not applied) |
| Provider row | `twelvedata`: `contract_tested` / `verified` / `persistence_permitted = 0` |
| History | exactly 2 rows, content-exact (genesis + transition; middle-dot evidence ref compared via chr(183)) |
| Audit | exactly `provider.status_transition.start` + `provider.status_transition.complete`, details exact |
| Immutability | 5/5 spot-checks refused with the exact guard messages |
| Authority variable | `AXIOM_TD_TRANSITION_AUTHORITY_REF` UNSET (verified) |
| Drift | existence asserted in run 5 (non-zero exit + "not up to date"); the itemized 9-token inherited V1 set (`audit_write_failure_records`, `ix_audit_write_failures_category_action`, `ix_audit_write_failures_created`, `ix_advisory_signals_expires_at`, `ix_advisory_signals_freshness_status`, `ix_ingestion_runs_symbol_started`, `ix_model_artifacts_advisory_status`, `ix_model_artifacts_artifact_hash`, `ix_model_artifacts_experiment_id`) stands as **directly observed in verify run 1 on this byte-identical file**; plus the expected BE-4 schema set (three 0043 tables) given the repository head |
| Environment (recorded) | alembic **1.19.0** (SECTION 3B, run 5) |

Recovery anchor (apply act backup): `axiom_dev.db.pre-0042-20260831140931.bak`, 1,085,440 B, sha256 `6db478ee…`, integrity ok — present and valid (B3, run 5).

## 4. Repository state record (proven by SECTION 3B of runs 3–5; recorded, not asserted)

1. Alembic head: `20260831_0043`; the 0043 migration file is **in the Operator repository, hash-verified** (`ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b` = the approved BE-4 manifest value), and **not applied** to the working database (12 vs 18 triggers + byte-identity + `alembic current` = 0042).
2. **Bulk-write event (OBS-9 mechanics):** all 43 files in `backend\alembic\versions` carry last-write 2026-09-01 17:26:38–41 +03:00 (a 3-second window; a single bulk write — copy/restore/checkout — recorded identically in runs 3, 4 and 5; no further writes since).
3. Git: HEAD frozen at the BE-1-era commit (only `20260823_0038_v2_be1_core.py` tracked; migrations 0039–0043 and all BE-2/BE-3/BE-4 code, tests, plans, governance documents and packs uncommitted) — consistent with Git custody deferred.
4. Venv: the venv's alembic version changed as part of the same event (itemized → summary `alembic check` format; exact version now recorded: **1.19.0**).
5. Migration-file hash cross-check (ITRGA recomputation, Level II): **0042 VERIFIED** (`af77a63f…`, approved) · **0043 VERIFIED** (`ab905762…`, approved) · **0040 VERIFIED** (`1332ebf5…` = pin in `ITRGA-DET-V2-BE-3-P1-FINAL-001`) · **0038, 0039, 0041 NOT VERIFIED** (no per-file pin in the ITRGA corpus — recorded gap; **carried as a precondition of the 0043 application act**: re-pin before application).
6. **OBS-9 accounting (OUTSTANDING):** what the 2026-09-01 17:26 +03:00 bulk-write operation was, and from where — the Operator's one-line statement. Working-DB impact is proven nil regardless (byte-identical in every run since).

## 5. Findings register (ITRGA-owned, V2 chain)

| ID | Severity | Status | Disposition |
|---|---|---|---|
| PGF-001…PGF-012 | LOW | CLOSED | BE-3 P2 transition chain instruments; closed in the chain records (see `BO-V2-BE-3-P2-TRANS-001` dated notes and `ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001` §4) |
| PGF-013 | LOW | CLOSED (2026-08-31) | Non-canonical vocabulary in `ITRGA-REQ-V2-BE-4-001`; corrected on issue |
| **PGF-014 (defect a)** | LOW | **CLOSED (2026-09-02, this determination)** | V2 B9 token-presence assertions were format-dependent on the alembic output format; the venv's alembic (1.19.0) prints the summary format. Closure evidence: verify run 5 B9 PASS via the V3 format-independent branch on the real summary-format environment (non-zero exit + "not up to date" asserted; itemized set stands from run 1 on the byte-identical file; PGF-014 NOTE line present in the transcript) |
| **PGF-014 (defect b)** | LOW | **CLOSED (2026-09-02, this determination)** | V2 SECTION 0 self-identification read "V1" (supersession residue). Closure evidence: verify run 5 SECTION 0 reads `Pack: ITRGA-V2-BE-3-P2-TRANS-VERIFY-PACK-V3` |

Supersession chain of the verify instrument (record): V1 (`00ffe783…`) → V2 (`753fe704…`, superseded by V3) → **V3 (`52c24352883f4291633950df08cd36a6`), instrument of record for the closing run.** No instrument was silently edited; each supersession is dated and recorded in `BO-V2-BE-4-001` §15–§18.

## 6. Observations register (BE-4 band)

| ID | Observation | Status |
|---|---|---|
| OBS-1 | BO allowed-files precision: 2 extra additive V2 modifications (`app/v2/rbac/permissions.py`, `app/db/models/__init__.py`) — additive, reviewed, approved | Recorded — closed |
| OBS-2 | Test-fixture credential placeholders confined to test databases — classified CLEAN (established classification) | Recorded — closed |
| OBS-3 | Read-only `git status`/`git diff --stat` in DA evidence — custody-compliant | Recorded — closed |
| OBS-4 | 0043 PostgreSQL deployment-dialect branch (guard triggers) — recorded for the PG target | Recorded — closed |
| OBS-5 | 0042 test-chain authority variable — test databases only | Recorded — closed |
| OBS-6 | API `/versions` output shows 1 of 3 components — recorded | Recorded — closed |
| OBS-7 | 2 test warnings (1 starlette deprecation, 1 pre-existing V1 asyncio-mark) — recorded | Recorded — closed |
| OBS-8 | Re-submission runs generated 2026-09-01 ~11:00 UTC — recorded | Recorded — closed |
| **OBS-9** | Repository bulk-write event 2026-09-01 17:26:38–41 +03:00 (all 43 migration files); git HEAD frozen at BE-1 era; venv alembic → 1.19.0 (now recorded); working DB unaffected (byte-identical); 0042/0043/0040 hash-verified, 0038/0039/0041 NOT VERIFIED (corpus gap, carried to the 0043 act) | **OPEN — mechanics proven; the Operator's one-line accounting (operation + source) outstanding** |

## 7. Residuals and later-governed acts (each requires a NEW Operator decision)

| # | Act / residual | Status | Gate |
|---|---|---|---|
| 1 | Browser evidence of facts vs interpretation (SD-2 = A) | Recorded residual | FE band / X-01 joint gate |
| 2 | Real-data research validation (SD-1 = A) | Recorded residual | Separate later-governed act |
| 3 | **0043 working-DB application act** — the 0043 file is already in the Operator repository (hash-verified); the act needs **no file-copy step** but must **re-pin 0038/0039/0041 first**; new OD + sanctioned pack (MD5 self-check) + file-level backup anchor + verify act (BE-3 P2 transition pattern) | Not authorized | New OD |
| 4 | Inherited V1 drift reconciliation (the 9-token set) | Recorded | New OD |
| 5 | Backup anchor retention/disposal (`axiom_dev.db.pre-0042-…bak`) | Operator's discretion; retention recommended pending item 3 | Operator decision |
| 6 | Band BE-5 (Predictive ML, Signal, Research Governance Expansion) | Roadmap next | New OD |
| 7 | FE band unblock | Sequenced | New OD |
| 8 | `integrated` provider-status ladder step | Separate chain | New OD |
| 9 | Git custody (deferred since BE-1 era) | Deferred | Operator decision |

## 8. Programme state (post BE-4 closure)

- **Test baseline going forward: 789** (552 V1 + 198 V2 pre-BE-4 + 39 BE-4; executed 789 passed / 0 failed / 0 error, Python 3.13.14, pytest 8.4.2).
- **Drift baseline:** exactly the 9 inherited V1 tokens (directly observed in run 1 on the byte-identical working DB file) + the expected BE-4 schema set (repository head 0043, not applied).
- **Working database:** in force at revision `20260829_0042`, byte-identity proven (`0483f9fe…`), 12 v2 triggers, guard set intact, authority UNSET.
- **Bands closed:** BE-0, BE-1, BE-2, BE-3 (P1, P2, transition apply act), **BE-4 (this determination)**. Next on the roadmap: BE-5 (requires a new OD).
- **V2 capability maturity registry:** BE-4 rows updated at closure (Market Context Engine, Chart Intelligence → Complete).
- **Credential law:** every artifact in this determination's corpus scanned before archiving — CLEAN. The Four Secrets remain unshared and unrecorded.
- DA claims of `V2_CURRENT_STATE.md` v19.0.0 and register synchronization remain Level III (DA workspace; not independently verifiable by ITRGA — custody independence).

## 9. Discipline statement

We don't guess. We prove.

Every assertion in this determination is tied to a named, archived, md5-identified record with an evidence level assigned (Level I: operator-machine runtime/DB/file/repo evidence, runs 1–5; Level II: executed tests, migrations, dry runs, and ITRGA recomputations from submitted artifacts; Level III: documents and claims, held as such). Missing evidence is stated as NOT PROVEN, never assumed. ITRGA's own instrument defects (PGF-014) were owned in full, corrected by dated supersession, and closed only on Operator-machine evidence. No step of this determination was self-authorized; the band was closed on the authority chain OD-006 → OD-007 → OD-008. Nothing in this document authorizes a repository change, a Git operation, or a database write.

— ITRGA (Independent Technical Review & Governance Authority), 2026-09-02
