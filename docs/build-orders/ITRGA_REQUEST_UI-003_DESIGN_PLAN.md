# ITRGA REQUEST — UI-003 ENGINEERING DESIGN PLAN
## UI-003 — Professional Market Workspace

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 (3rd UI workstream)
**Governing docs:** `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` **§5 (UI-003 objective/scope)**; `13_UI_TRANSFORMATION_MASTER_PLAN.md` (UI-003 depends on UI-001 + UI-002 + UI-009 core components); Doc 14/15 (build upon UI-001 without modifying its architectural responsibilities); existing chart constitution (W0 candlesticks / W5-U03 inert research annotations).
**Predecessor milestones:** 🏛️ **UI-001 COMPLETE** · 🏛️ **UI-002 COMPLETE**.
**Sequence note (operator-corrected):** ITRGA **requests this Design Plan first**; `BUILD_ORDER_UI-003-P01` is issued only after ITRGA accepts the plan.
**Motto:** *We don't guess. We prove.*

---

## 1. What ITRGA is requesting
A DA **Engineering Design Plan** for **UI-003 — Professional Market Workspace** (Doc 12 §5). Objective (verbatim): *"Transform market observation into a professional analytical environment."* Full Doc 12 §5 scope:
- Professional chart workspace
- Market overview
- Watchlists
- Chart overlays
- Annotation integration
- Research markers
- Market status
- Layout improvements

Expected outcome (verbatim): *"Charts become the operational centre of AXIOM."*

The plan is **not** implementation and **not** self-approving. On receipt, ITRGA returns **Approved / Approved-with-Observations + binding refinements / Corrective / Rejected**; only an accepted plan authorizes `BUILD_ORDER_UI-003-P01`.

## 2. 🔴 CONSTITUTIONAL READ-BEFORE-YOU-DESIGN — UI-003 is presentation, NOT new analysis
This is the first UI workstream that touches a *domain* surface (charts/market), so ITRGA pre-registers the brightest line: **"Professional analytical environment" and "charts become the operational centre" mean PRESENTATION improvements over EXISTING governed data — NOT new analysis, computation, or capability.** The plan MUST honor:
- **No client-side inference / no authoritative recompute / no new analytical algorithm** (existing chart constitution: `/charts` is research markup only; W5-U03 = inert annotations; **no client-side inference**).
- **No live/real market data, no real prices, no broker/feed.** Market data remains **simulated/governed** (`seed:synthetic` = non-authoritative; `live:simulated`). Chart context stays non-authoritative.
- **No execution/actuation** anywhere on the chart/market surface — no order ticket, buy/sell, go-live, connect-broker, price alerts that act. Research markers/overlays are **inert annotations**, not signals or instructions.
- **Chart overlays / research markers / annotation integration** = presentation of **existing** governed annotations/signals (read-only), not generation of new ones.
- **Market status / market overview** = display of existing governed status (like the Operations WebSocket-readiness/health surfaces), not a new data pipeline.
- **Gate stays CLOSED**; research-only posture and disclaimers preserved.

## 3. 🔴 Watchlists — the likely NEW PERSISTED TABLE (pre-registered)
"Watchlists" strongly implies **new operator-scoped persistence.** The plan MUST state its persistence approach explicitly and choose one:
- **(Preferred) Reuse `operator_workspace_preferences`** (as UI-002 recents did) — watchlist = operator preference (symbol id list), no new table. If so: route-ids/symbol-ids only, operator-scoped, no schema creep.
- **(If a NEW table is proposed)** it triggers the **standing persistence-capture control** on first submission: committing script + **raw `psql SELECT ≥1 row`** on the new table + **no-orphan audit JOIN** (`orphan_count 0`) + **`operator_id → operators.id` no-orphan JOIN** — INLINE raw psql (an API read-back NEVER substitutes) + Alembic head progression + `information_schema` forbidden-column proof. A new table also requires a **backend touch**, which must be justified, RBAC-scoped, no execution surface, and flagged for a dedicated persistence/endpoint review. Watchlist contents are **symbol references only** — no positions/quantities/orders/P&L.

