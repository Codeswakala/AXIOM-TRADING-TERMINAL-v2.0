# ITRGA REVIEW — UI-003 ENGINEERING DESIGN PLAN
## UI-003 — Professional Market Workspace

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003
**Plan under review:** `UI-003_ENGINEERING_DESIGN_PLAN.md` (597 lines) · Request: `ITRGA_REQUEST_UI-003_DESIGN_PLAN.md`
**Determination:** ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-6)**
**Authorizes:** `BUILD_ORDER_UI-003-P01` (Market Workspace Frame & Data-Source Inventory) — subject to the refinements below.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct plan: references the ITRGA request + UI-001/UI-002 completion; baseline v0.62.0 / head `20260717_0037` / backend 414 / frontend 31f·127t; Gate CLOSED; DA does not self-approve.

## 1. What the plan gets right (against the acceptance anchors)
- **🔴 Brightest line #1 — presentation, NOT new analysis (met decisively).** §2.1 bars client-side inference / authoritative recompute / new algorithms / signal generation / real feed / broker-execution / external AI. §2.2 preserves `seed:synthetic` (non-authoritative) + `live:simulated` provenance labels; forbids labeling simulated data as real. §2.3 makes overlays/markers **read-only presentation of existing governed artifacts**. **§5 data-source table: all seven surfaces = existing data origin, "New backend? No"**; §5.1 categorical no-new-analysis statement.
- **🔴 Brightest line #2 — watchlists (met, preferred path).** §6.1 **reuses `operator_workspace_preferences`, NO new table** (`professional-market-workspace-v1`; watchlists = symbol/timeframe **id lists** in `layout_config`); §6.3 forbids quantity/position/order/side/broker/account/margin/capital/stop/target/P&L/gate fields. The persistence-capture-control trigger is thereby **avoided by design**.
- **Extend-not-duplicate (met).** §3 reconciliation maps each §5 item to extends/reuse of UI-001 shell/panels/tokens + UI-002 nav/palette/breadcrumbs/search; §3.1 anti-duplication commitments (no second shell/nav/palette/overlay/header/route-map).
- **UI-009 dependency (resolved).** §3.2 uses existing primitives + small **first-party** components (flagged for later UI-009 harvesting); **no third-party component dependency** → no blocking prerequisite.
- **Accessibility first-class** (§8: chart/watchlist/overlay keyboard + screen-reader + reduced-motion). **Phase decomposition** (§10: P01 frame/inventory → P02 watchlists → P03 overlays/markers/annotations → P04 market status/overview/responsive → P05 completion). **§15 attestation** comprehensive; DA does not self-approve.

## 2. Binding refinements (fold into the relevant Build Orders; conditions of acceptance)
- **R-1 (answers §13 Q1) — ACCEPTED:** watchlists via `operator_workspace_preferences` (symbol/timeframe ids only, no new table) is the approved P02 persistence approach. Binds UI-003-P02.
- **R-2 (answers §13 Q5) — YES, require ONE raw psql read-back at P02** even though no new table: a raw `psql SELECT` on `operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1'` showing the persisted watchlist row contains **symbol/timeframe ids only** (no forbidden fields). This is lighter than the full persistence-capture control (no new table ⇒ no orphan-JOIN battery required) but ITRGA wants **one inline raw-DB proof** that the reused row is clean — not an API-only read-back.
- **R-3 (answers §13 Q2) — DEFER advisory-signal markers to P03, gated:** read-only signal markers are acceptable in **P03** (not P01), and only as **inert read-only badges over existing advisory records** — a named test must prove markers are not signals/instructions/actionable and generate nothing.
- **R-4 (answers §13 Q3) — watchlist reorder in P02 is fine IF keyboard-accessible;** if the accessible reorder is not ready, defer to P04 rather than ship an inaccessible drag-only control (R-6 a11y bar).
- **R-5 (answers §13 Q4) — UI-002 P04b (remaining search adapters) is INDEPENDENT of UI-003;** schedule it whenever convenient (before/after/parallel) — it does not block UI-003. Note it remains outstanding.
- **R-6 — Standing bright-lines + Level-I bar (binding every phase):** presentation-only / no new analysis / no live-real data / no execution/actuation (source grep + named test each phase); **market data provenance labels visible** in the browser (`seed:synthetic`/`live:simulated`); overlays/markers render existing governed data read-only; Gate CLOSED/research framing visible; extend-not-duplicate (no second shell/nav/palette/overlay); accessibility first-class; **no unspiked charting dependency** (reuse existing `lightweight-charts`; any new dep needs a wheel/bundle spike + ITRGA sign-off); no-drift via the retired-git-diff substitute (per-phase no-backend/schema/dep test + `alembic current` = head + no-endpoint grep + package-manifest content); named tests **displayed** passing; browser-judged served sessions; networked CI exit 0 + sentinel; backend ≥414 / frontend grown; **build-identity verified first every turn.**

## 3. Determination & rationale
**APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS.** The plan meets every acceptance anchor and — critically for the first *domain* workstream — holds both pre-registered brightest lines cleanly: it is **presentation over existing governed data with no new analysis/computation/live-data/capability** (§2/§5), and **watchlists reuse the existing preferences table with symbol references only** (§6), avoiding the persistence-capture trigger. It extends UI-001/UI-002 without duplication, resolves the UI-009 dependency with first-party components, and treats accessibility as first-class. It is not a *clean* Approve only because §13 raises **five legitimate open questions**, now ruled as **R-1…R-5**, plus the standing R-6 bright-line/Level-I bar.

Per the UI-Transformation sequence, **an accepted plan authorizes the first Build Order.** → **`BUILD_ORDER_UI-003-P01` (Professional Market Workspace Frame & Data-Source Inventory) is authorized** — frontend-only, chart-centered composition inside the UI-001/UI-002 shell, **no watchlist persistence yet** (P02), **no overlays/markers yet** (P03) — with R-6 applied and R-1/R-2 binding P02, R-3 binding P03.

**Constitutional posture:** Gate CLOSED; presentation-only; no new analysis/live-data/execution/AI; UI-001/UI-002 unmodified. Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 31f·127t. Residuals: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, and outstanding **UI-002 P04b** (remaining search adapters, non-blocking).

*We don't guess. We prove.*
