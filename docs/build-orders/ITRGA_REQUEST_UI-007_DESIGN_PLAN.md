# ITRGA REQUEST — UI-007 ENGINEERING DESIGN PLAN

**New workstream: UI-007 — Governance & Evidence Workspace. Design Plan requested BEFORE any Build Order.**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-007 — Governance & Evidence Workspace** (NEW) |
| Governing docs | Doc 12 §9, `13_UI_TRANSFORMATION_MASTER_PLAN.md` (UI-007 depends on UI-004, UI-006), completed UI-001…UI-006 foundations, `16_BRAND_GOVERNANCE_STANDARD.md`, and the constitutional corpus (Docs 00–11) it will surface |
| Predecessor milestones | 🏛️ UI-001 · UI-002 · UI-003 · UI-004 · UI-005 · UI-006 COMPLETE |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **55f/246t** |
| Action required of DA | **Produce `UI-007_ENGINEERING_DESIGN_PLAN.md`** — DA does NOT implement until ITRGA reviews the plan and issues the first Build Order |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Why a Design Plan first

UI-007 is a **new workstream**. Per the standing ITRGA workflow rule, ITRGA requests the Design Plan first, reviews it (Approved / Approved-with-Observations + numbered refinements), and only then issues the first Build Order. **No implementation is authorized by this request.**

---

## 2. Doc 12 §9 scope (verbatim intent)

**Objective:** Expose constitutional governance through professional operator interfaces.
**Scope:** Governance status · Audit explorer · Certification status · Platform health · Evidence viewer · Validation summaries · System readiness · Version information.
**Expected outcome:** Governance becomes visible without disrupting analytical workflows.

---

## 3. 🔴 THE DEFINING RISK — a governance UI must NEVER become a governance CONTROL surface

UI-007 is the most **constitutionally reflexive** workstream: it visualizes the very controls the constitution and this Authority enforce (the CLOSED Governance Gate, audit events, certification status, validation, readiness). The single overriding risk is that a "governance workspace" quietly becomes a **control panel**. The plan MUST pre-register:

- **G-1 READ-ONLY governance display.** UI-007 shall **display** existing governance/audit/certification/validation/health/version records only. It must **never** provide a control to open/close the Governance Gate, change governance state, approve/actuate certification, edit/delete/annotate audit events, or alter validation/readiness verdicts. No governance mutation of any kind.
- **G-2 The Gate is shown CLOSED and is INERT.** Any Gate-status surface renders the constitutional CLOSED state as **read-only fact** — no toggle, no "open gate" affordance, no `open_gate`/`allow_execution` path. Showing the Gate must not create a way to touch it.
- **G-3 Certification status is DISPLAY, not actuation.** "Certification status" and "system readiness" render the existing Doc 11 status (HELD / NOT CERTIFIED) as stored — no "certify" / "mark ready" / "approve production" control. Certification remains an out-of-band governance act, never a UI button.
- **G-4 Audit explorer is READ-ONLY.** Audit events (incl. reason-codes `details->>'reason_code'`, `*_REFUSED`) are displayed verbatim from `audit_events`; no create/edit/delete/redact/replay. Reason-codes and refusals rendered as-stored (not reinterpreted).
- **G-5 Evidence viewer = verbatim disclosure.** Validation summaries, evidence, readiness, version info rendered **as-stored** (UI-004 §2.2 verbatim discipline) — no recompute/re-derivation/reclassification; no-cherry-picking (scope/sample/limitations visible where applicable).
- **G-6 No actuation / no external AI / no recompute.** Standard brightest lines: no order/broker/account/live/execute path; no external LLM; no client-side analytics engine.
- **G-7 Read-only reuse.** Reuse existing read APIs/stores (governance status, `audit_events`, health/monitoring, certification/readiness, validation, version). No new dependency; no new backend capability.

---

## 4. Questions the Design Plan MUST answer

