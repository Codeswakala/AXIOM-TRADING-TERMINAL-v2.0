# BUILD ORDER — UI-007-P02

**Governance Status · Gate CLOSED · Certification Status Display** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P02** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-007-P01.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-1…G-7)/§8 (P02), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8), Doc 11, Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **56f/251t** (vite-8 toolchain) |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Render the **governance status**, the **CLOSED Governance Gate**, and the **certification status** as **read-only, inert constitutional facts** on the `/governance` workspace. This is the surface most exposed to the "governance UI becomes a control panel" risk — **G-2 (Gate inert) and G-3 (certification display, not actuation) are the spine.** Display-only; no control.

**IN scope:**
1. Governance status panel — existing governance posture rendered read-only.
2. **Gate CLOSED** — rendered as an inert read-only constitutional fact (no toggle/button/switch/form/palette action).
3. **Certification status** — Production NOT CERTIFIED / Doc 11 Certification HELD, plus the Doc 11 outcome vocabulary (CERTIFIED / CERTIFIED WITH CONDITIONS / DEFERRED / NOT CERTIFIED) shown as-stored; canonical records only (no certification endpoint — R-2).
4. **Residual honesty:** TD-UI-POSTCSS-HIGH is now **CLOSED** (dependency remediation approved) — the certification/pre-cert surface must reflect this accurately (no longer an open blocker); any remaining residuals (react-router moderate, TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b) shown as-stored, none relabeled.

**OUT of scope (do NOT build):**
- Audit explorer (P03), evidence/validation (P04), health/readiness/version (P05), completion (P06).
- **Any governance/Gate/certification control** — no open/close/toggle Gate, no certify/mark-ready/approve-production, no waive/accept-risk, no governance-status or verdict mutation (G-1…G-3).
- Any actuation / order / broker / account / live / execute path (G-6/M-4); external AI/LLM; recompute/inference/reclassification.
- Any new backend endpoint / service / table / migration / dependency / governance-state persistence (G-7); saved-view persistence.
- Certification-status backend endpoint (R-2 — canonical read-only records only).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/governance` (from P01); no new route; 14-field registry contract unchanged.
- **R-2** — Certification = canonical **read-only** posture; **no certification endpoint**.
- **R-7 (SPINE)** — G-2 Gate inert + G-3 certification display-not-actuation; mandatory named test `test_ui007_governance_status_contains_no_governance_mutation_gate_or_certification_control`; G-2 grep + M-4 no-actuation grep + no-recompute/external-AI grep.
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.
- **OBS-P01-1 closure (MANDATORY):** supply a **clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite run** (≥ 56f/251t, no test lost) on an unlocked machine (resolve the `@rolldown` EPERM/AV file-lock). A red/partial run again ⇒ Corrective.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui007_governance_status_renders_existing_posture_read_only`
2. `test_ui007_gate_closed_is_inert_no_toggle_or_control`
3. `test_ui007_certification_status_is_display_not_actuation`
4. `test_ui007_governance_status_contains_no_governance_mutation_gate_or_certification_control`
5. `test_ui007_governance_status_accessibility_and_doc16_brand_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL creds standard.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-007-P02.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 G-2 Gate-inert proof** — Gate CLOSED rendered as read-only fact; NOT a button/switch/checkbox/select/input/form/palette-action/menu-action; grep `open_gate|allow_execution|gate.*toggle|toggle.*gate` → no output; named test #2.
- (d) **🔴 G-3 certification-display-not-actuation proof** — certification/production status rendered as-stored; grep `certify|mark_ready|approve_production|waive|risk_accept` → no output; no certification endpoint added; named test #3.
- (e) **🔴 Governance-boundary named test** — `..._contains_no_governance_mutation_gate_or_certification_control` (#4).
- (f) **🔴 M-4 whole-surface no-actuation grep CLEAN**; **no-recompute + external-AI grep CLEAN**.
- (g) **Residual honesty** — certification/pre-cert surface shows TD-UI-POSTCSS-HIGH as **CLOSED/remediated** (not an open blocker); remaining residuals as-stored; none relabeled. Data sourced from canonical governance records (R-2), not a mutation/control API.
- (h) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep beyond the already-approved vite-8 toolchain; no NEW change this phase); no new endpoint grep; no registry/route change; no governance-state persistence.
- (i) **🔴🔴 Regression (OBS-P01-1 closure)** — **clean gated `FRONTEND_VITEST_EXIT_CODE: 0`** full-suite run, frontend **≥56f/251t** all passing (no test lost; verify FULL total, not a partial run; print the sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta.
- (j) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / **institutional-not-retail, not control-panel/console wording** / brand a11y (never color alone).
- (k) **Browser served-session screenshots** — logged-in `/governance` governance-status + Gate CLOSED (inert) + certification NOT CERTIFIED / Doc 11 HELD (inert) + residuals (postcss now remediated/closed); **no governance/Gate/certify control in the UI**; logged-out `/login` block.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel — **resolve the `@rolldown` EPERM/AV file-lock so `npm ci` completes**; postcss is now remediated so a green networked audit gate is achievable; OR documented TD-W6-CI-AUDIT env-flake after substantive gates green → waiver. **An EPERM/127 or red gated run again is a finding (OBS-P01-1 is due to close here).**

---

## 5. Determination rule

A single CRITICAL, any Gate/governance/certification control present, a certification endpoint, a new dependency/endpoint/table, a red/partial gated run (OBS-P01-1 unmet), or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-007-P03 — Read-Only Audit Explorer & Refusal Reason-Code Viewer).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
