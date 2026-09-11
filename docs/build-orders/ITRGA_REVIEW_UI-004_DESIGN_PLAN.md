# ITRGA REVIEW — UI-004 ENGINEERING DESIGN PLAN
## UI-004 — Research & Intelligence Workspace

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004
**Plan under review:** `UI-004_ENGINEERING_DESIGN_PLAN.md` (756 lines) · Request: `ITRGA_REQUEST_UI-004_DESIGN_PLAN.md`
**Determination:** ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-7)**
**Authorizes:** `BUILD_ORDER_UI-004-P01` (Research Workspace Frame, Data-Source Inventory & No-Recompute Guardrail) — subject to the refinements below.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct plan: references the ITRGA request + UI-001/UI-002/UI-003 completion + Doc 16; baseline v0.62.0 / head `20260717_0037` / backend 414 / frontend 36f·151t; Gate CLOSED; DA does not self-approve.

## 1. What the plan gets right (against the acceptance anchors)
- **🔴 Brightest line #1 — display, NOT recompute (met decisively).** §2.1 categorically bars client-side inference / authoritative recompute / new algorithms / signal generation / regime inference / recompute of correlations/scenarios/validation/calibration/drift/portfolio-risk/economic-usefulness / external-AI summaries / changing stored verdicts / hiding unfavorable sample counts. §2.2 gives a **permitted-vs-forbidden rendering table** (`not_assessed`→"Not assessed" not "Economically usable"; `research_only`→not "Tradable/executable"; `warning:POORLY_CALIBRATED`→not "Approved"). §7.1 verbatim-rendering rule + §7.2 "drilldown = progressive disclosure of stored fields, NOT recomputation/LLM-summary/reclassification."
- **🔴 No-cherry-picking (met).** §2.3/§7.3: sample counts, uncertainty, limitations, included scope, source-artifact ids visible; filtered views must not claim full-scope truth; **"no code path computes new aggregate performance from displayed rows."**
- **🔴 Advisory posture (met).** §2.4: read-only, **calibrated confidence not raw-score**, guardrails/lineage/freshness/economic-verdict, disclaimers, non-actionable.
- **🔴 Persistence (met, preferred path).** §6: **reuse existing stores + `operator_workspace_preferences` for view state; no new table.** Saved-view payload = ids/visibility/filter prefs only.
- **Extend-not-duplicate (met).** §3 reconciliation maps each §6 item to reuse/extend; §3.1 anti-duplication incl. **"no browser-side analytics engines"** and no off-palette tokens; §3.2 UI-009 via first-party components (report viewer / lineage-uncertainty-economic panels local candidates), no third-party dep.
- **Doc 16 brand plan (met).** §9 addresses B-1…B-7 (constitutional palette, monospace for ids/confidence/hashes, institutional-not-retail copy, brand proof in browser every phase).
- Accessibility first-class (§10); 6-phase decomposition (§12) with dependency rule; comprehensive **§17 attestation**; DA does not self-approve.

## 2. Binding refinements (fold into the relevant Build Orders; conditions of acceptance)
- **R-1 (§15 Q1) — ACCEPTED:** enhance existing `/intelligence` as the primary UI-004 workspace while **preserving `/signals` and `/analytics` as workflow destinations**. Any Workspace-Registry change (route add/relabel) is **ITRGA-pre-approval-gated** — registry stays the single source of truth (UI-002 R-1); prove the 14-field contract is not broken.
- **R-2 (§15 Q2/Q5) — ACCEPTED with condition:** default **no-new-table**; saved view state via `operator_workspace_preferences` (`research-intelligence-workspace-v1`, ids/visibility/filter only). **If saved state is implemented, R-2 requires one inline raw psql read-back** (≥1 row, ids/prefs only, no forbidden fields, `alembic current`=head) at that phase — API read-back does not substitute (UI-003-P02 precedent).
- **R-3 (§15 Q3) — SPLIT: advisory signals (P02) and performance analytics (P02b or a distinct slice) reviewed narrowly.** Given this is the highest-risk domain, do **not** land both large integrations in one under-scoped phase; analytics (the no-cherry-picking surface) gets its own focused evidence.
- **R-4 (§15 Q4) — collections/tags REMAIN READ-ONLY in UI-004** (context/linking only); any collection/tag mutation defers to UI-006 Artifact Explorer. UI-004 must not add create/update mutation surfaces.
- **R-5 (§15 Q6) — UI-002-P04b is INDEPENDENT/non-blocking**; UI-004 may consume existing search but must not bundle P04b adapter work without a separate Build Order.
- **R-6 — 🔴 NO-RECOMPUTE / NO-INFERENCE is the spine every phase.** Each phase owes: named test(s) proving surfaces render stored values only; a **no-recompute/no-inference source grep** (`inferSignal|runInference|authoritativeRecompute|emitSignal|recompute|recalculat|deriveConfidence|new .*Engine|/api/v1/orders`) clean; a **verbatim-rendering test** for validation/economic-usefulness (stored verdict shown, not reclassified); a **no-cherry-picking test** (sample counts/uncertainty/limitations/scope visible; no aggregate computed from displayed rows). Any recompute/inference/verdict-mutation ⇒ Corrective.
- **R-7 — Standing Level-I bar + Doc 16 gate every phase.** Build-identity first; named tests **displayed** passing; no-actuation grep; browser-judged served sessions **with brand proof (B-1…B-7)**; **full-suite regression ≥ baseline with NO test lost** (explicit lesson from UI-003-P05 — verify the full-suite total each phase); networked CI exit 0 + sentinel (offline-audit env-flake waivable); head `20260717_0037` (or persistence-capture if a table); no unspiked dependency; no-drift substitute (per-phase no-backend/schema/dep test + `alembic current` + package-manifest + no-endpoint grep).

## 3. Determination & rationale
**APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS.** On the highest-risk domain workstream, the plan holds both pre-registered brightest lines with precision: it is **presentation over existing governed intelligence with no recompute/inference/re-derivation** (§2.1/§2.2/§7 — verbatim rendering, permitted-vs-forbidden table, drilldown-as-disclosure), preserves **no-cherry-picking** and **read-only advisory posture**, **reuses existing stores with no new table**, extends UI-001/UI-002/UI-003 without duplication (no browser-side analytics engine), and presents a complete **Doc 16 brand plan**. It is not a *clean* Approve only because §15 raises **six legitimate open questions**, now ruled as **R-1…R-5**, plus the standing **R-6** (no-recompute spine) and **R-7** (Level-I + Doc 16 + full-suite-≥-baseline).

Per the sequence, **an accepted plan authorizes the first Build Order.** → **`BUILD_ORDER_UI-004-P01` (Research Workspace Frame, Data-Source Inventory & No-Recompute Guardrail) is authorized** — frontend-only, maps every surface to existing governed sources, establishes the no-recompute guardrail; **no report viewers/drilldowns yet** (P03), **no validation/economic panels yet** (P04), **no saved-state persistence yet** (P05) — with R-6/R-7 applied and R-1 binding.

**Constitutional + brand posture:** Gate CLOSED; presentation-only; no recompute/inference/AI/live-data/execution; UI-001/UI-002/UI-003 unmodified; Doc 16 B-1…B-7 gate applies. Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 36f·151t. Residuals: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
