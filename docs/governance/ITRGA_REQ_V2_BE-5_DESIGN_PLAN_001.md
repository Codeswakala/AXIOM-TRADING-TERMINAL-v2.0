# ITRGA-REQ-V2-BE-5-PLAN-001 — Request to the Development Authority: BE-5 Engineering/Design Plan

| Item | Value |
|---|---|
| From | ITRGA (succession ITRGA-REA-V2-SUCCESSION-001) |
| To | Development Authority (DA), via the Operator custody channel |
| Date | 2026-09-02 (Africa/Nairobi) |
| Authority | Operator authorization of Band BE-5, conveyed 2026-09-02 ("BE-5 authorized, you can now request the design plan from the DA"). OD number to be recorded by the Operator on the determination chain. |
| Roadmap basis | AXIOM-V2-BE-ROADMAP-001, Band BE-5 — Predictive ML, Signal, and Research Governance Expansion (`uploads/V2_BACKEND_ROADMAP.md`); delivery model §3 |
| Chain position | BE-0, BE-1, BE-2, BE-3 (P1, P2, transition), BE-4 all closed. BE-4 closed 2026-09-02 by ITRGA-DET-V2-0043-APPLY-001. Next migration chain number available: 0044. |
| Deliverable requested | ONE document: the DA engineering/design plan for Band BE-5 |
| Format exemplar | `docs/plans/V2_BE-4_DESIGN_PLAN.md` |

This request commissions the PLAN ONLY. It authorizes no code change, no migration authoring, no repository write, no commit, no database write, and no execution. Development/implementation begins only after ITRGA plan review, scope assessment, Build Order, and Operator decision, per the §3 delivery model.

## 1. Required content (the ITRGA plan-review acceptance checklist)

The DA design plan must cover Band BE-5 as one band, decomposed into implementation units as the DA determines, each separately implementable under a future Build Order.

**1.1 Band decomposition and unit structure**
- Units listed with sequence and dependencies; each unit single-responsibility.
- For every migration unit (chain numbering continues at 0044): exact DDL (tables, columns, types, constraints, indexes); immutability guard triggers with the exact refusal-message strings (R-2 pattern as established in 0040–0043); permission seeds with role alignment (SAL) and the expected global totals after each unit; data seeds with exact content; downgrade posture (documented no-downgrade or explicit downgrade per the established line); and the unit's **intended post-completion `alembic check` drift declaration** (the equivalent of the 0043 "9 inherited tokens + BE-4 set" declaration), stated per unit.
- For every non-migration unit: the artifact set and where each lands (service/contract/router/test/doc), with versioning.

**1.2 BE-5 contract scope (each item designed, not just named)**
- Model / feature / dataset registry evolution (tables or columns vs existing registries; versioning contract).
- Model **eligibility, calibration, freshness, economic-validation, and rollback** contracts — bound explicitly to `docs/governance/07_ML_SPEC.md` (cite the governing thresholds, sample requirements, rejection conditions, interpretation rules; report existence is necessary, never sufficient).
- Shadow / champion / challenger metadata contract.
- **Structural vs predictive signal contracts as separate, separately-typed families**; signal lineage, limitations, uncertainty; **withheld / expired / refused as permanent typed states** (not silent drops).
- Research reports, model diagnostics, and evidence-artifact model, with lineage and audit hooks per the BE-1 audit contract (mode, actor, correlation, append-oriented).

**1.3 Hard-boundary restatement (must appear in substance)**
- No execution authority from a signal; no live strategy authorization.
- No performance claim without correct data/mode/result classification.
- No model promotion by UI state or undocumented manual change.
- No broker, account, order, execution, or credential domain touched (BE-8..BE-10 territory).
- No external AI provider (BE-11 territory).
- RESEARCH mode only; read-only-by-default API surface for anything emitted; unknown/insufficient data is a typed outcome.
- Data honesty (§0.2 taxonomy): every artifact family tagged `synthetic · simulated · historical real · live · stale/cached · unavailable`; the plan must state what data classes BE-5 artifacts may legitimately contain at first landing and must NOT design fabricated research results.

**1.4 Mode, audit, and security integration**
- How new state carries mode and actor/correlation per the BE-1 contract.
- Audit events for eligibility, promotion, refusal, and rollback decisions (append-oriented).
- Secret/redaction law: this band prompts for NO credential. State that explicitly. Model metadata redaction rules for logs/artifacts.

**1.5 Test plan**
- Fail-first discipline per unit; budget of new tests per unit; the executed floor (789 passed as of BE-4 closure) must not decrease — state the projected new floor.
- Contract tests for every guard trigger/refusal (C-1/C-2/C-3 style); migration-up verification tests in the 0043 test pattern (upgrade to revision + schema/content assertions).
- Leakage/walk-forward/calibration/economic-validation evidence strategy consistent with the declared data classes (pipeline-validation vs research-validation tiers).

**1.6 Evidence plan for ITRGA review**
- The exact DB queries / API probes the DA will execute per unit (content-exact, like BE-4's compver pins — the ITRGA recomputes independently).
- The Delivery-Report-to-requirement mapping the DA will produce at closure.

**1.7 Register impacts**
- Capability maturity rows to change (`ML Research Expansion`, `Signal Architecture V2` — currently DESIGNED): target maturity per unit with evidence type.
- Technical-debt and risk-register additions anticipated; `V2_CURRENT_STATE.md` projection changes.

**1.8 Boundaries vs neighbours (explicit declarations)**
- What stays OUT of BE-5 and belongs to BE-6 (portfolio/risk research), BE-7 (backtesting/simulation/jobs), or the separate V1-era data-foundation track (B-01/B-02 corpus work) — and why. Signal truthfulness depends on honest data; declare any BE-5 item that cannot be honestly evidenced without the corpus track and state how it will be deferred or labelled.

**1.9 Package size/review volume**
- Expected evidence volume and the review-package composition, so the review loop can be planned.

## 2. Custody, channel, and discipline

- The plan is authored in the DA workspace; delivery to the ITRGA is via the Operator (no direct custody crossing; **no commits by the DA or the ITRGA — all commits strictly belong to the Operator**).
- All artifacts pass the credential scan law before entering the channel (no secrets, tokens, keys).
- The plan itself executes nothing — no SQL, no pytest, no migrations on the working DB. It is a document.

## 3. Next steps after submission

1. ITRGA plan review → scope assessment (analog of `ITRGA_ASSESSMENT_V2_BE-4_SCOPE_V1.md`), with any correction items.
2. Plan approval decision by the Operator, then Build Order issuance per unit.
3. Implementation, evidence, Delivery Report, ITRGA determination — per unit, gated.

— ITRGA, 2026-09-02
