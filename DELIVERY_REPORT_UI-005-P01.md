# DELIVERY REPORT — UI-005-P01

## Investigation & Planning Workspace Frame · Data-Source Inventory · No-Actuation Guardrail

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P01** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P01.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 43f/186t |
| DA status | Implemented; evidence package prepared; not self-approved |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for:

```text
UI-005-P01 — Investigation & Planning Workspace Frame · Data-Source Inventory · No-Actuation Guardrail
```

It is governed by:

```text
docs/build-orders/ITRGA_REVIEW_UI-005_DESIGN_PLAN.md
docs/build-orders/BUILD_ORDER_UI-005-P01.md
docs/plans/UI-005_ENGINEERING_DESIGN_PLAN.md
```

Binding refinements applied:

- **R-1:** enhanced existing `/investigate`; no new registered route;
- **R-2:** P01 persists nothing;
- **R-3:** no Trade Planning / Journal mutation expansion;
- **R-4:** Execution Research shown as SIMULATED / display-only in inventory;
- **R-5:** phase mapping confirmed — P03 = Scenario + Portfolio; P05 = Execution Research only;
- **R-6:** no recompute/no inference/no external AI guardrail;
- **R-7:** Level-I evidence and Doc 16 brand gate.

DA does not self-approve UI-005-P01.

---

## 2. Implementation summary

UI-005-P01 establishes the Investigation & Planning workspace frame inside the existing `/investigate` workspace and proves every UI-005 surface maps to an existing governed source.

Implemented:

1. `InvestigationPlanningFrame` inside `SignalInvestigationPage.tsx`;
2. UI-005 governed data-source inventory covering:
   - Signal Investigation;
   - Scenario Comparison;
   - Trade Planning;
   - Execution Research;
   - Research Journal;
   - Portfolio Research;
3. visible guardrail:
   ```text
   Gate CLOSED · Research-only · Existing routes · SIMULATED evidence only
   ```
4. responsive/brand-consistent CSS using existing tokens;
5. five UI-005-P01 named tests.

No registry route was added. `/investigate` remains the primary UI-005 workflow hub.

---

## 3. Files added

```text
docs/build-orders/ITRGA_REVIEW_UI-005_DESIGN_PLAN.md
docs/build-orders/BUILD_ORDER_UI-005-P01.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-005-P01.md
frontend/src/workstation/investigation/InvestigationPlanningFrame.test.tsx
docs/evidence/UI-005-P01_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-005-P01.md
```

---

## 4. Files modified

