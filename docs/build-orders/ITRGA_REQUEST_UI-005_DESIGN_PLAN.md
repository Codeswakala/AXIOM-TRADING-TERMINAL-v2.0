# ITRGA REQUEST — UI-005 ENGINEERING DESIGN PLAN

**New workstream: UI-005 — Investigation & Planning Workspace. Design Plan requested BEFORE any Build Order.**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-005 — Investigation & Planning Workspace** (NEW) |
| Governing docs | Doc 12 §7 (`12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md`, line 2282), `13_UI_TRANSFORMATION_MASTER_PLAN.md`, completed UI-001/UI-002/UI-003/UI-004 foundations, `16_BRAND_GOVERNANCE_STANDARD.md` |
| Predecessor milestones | 🏛️ UI-001 COMPLETE · 🏛️ UI-002 COMPLETE · 🏛️ UI-003 COMPLETE · 🏛️ UI-004 COMPLETE |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **43f/186t** |
| Action required of DA | **Produce `UI-005_ENGINEERING_DESIGN_PLAN.md`** — DA does NOT implement until ITRGA reviews the plan and issues the first Build Order |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Why a Design Plan first

UI-005 is a **new workstream**, not a phase of an approved one. Per the standing ITRGA workflow rule, ITRGA requests the Design Plan from the DA first, reviews it (Approved / Approved-with-Observations + numbered refinements), and only then issues the first Build Order. **No implementation is authorized by this request.**

---

## 2. Doc 12 §7 scope (verbatim intent)

**Objective:** Integrate analytical investigation with planning workflows.
**Scope surfaces (all already exist as pages — this is presentation/navigation/integration, NOT new capability):**
- Signal Investigation (`SignalInvestigationPage`)
- Scenario Comparison (`ScenarioComparisonPage`)
- Trade Planning (`TradePlanningPage`)
- Execution Research (`ExecutionResearchPage` — SIMULATED execution research, display-only)
- Research Journal (`ManualJournalPage`)
- Portfolio Research (`PortfolioResearchPage`)

**Expected outcome:** Operators move naturally from investigation to planning while preserving analytical context — **advisory and research-oriented only** (Doc 12 §"Plan": "Planning shall remain advisory and research-oriented").

---

## 3. Constitutional brightest lines the plan MUST pre-register (non-negotiable)

This is a **higher-sensitivity domain** than UI-004: it names "Trade Planning" and "Execution Research." The plan must make the following bright lines explicit and testable:

- **B-1 Gate CLOSED / no actuation anywhere.** "Trade Planning" and "Execution Research" are **research notes and SIMULATED research artifacts only** — no order ticket, no broker/account/position/balance/margin field, no live/real data, no go-live/open-gate/execute path. Execution Research remains **SIMULATED, display-only** (as it is today).
- **B-2 No recompute / inference / re-derivation / reclassification / client-side analytics engine / external AI-LLM.** Investigation surfaces disclose **stored** signal lineage, validation, confidence, and related artifacts — they do not recompute confidence or derive new analytical truth.
- **B-3 Verbatim posture preserved.** Where investigation/planning surfaces show validation/economic/confidence values, they render **as-stored** (UI-004 §2.2 discipline carries forward — `research_only`/`not_assessed`/`warning:*` never upgraded).
- **B-4 No-cherry-picking.** Where analytics/comparison surfaces aggregate, included scope / sample counts / uncertainty / limitations remain visible; filtered views never claim full-scope truth unless the stored artifact declares it.
- **B-5 Read-only reuse; no new analytical authorship.** Reuse existing read APIs (`fetchAdvisorySignals`, `fetchAdvisoryAnalytics`, `fetchInstitutionalIntelligenceBundle`, `fetchResearchManagementBundle`, `fetchJournalEntries`, `fetchPortfolioResearchDashboard`, chart/annotation APIs, scenario read APIs). No new charting/markdown/fuzzy dependency without a spike.

---

## 4. Questions the Design Plan MUST answer

1. **Route/registry posture:** Which existing route(s) host UI-005 (e.g. enhance existing `/investigate` `/compare` `/plan` destinations vs a new workspace)? Any registry change must be justified against R-1-style no-drift; state explicitly whether a new registered workspace/route is proposed or existing routes are enhanced.
2. **Persistence posture:** Default **no new table**. If any planning-note / investigation-view saved state is proposed, does it reuse `operator_workspace_preferences` (ids/visibility/filter only) under a named key? Note the persistence-capture control (inline raw psql save→SELECT ≥1 row on the CORRECT table, `operator_id→operators.id`, alembic head) will bind any phase that persists — and note whether Trade Planning / Journal already have their own authorized stores (they appear to, from existing create/update tests) and whether UI-005 only READS them or touches those existing authorized mutations.
3. **Trade Planning & Journal mutation boundary:** These pages today have authorized plan-store / journal-store callbacks. Does UI-005 change any mutation surface, or is it navigation/presentation only over the existing authorized create/update? Any mutation must be justified and constitutionally bounded (research notes only, no order/execution fields).
4. **Execution Research boundary:** Confirm it stays SIMULATED / display-only with no execution/Gate pathway.
5. **Phase split:** Propose a phase breakdown (e.g. P01 frame + data-source inventory + no-recompute/no-actuation guardrail; then per-surface integration; then completion checkpoint) so each phase is narrowly reviewable.
6. **Investigation lineage:** How signal-investigation lineage / validation / related-artifact links are surfaced as disclosure (not recompute), reusing UI-004 report-viewer/drilldown patterns.
7. **UI-002-P04b search adapters:** remain independent/non-blocking, or folded in only after a separate Build Order?

---

## 5. Standing acceptance conditions (every UI-005 phase, going forward)

- **Doc 16 brand gate B-1…B-7** (Part XIV) — constitutional palette / typography + monospace numerics / unified iconography / institutional-not-retail / brand a11y / documentation branding; **never color alone**. Material brand violation ⇒ Corrective.
- **Level-I evidence** — operator-run on target; report-claims alone never approve; build-identity verified FIRST each turn.
- **No-drift substitute** — alembic `20260717_0037` (unless a separately authorized persistence migration), package manifests unchanged, no new endpoint, registry/route change only if justified; git-diff phase-isolation remains retired for the single-commit repo.
- **Regression** — full frontend suite ≥ current baseline (**43f/186t**, no test lost) + backend ≥414.
- **CI** — networked `LOCAL_CI_EXIT_CODE: 0` + sentinel, or documented TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver.
- **Carried security residual TD-UI-POSTCSS-HIGH** — the disclosed high-severity transitive advisory `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) does not gate presentation-only UI-005 work (no dependency change in scope), but remains OPEN and MUST be remediated/accepted before Production Readiness Certification; any UI-005 phase that would touch dependencies must address it.

---

## 6. Deliverable & next step

**DA to deliver:** `UI-005_ENGINEERING_DESIGN_PLAN.md` addressing §2–§5 above, with a §"Open questions for ITRGA" mirroring §4.

**ITRGA will then:** review the plan (Approved / Approved-w-Obs + numbered refinements R-1…R-n), and only on Approved/Approved-w-Obs **issue `BUILD_ORDER_UI-005-P01`**. No implementation is authorized until then.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