## 4. 🔴 Extend UI-001/UI-002, do NOT duplicate (Doc 15 §12)
UI-003 must **consume** the completed infrastructure, not rebuild it:
- Mount as **workspace(s) inside the UI-001 shell** (Regions A–F); register via the **14-field Workspace Registry**; navigation via the **UI-002 Nav Dock / palette / breadcrumbs / global search / workflow metadata** (no page-specific nav, no second palette/overlay).
- Reuse the **Design System tokens** (11 categories / 18 semantic color roles; never color alone), **Panel Infrastructure / Docking / Layout Manager** (P03), **overlay family** (P05), **session persistence** seam (P04).
- The plan MUST include a **UI-001/UI-002 reconciliation table** mapping each Doc 12 §5 item to reuse / extends / net-new, with an explicit no-duplication commitment. **UI-009 "core components"** dependency: state which core components UI-003 needs and whether they exist or are proposed (a new shared-component workstream may be a prerequisite — flag it).

## 5. Content ITRGA expects in the Design Plan
1. Objective/scope restatement mapped to Doc 12 §5 + **UI-001/UI-002 reconciliation table** (§4) + UI-009 dependency status.
2. Architecture: how the professional chart workspace, market overview, watchlists, overlays, research markers, market status compose within the shell; state ownership (Shell owns nav/layout; workspace owns presentation; **no business/analysis state**).
3. **Data-source table** — every surface's data origin = **existing read API / existing governed annotation/signal store / simulated market feed**; explicitly **no new analytical computation, no live feed, no new backend analysis**. Any backend touch justified + flagged.
4. **Watchlist persistence design** (§3) — reuse-vs-new-table decision + the persistence-capture commitment if new.
5. **Chart overlays / research markers / annotation integration** — proof they render **existing** governed annotations read-only; no client-side inference; provenance/non-authoritative markers preserved.
6. **Constitutional attestation** — presentation-only, no new analysis/capability, no live/real data, no execution/AI, Gate CLOSED, extends-not-modifies UI-001/UI-002.
7. **Accessibility plan** (charts are hard for a11y — keyboard/screen-reader/reduced-motion for chart controls, overlays, watchlists) as a first-class section.
8. **Phase decomposition** (UI-003-P01…Pn) with dependency rule (no later phase until ITRGA accepts the prior), each phase's named tests + evidence anchors.
9. **Regression & evidence strategy** — Level-I bar: operator-run on-target evidence, named tests displayed passing, no-actuation source grep, browser-judged served sessions, networked CI exit 0 + sentinel, head unchanged (or persistence-capture if a table is added), no unspiked dependency (charting lib? — if a new chart dependency is proposed it needs a **wheel/bundle-compat spike + ITRGA sign-off**; note the platform already uses TradingView Lightweight Charts).
10. Risks/assumptions/**open questions for ITRGA**.

## 6. Acceptance anchors (how ITRGA will judge the plan)
Accepted (→ authorizes `BUILD_ORDER_UI-003-P01`) requires: Doc 12 §5 scope covered; **presentation-only with NO new analysis/computation/live-data/capability** (the domain brightest line, §2); **watchlist persistence approach declared** (reuse preferred; new table pre-commits the persistence-capture control, §3); **extend-not-duplicate reconciliation** + UI-009 dependency addressed (§4); overlays/markers render existing governed data read-only; accessibility first-class; no execution/AI; Gate CLOSED attested; phase decomposition + Level-I evidence strategy sound; no unspiked charting dependency. Otherwise: Approved-with-Observations + binding refinements, Corrective, or Rejected.

Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 31f·127t. Standing residuals (non-blocking): TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT. Standing methodology: git-diff phase-isolation retired (single-commit repo) — no-drift via per-phase no-backend/schema/dep test + alembic head + no-endpoint grep + package-manifest content.

**Please deliver `UI-003_ENGINEERING_DESIGN_PLAN.md`.**

*We don't guess. We prove.*
