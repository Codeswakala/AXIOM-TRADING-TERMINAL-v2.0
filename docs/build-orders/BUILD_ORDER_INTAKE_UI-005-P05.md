# BUILD ORDER INTAKE — UI-005-P05

**Execution Research / SIMULATED Evidence Context**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P05.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-005-P04.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 46f/201t |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P05 |
| Mandatory carried observation | OBS-P04-1 timeout closure: harden `ResearchPerformanceAnalytics.test.tsx` timeout and supply clean gated full-suite run |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-005-P04 with observations and authorized UI-005-P05 as the next phase, carrying mandatory OBS-P04-1 closure.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-005-P04.md
docs/build-orders/BUILD_ORDER_UI-005-P05.md
```

P05 is limited to the existing `/execution-research` route and existing W6 SIMULATED execution research read APIs.

---

## 2. Accepted implementation scope

DA will enhance only the existing Execution Research surface:

```text
/execution-research
```

Implementation remains display-only over existing W6 read source:

```text
fetchExecutionResearchBundle
```

No new registered route will be added. No `/investigation-planning` route will be added.

---

## 3. R-4 SIMULATED spine acceptance

P05 must prove:

- SIMULATED label rendered across execution research evidence;
- no live/real relabeling;
- no venue action path;
- no broker/account/Gate path;
- assumptions, uncertainty, limitations, source ids, hashes, and policy details preserved from existing records;
- artifact/context links are registered-route navigation only;
- no persistence, saved view, backend/API/schema/migration/dependency, or registry change.

---

## 4. OBS-P04-1 closure acceptance

DA accepts the mandatory carried observation:

```text
ResearchPerformanceAnalytics.test.tsx > test_ui004_analytics_accessibility_and_brand_markers_hold
```

must receive an explicit `30000` ms test timeout, and P05 evidence must include a clean gated full-suite Vitest run with:

```text
FRONTEND_VITEST_EXIT_CODE: 0
```

A red gated run remains a finding and cannot be relabeled green.

---

## 5. Evidence obligations accepted

DA will produce:

```text
frontend/src/workstation/investigation/ExecutionResearchContext.test.tsx
DELIVERY_REPORT_UI-005-P05.md
docs/evidence/UI-005-P05_OPERATOR_EVIDENCE_COMMANDS.md
```

Mandatory named tests:

```text
test_ui005_execution_research_renders_existing_simulated_artifacts_only
test_ui005_execution_research_never_claims_live_execution_or_real_fills
test_ui005_execution_research_preserves_assumptions_uncertainty_limitations
test_ui005_execution_research_contains_no_broker_order_account_or_gate_path
test_ui005_execution_research_accessibility_and_brand_markers_hold
```

---

## 6. Non-authorizations

This intake does not authorize:

- UI-005-P06 completion checkpoint;
- plan/journal mutation;
- new backend/API/schema/migration/dependency work;
- new persistence key or table;
- new route or registry change;
- live/real execution path;
- Governance Gate opening;
- production deployment or certification.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
