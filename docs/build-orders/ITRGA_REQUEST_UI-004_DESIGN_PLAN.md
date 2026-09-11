# ITRGA REQUEST — UI-004 ENGINEERING DESIGN PLAN
## UI-004 — Research & Intelligence Workspace

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 (4th UI workstream)
**Governing docs:** `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` **§6**; `13_UI_TRANSFORMATION_MASTER_PLAN.md` (UI-004 depends on UI-001 + UI-002 + UI-009); Doc 14/15 (build upon UI-001, don't modify it); **Doc 16 Brand Governance Standard**; existing intelligence/signals/analytics constitution (W3 advisory, W4 intelligence, W6 analytics no-cherry-picking, calibrated-confidence/uncertainty/economic-usefulness framing).
**Predecessor milestones:** 🏛️ **UI-001** · 🏛️ **UI-002** · 🏛️ **UI-003** COMPLETE.
**Sequence note:** ITRGA **requests this Design Plan first**; `BUILD_ORDER_UI-004-P01` issues only after ITRGA accepts the plan.
**Motto:** *We don't guess. We prove.*

---

## 1. What ITRGA is requesting
A DA **Engineering Design Plan** for **UI-004 — Research & Intelligence Workspace** (Doc 12 §6). Objective (verbatim): *"Unify institutional research capabilities."* Full §6 scope:
- Institutional Intelligence
- Advisory Signals
- Performance Analytics
- Research artifacts
- Validation
- Economic usefulness
- Report viewers
- Intelligence drilldowns

Expected outcome (verbatim): *"Institutional research becomes a continuous analytical workflow rather than isolated pages."*

Not implementation, not self-approving. ITRGA returns Approved / Approved-with-Observations + binding refinements / Corrective / Rejected; only an accepted plan authorizes `BUILD_ORDER_UI-004-P01`.

## 2. 🔴 BRIGHTEST LINE #1 (highest-risk yet) — DISPLAY existing governed intelligence, DO NOT recompute or re-derive
UI-004 surfaces the platform's constitutional core (intelligence, signals, analytics). "Continuous analytical workflow" and "drilldowns" mean **presentation/navigation over EXISTING governed research artifacts — NOT new analysis.** The plan MUST honor:
- **No client-side inference / no authoritative recompute / no new analytical algorithm / no signal generation / no regime inference / no economic-usefulness or validation re-derivation.** Validation reports, economic-usefulness verdicts, calibrated confidence, uncertainty, drift/generalization results are **displayed as stored** (read from existing report APIs), never recomputed or re-scored in the browser.
- **Economic-usefulness & validation integrity** — verdicts like `not_assessed` / `economically_usable` and validation statuses are **existing governed values**; UI-004 must render them verbatim with their uncertainty/limitations, never upgrade/downgrade/interpret them.
- **No-cherry-picking (W6 analytics discipline)** — analytics/report views must present the governed dataset as-is (sample counts, uncertainty, limitations shown); no selective/favorable filtering that misrepresents performance.
- **Advisory Signals stay research-advisory-only** — read-only records with guardrails, calibrated confidence, rationale, lineage, freshness + the "not financial advice / not a trade instruction / operator decides" disclaimers; **never actionable** (no execute/order/act).
- **No external AI/LLM** in any intelligence/drilldown feature; **no live/real data; no execution; Gate CLOSED.**

## 3. 🔴 BRIGHTEST LINE #2 — persistence approach declared (research artifacts / saved views)
"Research artifacts" + any saved drilldown/report-view state likely implies persistence. The plan MUST declare its approach:
- **(Preferred) Reuse existing stores** — research artifacts already persist (W4 intelligence reports, W3 signals, W6 analytics, research collections/tags from W7-U03); UI-004 **reads** them. Saved *view/layout* state = reuse `operator_workspace_preferences` (symbol/id lists only, like UI-002/UI-003), no new table.
- **(If a NEW table is proposed)** → standing **persistence-capture control** on first submission (committing script + raw `psql SELECT ≥1 row` + no-orphan audit JOIN + `operator_id → operators.id` JOIN, INLINE raw psql — API read-back never substitutes — + Alembic head progression + `information_schema` forbidden-column proof), justified RBAC-scoped backend touch, **no positions/orders/P&L/actionable fields**. Any new read endpoint likewise justified + flagged for dedicated review; default = reuse existing read APIs.

## 4. 🔴 Extend UI-001/UI-002/UI-003, do NOT duplicate (Doc 15 §12)
UI-004 mounts as workspace(s) **inside the UI-001 shell**; registers via the **14-field Workspace Registry**; navigation via **UI-002** (nav dock / palette / breadcrumbs / global search / workflow metadata) — no page-specific nav, no second palette/overlay. Reuse **Design System tokens** (Doc 16 palette / 11 categories / 18 roles), **Panel/Docking/Layout** (UI-001 P03), **overlay family** (P05), **session-persistence seam** (P04). Reuse UI-003 chart/marker patterns where analytics need charts. The plan MUST include a **reconciliation table** (each §6 item → reuse / extends / net-new) + **UI-009 core-components** dependency status (existing vs proposed; first-party components flagged for later harvesting; no third-party dep without a spike).

## 5. Content ITRGA expects
1. Objective/scope mapped to Doc 12 §6 + **reconciliation table** + UI-009 status.
2. Architecture: how intelligence/signals/analytics/validation/economic-usefulness/report-viewers/drilldowns compose in the shell; state ownership (no business/analysis state; Shell owns nav/layout).
3. **Data-source table** — every surface's origin = **existing governed report/read API** (intelligence bundle, advisory signals, analytics, validation/economic/scenario/correlation/regime reports, research collections/journal); explicit **no new analysis/computation, no recompute, no live feed, no external AI**; any backend touch justified + flagged.
4. **Validation / economic-usefulness / drilldown integrity** — proof surfaces render stored verdicts verbatim with uncertainty/limitations; **no re-derivation**; no-cherry-picking preserved.
5. **Advisory-signal presentation** — read-only, guardrails/calibration/disclaimers preserved, non-actionable.
6. **Persistence design** (§3) — reuse-vs-new-table decision + persistence-capture commitment if new.
7. **Doc 16 brand plan** (B-1…B-7) — constitutional palette / typography+monospace numerics / iconography (incl. Intelligence/Research/Signals categories) / institutional-not-retail / accessibility; no off-palette color.
8. **Accessibility plan** (report tables, drilldowns, charts — keyboard/screen-reader/reduced-motion) first-class.
9. **Phase decomposition** (UI-004-P01…Pn) with dependency rule + per-phase named tests + evidence anchors.
10. **Regression & evidence strategy** — Level-I bar: operator-run on-target evidence, named tests **displayed** passing, no-actuation + **no-recompute/no-inference** source greps, browser-judged served sessions, **full-suite regression ≥ baseline (no test lost)**, networked CI exit 0, head unchanged (or persistence-capture if a table), no unspiked dependency, no-drift substitute (per-phase no-backend/schema/dep test + alembic head + no-endpoint grep + package-manifest — git-diff phase-isolation retired for the single-commit repo).
11. **Constitutional + Doc 16 attestation** + **open questions for ITRGA**.

## 6. Acceptance anchors
Accepted (→ authorizes `BUILD_ORDER_UI-004-P01`) requires: Doc 12 §6 covered; **presentation-only with NO recompute/inference/re-derivation of validation/economic-usefulness/analytics** (brightest line #1); **economic-usefulness & validation rendered verbatim, no-cherry-picking, advisory read-only** ; **persistence approach declared** (reuse preferred; new table pre-commits persistence-capture); **extend-not-duplicate reconciliation** + UI-009 addressed; **Doc 16 brand plan (B-1…B-7)**; accessibility first-class; no external AI / no live data / no execution / Gate CLOSED attested; phase decomposition + Level-I evidence strategy (incl. full-suite ≥ baseline) sound; no unspiked dependency. Otherwise: Approved-with-Observations + binding refinements, Corrective, or Rejected.

Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 36f·151t. Governing hierarchy Docs 00–16. Standing residuals (non-blocking): TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b. Standing gates: constitutional line + **Doc 16 brand (B-1…B-7)** on every phase.

**Please deliver `UI-004_ENGINEERING_DESIGN_PLAN.md`.**

*We don't guess. We prove.*