```text
frontend/src/pages/SignalInvestigationPage.tsx
frontend/src/pages/SignalInvestigationPage.test.tsx
frontend/src/styles/global.css
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

No backend source, API contract, schema, migration, package manifest, persistence, or workspace registry change was made.

---

## 5. Data-source inventory

The P01 UI inventory maps surfaces to existing governed sources:

| Surface | Existing route | Existing store | Existing read seam | P01 posture |
|---|---|---|---|---|
| Signal Investigation | `/investigate` | W3 advisory signal records and linked report ids | `fetchAdvisorySignals` + `fetchInstitutionalIntelligenceBundle` | Read-only rationale, guardrails, lineage, related reports |
| Scenario Comparison | `/compare-scenarios` | W4 stored hypothetical scenario reports | `fetchScenarioReports` / `fetchScenarioReport` | Existing hypothetical comparisons with assumptions and limitations |
| Trade Planning | `/trade-plans` | W5 trade plan research notes | existing trade plan read path | Research-note planning context only; mutation scope unchanged |
| Execution Research | `/execution-research` | W6 SIMULATED execution research artifacts | `fetchExecutionResearchBundle` | SIMULATED display-only evidence with assumptions and limitations |
| Research Journal | `/journal` | W5 manual research journal entries | `fetchJournalEntries` | Research documentation links and reflections |
| Portfolio Research | `/portfolio-research` | W7 hypothetical portfolio research dashboard/report preview | `fetchPortfolioResearchDashboard` + `fetchAdvancedResearchReport` | Hypothetical review context; no real portfolio state |

No new endpoint, table, store, or route was introduced.

---

## 6. R-5 phase mapping clarification

UI-005-P01 intake confirms the binding phase mapping required by ITRGA:

```text
P03 = Scenario Comparison + Portfolio Research
P05 = Execution Research (SIMULATED) only
```

This supersedes the stray wording in the design plan rationale and closes `OBS-DP-1` for P01 intake.

---

## 7. No-recompute / no external AI proof

Production source grep against `SignalInvestigationPage.tsx` showed no matches for:

```text
inferSignal
runInference
authoritativeRecompute
emitSignal
generateSignal
recompute
recalculat
deriveConfidence
reclassif
summariz.*(ai|llm|gpt)
new .*Engine
/api/v1/orders
openai
gpt
external_llm
llm_summary
ai_summary
```

Result:

```text
NO_RECOMPUTE_EXTERNAL_AI_GREP_CLEAN
```

---

## 8. Expanded no-actuation proof

Production source grep against `SignalInvestigationPage.tsx` showed no matches for:

```text
buy
sell
place_order
execute
go-live
connect-broker
broker
account_id
order_ticket
position
balance
margin
capital
allocation
real_pnl
open_gate
allow_execution
```

Result:

```text
NO_ACTUATION_GREP_CLEAN
```

No execution/order/broker/account/Gate path was introduced.

---

## 9. No-drift substitute

DA local no-drift facts:

```text
No backend source change
No API/schema/migration change
No package manifest change
No workspace registry change
No persistence implemented
No new endpoint/provider/table markers
Alembic temp smoke: 20260717_0037 (head)
```

Registry remains existing routes only:

```text
/investigate
/compare-scenarios
/trade-plans
/execution-research
/journal
/portfolio-research
```

No `/investigation-planning` route was added.

---

## 10. Named UI-005-P01 tests

Added:

```text
frontend/src/workstation/investigation/InvestigationPlanningFrame.test.tsx
```

Required named tests:

```text
test_ui005_workspace_mounts_inside_single_ui001_shell
test_ui005_workspace_uses_existing_routes_and_registry_only
test_ui005_workspace_maps_every_surface_to_existing_sources
test_ui005_workspace_contains_no_actuation_or_gate_path
test_ui005_workspace_preserves_research_only_and_doc16_branding
```

DA local result:

```text
1 file passed / 5 tests passed
```

---

## 11. Local DA validation

### 11.1 Frontend

Commands:

```bash
cd frontend
npm audit --audit-level=high
npm test -- --reporter=verbose
npx tsc -b --pretty false
npm run build
```

Results:

```text
Frontend full suite: 44 files / 191 tests passed
TypeScript: clean
Production build: successful
```

Build output:

```text
CSS: 46.54 kB
JS: 532.12 kB
```

Baseline comparison from UI-004 completion:

```text
Frontend tests: 43 files / 186 tests → 44 files / 191 tests
Bundle: CSS 45.92 kB / JS 529.02 kB → CSS 46.54 kB / JS 532.12 kB
Delta: +1 test file / +5 tests; +0.62 kB CSS / +3.10 kB JS
```

### 11.2 Frontend audit finding

DA local `npm audit --audit-level=high` remains non-green due the standing high-severity transitive advisory:

```text
postcss <=8.5.17
Severity: high
GHSA-r28c-9q8g-f849
```

It also disclosed the existing moderate `react-router` / `react-router-dom` advisories.

No dependency remediation was performed because UI-005-P01 does not authorize dependency changes. Operator evidence must not relabel this audit output as green. This remains the carried `TD-UI-POSTCSS-HIGH` residual requiring separately authorized remediation or formal acceptance before Production Readiness Certification.

### 11.3 Backend

Commands:

```bash
cd backend
ruff check .
pytest -q
```

Results:

```text
Ruff: All checks passed!
Backend full suite: 414 passed, 1 warning
```

### 11.4 Alembic

Temp SQLite Alembic smoke:

```text
alembic current: 20260717_0037 (head)
```

Operator target must still provide target `alembic current` evidence.

---

## 12. Doc 16 brand self-check

| Doc 16 check | DA self-check |
|---|---|
| B-1 Logo / monogram | Existing UI-001 shell AX monogram and AXIOM identity unchanged. |
| B-2 Constitutional palette | New styling uses existing CSS tokens only. No hardcoded colors in UI-005 production TSX. |
| B-3 Typography + monospace numerics | Existing route ids and read seams use `.mono`. |
| B-4 Unified iconography | No new icon set introduced. |
| B-5 Institutional-not-retail | Copy emphasizes investigation, research-only planning, existing routes, SIMULATED evidence, and no browser-authored analytical result. |
| B-6 Accessibility | Semantic section, ARIA labels, role note, readable cards, responsive layout. |
| B-7 Documentation branding | Delivery/evidence/build-order records use AXIOM governance format. |

Browser proof remains mandatory for ITRGA review.

---

## 13. Operator evidence package

Prepared:

```text
docs/evidence/UI-005-P01_OPERATOR_EVIDENCE_COMMANDS.md
```

The command pack covers:

- build identity;
- five named tests displayed passing;
- data-source inventory proof;
- no-recompute/no-external-AI grep;
- expanded no-actuation grep;
- no-drift substitute and no registry change;
- R-5 mapping confirmation;
- Doc 16 brand/accessibility proof;
- frontend/backend regression;
- browser served-session evidence;
- networked local CI.

---

## 14. DA disposition

DA submits UI-005-P01 for operator evidence collection and ITRGA review.

DA does not self-approve UI-005-P01.

UI-005-P02 is not authorized until ITRGA approves or approves-with-observations P01 and explicitly authorizes the next Build Order.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of DELIVERY_REPORT_UI-005-P01.md**
