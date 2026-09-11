# ITRGA REVIEW — UI-005 ENGINEERING DESIGN PLAN

**Investigation & Planning Workspace**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-005 — Investigation & Planning Workspace** (NEW) |
| Document reviewed | `UI-005_ENGINEERING_DESIGN_PLAN.md` (484 lines) |
| ITRGA request | `docs/ITRGA_REQUEST_UI-005_DESIGN_PLAN.md` |
| Governing docs | Doc 12 §7, Doc 13, completed UI-001/UI-002/UI-003/UI-004 foundations, Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 43f/186t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7** |
| Authorizes | Issuance of `BUILD_ORDER_UI-005-P01` (on operator "authorized") — NOT implementation |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Plan header | `# UI-005 Engineering Design Plan — Investigation & Planning Workspace`; document type "pre-Build-Order; no implementation authorization" — OF the workstream |
| Plan length | 484 lines — substantive |
| References ITRGA request + correct predecessor + baseline | Yes (`ITRGA_REQUEST_UI-005_DESIGN_PLAN.md`, UI-004 COMPLETE, v0.62.0/0037/414/43f·186t) |
| Delivery report | `DELIVERY_REPORT_UI-005_DESIGN_PLAN.md` (170 lines) — "not self-approved; no implementation started" |

**Pack confirmed OF the UI-005 Design Plan.** No stale/wrong-doc pack.

---

## 2. Assessment against ITRGA request §3 brightest lines

| Brightest line | Plan coverage | Verdict |
|---|---|---|
| **B-1 Gate CLOSED / no actuation** | §2 B-1 pre-registers an EXPANDED forbidden-token grep — adds `position/balance/margin/capital/allocation/real_pnl` beyond my list; Trade Planning = research-note only; Execution Research = SIMULATED/display-only | ✅ Met (exceeds request) |
| **B-2 No recompute/inference/re-derivation/AI** | §2 B-2 enumerates: no infer/recompute/generate-scenarios/derive-economic/client-side-engine/AI-LLM-summary/reclassify/action-recommendation | ✅ Met |
| **B-3 Verbatim posture** | §2 B-3 inherits UI-004 §2.2 verbatim rule verbatim (research_only/not_assessed/warning:*/SIMULATED never upgraded) | ✅ Met |
| **B-4 No-cherry-picking** | §2 B-4: scope/sample/assumptions/uncertainty/limitations/source-ids/hashes visible; filtered ≠ full-scope truth | ✅ Met |
| **B-5 Read-only reuse / no new authorship** | §2 B-5 + §5 data-source table: all surfaces map to existing read APIs/stores, "New backend? No" for every row | ✅ Met |

All five constitutional brightest lines are pre-registered and testable. The plan correctly self-identifies UI-005 as **higher-sensitivity** than UI-004 and hardens the no-actuation line accordingly.

---

## 3. Assessment against ITRGA request §4 questions

| Q | Plan answer | ITRGA finding |
|---|---|---|
| 1 Route/registry | §3: enhance existing `/investigate` (+ `/compare-scenarios` `/trade-plans` `/execution-research` `/journal` `/portfolio-research`); **no new route**; any future registry change needs ITRGA pre-approval + 14-field contract unchanged | ✅ Accepted (R-1) |
| 2 Persistence | §4: **no new table** default; optional `operator_workspace_preferences` key `investigation-planning-workspace-v1` (ids/vis/filter only); persistence-capture control acknowledged (save→psql ≥1 row, no forbidden fields, operator_id→operators.id, alembic head) | ✅ Accepted (R-2) |
| 3 Trade Planning / Journal mutation | §4.3: existing W5 authorized create/update may remain; UI-005 does not expand; any touching phase must prove research-note fields only, no order/account/broker/execution/P&L, no plan-to-execution path, existing APIs only | ✅ Accepted (R-3) |
| 4 Execution Research boundary | §1 + §10 P05: SIMULATED/display-only; no live execution/fill/order/broker/account/Gate | ✅ Accepted (R-4) |
| 5 Phase split | §10: P01 frame/inventory/guardrail → P02 investigation lineage → P03 scenario+portfolio → P04 trade-planning+journal → P05 execution-research SIMULATED → P06 completion | ✅ Accepted with a precision note (R-5) |
| 6 Investigation lineage as disclosure | §1 + §10 P02: lineage/validation/related-reports via UI-004 viewer/drilldown patterns, no recompute | ✅ Accepted (R-6) |
| 7 UI-002-P04b independence | §12 Q6 defers to ITRGA | ✅ Accepted (R-7) |

