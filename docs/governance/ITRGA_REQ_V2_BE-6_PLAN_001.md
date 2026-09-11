# ITRGA-REQ-V2-BE-6-PLAN-001 — Band BE-6 review contract (Design-Plan Request + REQ checklist)

| Item | Value |
|---|---|
| From | ITRGA |
| To | Development Authority (DA), via the Operator custody channel |
| Date | 2026-09-03 |
| Authority | Operator BE-6 authorization of 2026-09-03, recorded in `ITRGA-CN-V2-BE-6-001` |
| Roadmap basis | `AXIOM-V2-BE-ROADMAP-001`, Band **BE-6 — Portfolio and Risk Research Domain** (in-repo `uploads/V2_BACKEND_ROADMAP.md` §"Band BE-6", lines 254–280; verified verbatim against `AXIOM-V2-BE-6-DA-PLAN-001` §0 this session) |
| Sequencing note | The DA's plan arrived before this document (Operator-routed flow, disclosed honestly by the DA). This REQ now stands as the formal review contract: `AXIOM-V2-BE-6-DA-PLAN-001` v1.0.0 is reviewed against it, and the future Delivery Report requirement map owes an item-for-item answer to REQ §1.1–§1.11, Pins P-1…P-7, and the roadmap §0 contract. |

This contract authorizes nothing beyond planning. Implementation begins only under the issued Build Order (§3), per the delivery model.

## 1. REQ checklist (the review contract)

- **REQ-1.1 Decomposition and unit structure.** Units listed with dependencies; each migration unit single-purpose; chain continues at `20260903_0046`, `down_revision = "20260902_0045"`. Per migration unit: exact DDL (tables/columns/types/constraints/indexes); guard triggers with exact refusal-message strings; permission seeds SAL-aligned with projected global totals; data seeds (declared, "none" allowed); downgrade posture; post-unit drift declaration (the 9 inherited V1 tokens, zero band tokens) and pinned totals (triggers/permissions/compver before→after).
- **REQ-1.2 Hypothetical-only portfolio model.** Versioned-immutable definition (`record_seq` + `supersedes` C-1 vocabulary; currency = greatest `record_seq`; UNIQUE on (logical id, record_seq)). The band exclusion made structural: `basis` CHECK admits only `hypothetical`; allocations contract declared (shape, sum-to-1 tolerance, non-negative, scope limits disclosed).
- **REQ-1.3 Risk-metric contract.** Per metric: `method`, `method_citation`, `inputs`, `value`, `uncertainty`, `limitations`, `time_basis`, and typed `insufficient` (never a fabricated number). Pure deterministic functions only — no wall clock, no randomness, no sampling in v1 scope. Threshold/confidence constants cited from existing V1/V2 config where they exist, declared band-level otherwise; **no invented numbers presented as spec values**.
- **REQ-1.4 Scenario/stress contracts.** Declared deterministic shocks; mandatory limitation on shock realism; typed-empty allowed.
- **REQ-1.5 Immutable artifacts + determinism anchor (P-2).** UNIQUE anchor over (definition, inputs hash, engine-versions hash); same inputs+versions ⇒ existing artifact returned (idempotency); `as_of` rules (no-future, writer-enforced); `engine_versions`/`engine_versions_hash` on every artifact (P-4), compver seed with the C-2 instrument re-pin disclosure.
- **REQ-1.6 Hypothetical-vs-account separation made provable.** `basis_label` CHECK single-value `hypothetical-research` on every artifact; **zero** account/broker/order/position/live-P&L state, fields, or vocabulary (incl. the token "position" in schema/permissions); V1 simulated ledger read-only and labelled.
- **REQ-1.7 Data honesty.** Six-class taxonomy on both tables; first landing restricted to `synthetic`/`simulated`; `historical_real`/`live` refused with typed reasons (V2-TD-18 continuity); every evidence outcome declares its tier (pipeline-validation vs research-validation).
- **REQ-1.8 Mode/audit/security.** BE-1 columns on every row (mode, operator_id, correlation_id, created_at); audit events enumerated; lineage rows carrying `input_snapshot_id` (inputs hash), `computation_version` (engine-versions hash), `source_artifact_ids`; RBAC SAL-aligned with `denied` as a typed state; redaction gate untouched; the band prompts for no credential — stated.
- **REQ-1.9 Test plan.** Fail-first per unit; declared per-unit budgets and projected floor (856 base); migration-up content tests in the 0043 pattern; guard messages verbatim; CHECK-vocabulary probes (incl. the single-value `basis` refusing any real-class value); versioning/idempotency; six states; forbidden-token construction scans; socket/no-network guard; deterministic recomputation against the worked-sample annex fixtures.
- **REQ-1.10 Independent-recomputation evidence (roadmap exit-evidence item 1).** Worked-sample annex: one pinned portfolio + pinned synthetic input series + every metric's expected value to stated precision — sufficient for the ITRGA to recompute without executing the engine.
- **REQ-1.11 Boundaries and deferrals.** Explicit: no backtesting/jobs (BE-7); no real accounts/orders/positions/balances/live P&L (BE-8…BE-10, structurally impossible here); no external AI (BE-11); real-data risk inputs deferred to the corpus track; **report preview/export EXCLUDED** (the roadmap grants it "only where separately authorized" — ungranted); regression-based factor models and short/leveraged allocations deferred (debt rows).

## 2. Pins

P-1…P-5 carry unchanged from BO-V2-BE-5-001/0043 lineage (versioned-immutable lineage; determinism anchors on immutable artifacts; typed permanent outcomes + six-class honesty; computation provenance via compver/version pins; structural proof over vocabulary). BE-6 adds:

- **P-6 (hypothetical-only structural guarantee):** the hypothetical-vs-account separation exists in CHECK constraints, schemas, and responses — provable by probes, not claims.
- **P-7 (independent recomputation):** every reported metric's expected value appears in the worked-sample annex at stated precision; ITRGA recomputation must reproduce it.

## 3. Custody and next acts

Document-only channel; no commits by DA or ITRGA (all commits belong to the Operator); credential scan before every transmission. On a verified plan: ITRGA issues the Build Order under the existing authorization; implementation, evidence, Delivery Report, determination follow per unit, gated.

— ITRGA, 2026-09-03