1. **Route/registry posture:** Does UI-007 add a new registered `/governance` (or similar) workspace route, or enhance an existing surface? Justify against the 14-field Workspace Registry contract and no-duplicate-navigation.
2. **Read-only enforcement (the central question):** How is G-1…G-4 enforced and tested — i.e. how does the plan guarantee the governance/audit/certification surfaces expose **no** mutation/actuation/Gate/certify control? Which named tests prove it (a `no_governance_mutation_or_gate_or_certification_control` test is expected every phase)?
2b. **Gate & certification rendering:** Exactly how are the CLOSED Gate and NOT-CERTIFIED/HELD status rendered as inert read-only facts (no toggle/affordance)?
3. **Data sources:** Governance status / audit events (`audit_events`, `details->>'reason_code'`) / platform health / certification-readiness (Doc 11) / validation summaries / version — mapped to which existing read APIs? Confirm `audit_events` has a read API (or identify the existing read seam) and that reason-codes/`*_REFUSED` render verbatim.
4. **Persistence posture:** Default **no new table**; UI-007 is display-only. If any saved-view state is proposed, reuse `operator_workspace_preferences` (ids/visibility/filter only) with the persistence-capture control binding that phase. No governance-state persistence.
5. **Constitutional self-surfacing:** Since UI-007 displays the constitution's own guardrails, how does it avoid misrepresenting them (e.g. showing "Gate CLOSED" must not imply an operator-openable control; certification "HELD" must not imply a UI unblock)?
6. **Verbatim + no-cherry-picking:** How validation summaries / evidence / audit reason-codes are shown verbatim, with scope/limitations, never recomputed or reclassified.
7. **Phase split:** Propose a reviewable phase breakdown (e.g. P01 frame + data-source inventory + no-actuation/no-governance-mutation guardrail; then governance-status/Gate/certification display; then audit explorer; then evidence/validation/health/version; then completion).
8. **TD-UI-POSTCSS-HIGH:** UI-007 introduces no dependency, but per the UI-006 completion the postcss remediation is now a non-waivable pre-certification blocker — does the DA propose to schedule the dedicated dependency-remediation Build Order during UI-007 (recommended) or continue carrying it? (UI-007 notably includes a "certification status" surface, making the pre-cert residual especially relevant to display honestly.)

---

## 5. Standing acceptance conditions (every UI-007 phase, going forward)

- **🔴 G-1…G-7 read-only governance discipline** — no governance mutation / Gate control / certification actuation / audit mutation; every phase carries a **`..._contains_no_governance_mutation_gate_or_certification_control`** named test + the whole-surface no-actuation grep (M-4 expanded incl. `open_gate|allow_execution`).
- **Doc 16 brand gate B-1…B-7** (Part XIV) — never color alone; material violation ⇒ Corrective.
- **Level-I evidence** — operator-run on target; report-claims alone never approve; build-identity verified FIRST.
- **Verbatim + no-cherry-picking + no-recompute/no-external-AI** whole-surface greps each phase; audit reason-codes/`*_REFUSED` and certification/validation status rendered as-stored.
- **No-drift substitute** — alembic `20260717_0037`; package manifests unchanged (no new dep); registry/route change only if justified.
- **Regression** — full frontend suite ≥ current baseline (**55f/246t**, no test lost) + backend ≥414; gated run exit 0.
- **CI** — networked `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR TD-W6-CI-AUDIT env-flake waiver after substantive gates green; OR `LOCAL_CI_EXIT_CODE: 1` solely the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed. Any other nonzero is a finding.
- **🔴 TD-UI-POSTCSS-HIGH** — OPEN, Path-B re-accepted at UI-006 completion, now a **non-waivable pre-certification blocker**; must be remediated before Production Readiness Certification. Since UI-007 surfaces certification status, the certification surface must honestly reflect this residual as a pre-cert blocker.

---

## 6. Deliverable & next step

**DA to deliver:** `UI-007_ENGINEERING_DESIGN_PLAN.md` addressing §2–§5, with a dedicated **read-only governance-boundary section (G-1…G-7)** and a §"Open questions for ITRGA" mirroring §4.

**ITRGA will then:** review the plan (Approved / Approved-w-Obs + numbered refinements R-1…R-n), and only on Approved/Approved-w-Obs **issue `BUILD_ORDER_UI-007-P01`**. No implementation is authorized until then.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