---

## 4. Binding refinements (R-1…R-7) — conditions on every UI-005 phase

- **R-1 — Route/registry no-drift.** Enhance existing routes; **no new registered route/workspace without ITRGA pre-approval.** Each phase proves: registry 14-field contract unchanged, `/investigate` etc. only, no `/investigation-planning` new route, no duplicate navigation.
- **R-2 — No-new-table default; persistence-capture binds if implemented.** Saved view state only via `operator_workspace_preferences` key `investigation-planning-workspace-v1`, ids/visibility/filter only. **If any phase persists, that phase MUST supply the inline raw psql save→SELECT ≥1 populated row on the CORRECT table, no forbidden fields, `operator_id→operators.id` JOIN, `alembic current`=head. API/in-process read-back NEVER substitutes; `(0 rows)`=disproof.** Default expectation: P01–P03 and P05 do NOT persist.
- **R-3 — Trade Planning & Journal mutation boundary (HARD).** UI-005 must NOT expand W5 plan/journal mutation. Any phase touching them (P04) proves: research-note/reflection fields only; **no order/account/broker/position/P&L/execution field; no plan-to-execution path; no broker/account journal import;** existing APIs only; no new endpoint/table. A forbidden-field-rejection named test is required (the plan already anchors `test_ui005_planning_preserves_research_only_fields_and_forbidden_field_rejection`).
- **R-4 — Execution Research stays SIMULATED / display-only.** No live execution/real fill/real order/broker/account/Gate path. "SIMULATED" label rendered and never relabeled live/real (named test `execution_research_never_claims_live_execution_or_real_fills`).
- **R-5 — Phase-split precision.** Accepted as: **P03 = Scenario Comparison + Portfolio Research** (both read-only/hypothetical); **P05 = Execution Research (SIMULATED) only.** (The §13 rationale text mentioned "execution research and portfolio context together" — that is superseded; portfolio belongs to P03 per §10. Confirm this mapping in the P01 Build-Order intake.) ITRGA reserves the right to require P04 to be split into separate Trade-Planning and Journal phases if the mutation-boundary evidence is not crisp (Q4).
- **R-6 — No-recompute SPINE (every phase).** Grep clean for `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` on UI-005 source + external-AI grep (`openai|gpt|external_llm|llm_summary|ai_summary`) + verbatim-render + no-cherry-picking tests where analytics/comparison/report surfaces are touched. Investigation lineage = disclosure of stored fields, never recompute.
- **R-7 — Level-I + Doc-16 + regression.** Every phase: build-identity FIRST; named tests DISPLAYED passing; whole-surface no-actuation grep; no-drift substitute (head `20260717_0037` + manifests unchanged + no-endpoint + no registry change unless R-1-approved); full frontend suite ≥ baseline **43f/186t no test lost** + backend ≥414; **Doc-16 brand B-1…B-7 (never color alone; material violation ⇒ Corrective per Part XIV)**; served browser evidence; networked CI exit 0 + sentinel (or waive TD-W6-CI-AUDIT env-flake via ask_user). **Carried TD-UI-POSTCSS-HIGH:** does not gate presentation-only work, but any dependency-touching phase must address it, and it must be remediated/accepted before Production Readiness Certification.

---

## 5. Observations (non-blocking)

- **OBS-DP-1** — §13 rationale text bundles "execution research and portfolio context together," which conflicts with §10 (portfolio in P03, execution research alone in P05). Resolved by **R-5**; confirm the mapping at P01 intake.
- **OBS-DP-2** — Q4 (split P04 into Trade Planning vs Journal) is left to ITRGA. Default: keep P04 combined, BUT if the mutation-boundary evidence (R-3) is not crisp at P04 delivery, ITRGA will require a split (this is a standing conditional, not a plan defect).
- **OBS-DP-3** — Q6 (UI-002-P04b search adapters): remain **independent/non-blocking**; not folded into UI-005 unless a separate Build Order authorizes it (R-7 carries this).

---

## 6. Disposition

**UI-005 Design Plan is APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7.** On operator "authorized", ITRGA will issue **`BUILD_ORDER_UI-005-P01` — Investigation & Planning Workspace Frame, Data-Source Inventory, and No-Actuation Guardrail** (per the DA's recommended first Build Order and §10 P01), carrying R-1…R-7 and the 5 P01 named-test anchors.

No implementation is authorized by this review. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
