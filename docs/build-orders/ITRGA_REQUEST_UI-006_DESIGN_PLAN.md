# ITRGA REQUEST — UI-006 ENGINEERING DESIGN PLAN

**New workstream: UI-006 — Unified Research Artifact Explorer. Design Plan requested BEFORE any Build Order.**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-006 — Unified Research Artifact Explorer** (NEW) |
| Governing docs | Doc 12 §8, `13_UI_TRANSFORMATION_MASTER_PLAN.md` (UI-006 depends on UI-004, UI-005, UI-009), completed UI-001/UI-002/UI-003/UI-004/UI-005 foundations, `16_BRAND_GOVERNANCE_STANDARD.md` |
| Predecessor milestones | 🏛️ UI-001 · UI-002 · UI-003 · UI-004 · UI-005 COMPLETE |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **49f/216t** |
| Action required of DA | **Produce `UI-006_ENGINEERING_DESIGN_PLAN.md`** — DA does NOT implement until ITRGA reviews the plan and issues the first Build Order |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Why a Design Plan first

UI-006 is a **new workstream**. Per the standing ITRGA workflow rule, ITRGA requests the Design Plan first, reviews it (Approved / Approved-with-Observations + numbered refinements), and only then issues the first Build Order. **No implementation is authorized by this request.**

---

## 2. Doc 12 §8 scope (verbatim intent)

**Objective:** Provide centralized access to institutional research artifacts.
**Scope:** Unified artifact explorer · Collections · Tags · Linked artifacts · Lineage · Metadata · Cross-artifact relationships · Advanced filtering.
**Expected outcome:** Every research artifact becomes discoverable, interconnected, and traceable.

---

## 3. 🔴 THE DEFINING RISK — inherited collection/tag MUTATION (UI-004 R-4 deferral)

Across UI-004 and UI-005, collections/tags were held **READ-ONLY**, with mutation explicitly **deferred to UI-006**. UI-006 is therefore the **first UI workstream that may legitimately introduce artifact-organization mutation** (create/update/delete of collections, tags, memberships). This is a heightened constitutional risk and the plan's central concern. The plan MUST pre-register:

- **M-1 Mutation scope is ORGANIZATION-ONLY.** Any create/update/delete applies strictly to **research-artifact organization** — collection names/descriptions, tag labels, artifact↔collection and artifact↔tag associations. It must **never** create, alter, recompute, reclassify, or upgrade the **underlying artifacts** (signals, reports, validation, economic verdicts, scenarios, plans, journal, execution research) or their stored values.
- **M-2 No new analytical truth / no verdict mutation.** Organizing an artifact into a collection or tagging it must not change any stored verdict, confidence, validation status, economic-usefulness value, or lineage. Verbatim posture (UI-004 §2.2) is preserved on every displayed artifact value.
- **M-3 Existing authorized store + persistence discipline.** Prefer the existing W7-U03 research-management collection/tag store/APIs. If any mutation is persisted, the **persistence-capture control** binds that phase (inline raw psql save→SELECT ≥1 row on the CORRECT table, `operator_id → operators.id`, no forbidden fields, `alembic current`). **If a new table or migration is genuinely required for cross-artifact relationships, it must be explicitly justified, separately called out, and it changes the no-drift posture** (this would be the first UI workstream to add a migration — treat as a distinct, heightened-evidence sub-decision).
- **M-4 No actuation, ever.** No order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path anywhere in the explorer or its mutations. Cross-artifact relationships and filtering are research-organization only.
- **M-5 No external AI/LLM, no client-side analytics engine, no recompute/inference** in the explorer, filtering, or relationship mapping.

---

## 4. Questions the Design Plan MUST answer

1. **Route/registry posture:** Does UI-006 add a new registered `/artifacts` (or similar) workspace route, or enhance existing surfaces? Any new route/registry entry must be justified against the 14-field Workspace Registry contract and no-duplicate-navigation; state explicitly.
2. **Mutation model (the central question):** Exactly which mutations does UI-006 introduce (collection create/update/delete? tag create/update/delete? membership add/remove?), on which existing authorized store, and how is M-1/M-2 (organization-only, no underlying-artifact/verdict mutation) enforced and tested? Which phase introduces the FIRST mutation?
3. **Persistence & schema:** Can UI-006 reuse the existing W7-U03 collection/tag store with no new table? If a new table/migration is proposed for cross-artifact relationships, justify it explicitly and flag the alembic-head change (heightened evidence).
4. **Read surfaces:** Lineage, metadata, cross-artifact relationships, advanced filtering — mapped to which existing read APIs (`fetchResearchManagementBundle`, `fetchResearchCollections`, `fetchResearchTags`, and the UI-004/UI-005 read seams)? No new analytical authorship.
5. **Verbatim preservation:** How does the explorer preserve verbatim artifact values (verdicts/validation/economic/confidence) and no-cherry-picking when aggregating/filtering across artifacts?
6. **Phase split:** Propose a phase breakdown (e.g. P01 explorer frame + data-source inventory + no-actuation/no-recompute guardrail READ-ONLY; then read lineage/relationships/filtering; then the mutation phase(s) with the persistence-capture control; then completion) so each phase — especially the first mutation phase — is narrowly reviewable.
7. **UI-002-P04b search adapters & UI-009 dependency:** How does advanced filtering relate to the existing global search (UI-002-P04b, still independent) and the UI-009 design-system dependency (not yet built)? Any first-party components flagged for later UI-009 harvest?

---

## 5. Standing acceptance conditions (every UI-006 phase, going forward)

- **Doc 16 brand gate B-1…B-7** (Part XIV) — never color alone; material violation ⇒ Corrective.
- **Level-I evidence** — operator-run on target; report-claims alone never approve; build-identity verified FIRST each turn.
- **No-recompute / no-actuation / no-external-AI whole-surface greps** each phase; **verbatim + no-cherry-picking** preserved.
- **🔴 Mutation phases:** organization-only proof (M-1/M-2), no-underlying-artifact-mutation named test, and the **persistence-capture control** (inline raw psql save→SELECT ≥1 row, `operator_id→operators.id`, no forbidden fields, alembic head) — API/in-process read-back NEVER substitutes; `(0 rows)` = disproof. Any new migration is a distinct heightened-evidence sub-decision.
- **No-drift substitute** — alembic `20260717_0037` unless a separately-justified persistence migration; package manifests unchanged (no new dep); registry/route change only if justified; git-diff phase-isolation remains retired for the single-commit repo.
- **Regression** — full frontend suite ≥ current baseline (**49f/216t**, no test lost) + backend ≥414.
- **CI** — networked `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR the TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver; OR `LOCAL_CI_EXIT_CODE: 1` solely the tracked **TD-UI-POSTCSS-HIGH** after substantive gates green → disclosed, standing disposition. Any other nonzero cause is a finding.
- **🔴 Carried security residual TD-UI-POSTCSS-HIGH** — OPEN (Path-B accepted at UI-005 completion). It does not gate presentation-only UI-006 work, but **must be remediated/accepted before Production Readiness Certification** — and any UI-006 phase that touches dependencies must address it.

---

## 6. Deliverable & next step

**DA to deliver:** `UI-006_ENGINEERING_DESIGN_PLAN.md` addressing §2–§5 above, with a §"Open questions for ITRGA" mirroring §4 and a dedicated **mutation-boundary section** (M-1…M-5).

**ITRGA will then:** review the plan (Approved / Approved-w-Obs + numbered refinements R-1…R-n), and only on Approved/Approved-w-Obs **issue `BUILD_ORDER_UI-006-P01`**. No implementation is authorized until then.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
