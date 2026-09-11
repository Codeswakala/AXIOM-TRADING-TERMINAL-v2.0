# BUILD ORDER — AXIOM V2 BAND BE-5: PREDICTIVE ML, SIGNAL, AND RESEARCH GOVERNANCE EXPANSION (IMPLEMENTATION)

| Field | Value |
|---|---|
| Build Order ID | `BO-V2-BE-5-001` |
| Date | 2026-09-02 |
| Authority | Operator authorization of Band BE-5 (2026-09-02; OD number recorded by the Operator on the determination chain) · Operator approval of the plan review and explicit Build-Order issuance authorization ("the BUILD order is authorized for issuance", 2026-09-02) |
| Governing instruments | `AXIOM-V2-BE-5-DA-PLAN-001` v1.0.0 (DA design plan) · `ITRGA-PRV-V2-BE-5-PLAN-001` (ITRGA plan review; **Review Pins P-1…P-5 are MANDATORY amendments embedded below**) · `ITRGA-REQ-V2-BE-5-PLAN-001` · `AXIOM-V2-BE-ROADMAP-001` Band BE-5 · `docs/governance/07_ML_SPEC.md` (binding spec: Statistical Validation, Economic Validation, Model Registry, Drift Monitoring, Continuous Learning, Deployment Policy, Research Integrity) |
| Executing authority | Development Authority (DA) — implementation in the DA workspace only |
| Review authority | ITRGA (full-depth review standard per the Operator's standing instruction: defects issued as corrections; anything contrary to the roadmap or overall design is ruled out until sufficient corrected plan/delivery evidence is presented; closure by determination, no self-approval) |
| Baseline | working DB head `20260831_0043` in force (ITRGA-DET-V2-0043-APPLY-001) · 789 executed tests (0 fail) · 18 v2 triggers · `v2_permission` 27 · compver 3 · drift = exactly 9 inherited V1 tokens · RESEARCH/SIMULATION only |
| Status | **ISSUED — DA implementation authorized. Nothing in this order touches the working database: application of 0044/0045 to it is a separate future sanctioned act in the BO-V2-0043-APPLY-001 pattern.** |

## 1. Scope

Implement Band BE-5 exactly as the DA design plan `AXIOM-V2-BE-5-DA-PLAN-001`, **as amended by ITRGA Review Pins P-1…P-5** (§2 pins the resulting exact expectations; the plan text and this order read together; this order prevails on any point of difference).

Units and delivery packaging (as reviewed):
- **PG-1** — U-1 (migration `20260902_0044_v2_be5_ml_governance.py`) + U-2 (decision-contract engine); `ml_governance_engine = mge-1.0.0` compver seed co-delivered (P-4).
- **PG-2** — U-3 (migration `20260902_0045_v2_be5_signal_contracts.py`) + U-4 (signal writer + read API); `signal_engine = sge-1.0.0` compver seed co-delivered (P-4).
- **PG-3** — U-5 (diagnostics services + read projections over the P-2 table) + U-6 (evidence, Delivery Report, register sync).

One Delivery Report may cover all units, or one per package — evidence discipline identical (delivery choice per plan Part 12).

## 2. Terminal state (acceptance contract — every item pinned)

| # | Item | Pinned expectation |
|---|---|---|
| T-1 | Migration chain | `20260902_0044_v2_be5_ml_governance.py` (`down_revision = '20260831_0043'`) → `20260902_0045_v2_be5_signal_contracts.py` (`down_revision = '20260902_0044'`). Literal-revision upgrades only, never `head`. Models registered in `app/db/models/__init__.py` in the SAME unit (PG-002 law). |
| T-2 | 0044 tables (exact, P-1/P-2/P-3 applied) | `v2_ml_governance_record`: plan columns **plus** `record_seq INTEGER NOT NULL`, `superseded_by String(36) NULL`, `model_type String(64) NOT NULL`, `instrument_class String(64) NOT NULL`; `UNIQUE(model_artifact_id, record_seq)` replacing `UNIQUE(model_artifact_id)`; NO `updated_at_event_id`; current state = greatest `record_seq` (P-1, P-3). `v2_ml_lifecycle_event` as planned (append-only). `v2_ml_diagnostic_report`: full 0043 report-table pattern — content-hash determinism anchor, `engine_versions` + `engine_versions_hash`, input refs, mode/actor/correlation/`created_at` (P-2). All CHECK vocabularies as plan (deployment_class `research|shadow|champion|challenger|retired`; data_class 6-value taxonomy). |
| T-3 | v2 triggers after 0044 | **24** = 18 + 6 new with exact names/messages: `v2_ml_governance_record_immutable_update/_delete` → `V2 ML governance records are immutable; UPDATE prohibited` / `…DELETE prohibited` · `v2_ml_lifecycle_event_immutable_update/_delete` → `V2 ML lifecycle events are immutable; UPDATE prohibited` / `…DELETE prohibited` · `v2_ml_diagnostic_report_immutable_update/_delete` → `V2 ML diagnostic reports are immutable; UPDATE prohibited` / `…DELETE prohibited` |
| T-4 | `v2_permission` rows after 0044 | **34** = 27 + 7 additive, SAL-aligned: admin `v2.research.ml_governance.read` (SAL-2), `v2.research.ml_governance.decide` (SAL-3), `v2.research.signal.read` (SAL-2), `v2.research.ml_diagnostics.read` (SAL-2); operator `v2.research.ml_governance.read`, `v2.research.signal.read`, `v2.research.ml_diagnostics.read`. No role+permission duplicates. |
| T-5 | compver after 0044 | **4** rows: `ml_governance_engine = mge-1.0.0` hash pinned from the implementation transcript of the co-delivered U-2 engine (P-4; ITRGA recomputes). |
| T-6 | 0045 tables/triggers/permissions | Tables `v2_signal_record` (family CHECK exactly `structural|predictive`; state CHECK exactly `emitted|withheld|expired|refused`; conditional contracts per plan) and `v2_signal_state_event`. Triggers after 0045: **28** = 24 + 4 with exact messages: `V2 signal records are immutable; UPDATE prohibited` / `…DELETE prohibited` · `V2 signal state events are immutable; UPDATE prohibited` / `…DELETE prohibited`. `v2_permission` after 0045: **35** (+ admin `v2.research.signal.emit`, SAL-3). compver **5** (+ `signal_engine = sge-1.0.0`, P-4). |
| T-7 | Decision contracts (U-2) | Each contract (eligibility/calibration/freshness/economic/statistical/rollback) is a pure decision function over V1 evaluator outputs with spec citations in `decision_basis`; ≥1 passing and ≥1 typed-refusal test per contract; `economic_status` independent of `statistical_status`; full promotion ladder enforced (all statuses passing AND SAL-3 AND RESEARCH mode; every other path = permanent `refused` event); rollback REFUSED unless `rollback_target_version` set and resolvable; at most one `champion` per (`model_type`,`instrument_class`) on the current projection — writer + dedicated test (P-3). |
| T-8 | Signal writer + API (U-4) | Predictive signal without an eligible current governance record → permanent `refused` typed record; `withheld`/`expired`/`refused` permanent typed states (no silent drops, no row mutation — state events); `payload` NULL when withheld/refused; `uncertainty` mandatory for `predictive`; lineage refs mandatory (structural → BE-4 observation ids; predictive → governance record + V1 model/dataset/feature versions); `historical_real`/`live` data classes REFUSED with typed reason at first landing; read-only endpoints under `/v2/research-governance` including typed `denied` responses; no-network/socket guard in tests. |
| T-9 | Integrity posture (DA test-chain databases) | `integrity_check` ok · journal delete · no `-wal`/`-shm`; the working DB untouched by this order. |
| T-10 | Drift | At the 0044 head and at the 0045 head: `alembic check` reports exactly the 9 inherited V1 tokens (no `v2_*` / `ix_v2_*` token); direct-run output in evidence. |
| T-11 | Regression and floor | BE-3 provider state and BE-4 state (report tables, compver rows, permission rows) byte-identical across 0044/0045 in the DA test chains (no-touch group); full suite executed green with count **≥ 853** (789 + ≥64 new tests, itemized); the executed floor 789 never decreases; no position-based test assertions (PGF-012). |
| T-12 | Mode/audit/credential law | Every new row carries mode/actor/correlation; append-oriented audit events for register/evaluate/promote/demote/refuse/rollback/emit/withhold/expire decisions and sensitive reads; redaction gate and `V2_FORBIDDEN_PERMISSION_MARKERS` intact; **no credential of any kind appears anywhere in the band** (explicit evidence line per the plan's Part 7 declaration). |

## 3. Constraints

- Fail-first per unit (each unit's first commit is its failing contract tests; the commit order is stated in the Delivery Report).
- Symmetric downgrades (drop only what the unit creates: 0044 drops 3 tables/6 triggers/7 permission rows/1 compver row; 0045 drops 2 tables/4 triggers/1 permission row/1 compver row).
- No fabricated state: no data seeds beyond the registrar/permission/computation-version rows pinned above; no demo models; no synthetic "performance" rows; every metric-bearing artifact carries data_class + mode + validation tier.
- Threshold constants (calibration bound, freshness bound) pinned at implementation FROM the V1 service configs, with the citation recorded in `decision_basis` — no invented numbers in the Delivery Report or code comments presented as spec values.
- Custody: implementation in the DA workspace only; **no commits and no pushes by the DA or the ITRGA — all commits strictly belong to the Operator**; delivery of all artifacts through the Operator custody channel; every artifact credential-scanned before channel entry.
- This order authorizes NO repository write on the delivery repo, NO working-database application of 0044/0045 (separate future sanctioned act), and NO state change outside the DA implementation workspace and its test-chain databases.

## 4. Evidence requirements (Delivery Report package)

- REM-001 literal transcript of every changed/added file with SHA-256 manifest (the exact BE-4 OBS-1 set: engine modules, model classes, `app/v2/api/router.py` mount line, `app/v2/rbac/permissions.py` seeds, `app/db/models/__init__.py` registrations, both migrations, all tests).
- RSR-1 executed Level-I transcripts: migration-up runs (0043 test pattern: upgrade to literal revision + schema/seed/trigger/CHECK content assertions); guard-refusal probes with byte-exact messages; API probes incl. denied responses.
- RSR-2 full-suite `-v` output with itemized delta vs 789 and the executed count.
- Drift direct runs at both heads (T-10).
- Content-exact DB probes the ITRGA can recompute independently (trigger enumeration, permission rows with SAL, compver rows with source hashes).
- DR requirement-mapping table: `ITRGA-REQ-V2-BE-5-PLAN-001` §1.1–§1.9 + pins P-1…P-5 + this order's T-1…T-12, item for item.
- Credential-scan result line; law declaration restated.

## 5. Explicitly out of scope (do-not-touch)

Corpus/data-foundation track (B-01/B-02) · BE-6 portfolio/risk · BE-7 backtesting/jobs · broker/account/order/execution domains (BE-8…BE-10) · external AI (BE-11) · FE serving · working-DB application of 0044/0045 · any commit/push on the delivery repository.

## 6. Closure rule

Band BE-5 closes only on an ITRGA determination after the Delivery Report: evidence verified item-for-item against T-1…T-12 and the requirement map; report existence is necessary, never sufficient (07_ML_SPEC discipline). Any working-DB application follows the full sanctioned-act pattern (plan → scope assessment → packs → battery → issuance → execution → determination), separately authorized.

— Issued by the ITRGA under Operator authorization, 2026-09-02. We don't guess. We prove.
