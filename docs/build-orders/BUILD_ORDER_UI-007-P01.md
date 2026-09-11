# BUILD ORDER — UI-007-P01

**Governance Workspace Frame · `/governance` Route · Data-Source Inventory · Read-Only Guardrails**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P01** |
| Design-plan review | `docs/ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` — ✅ Approved w/ Obs + R-1…R-8 |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-1…G-7)/§8 (P01), Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **55f/246t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Establish the UI-007 Governance & Evidence Workspace **frame** on a single protected **`/governance`** route (UI-001/UI-002 shell), prove **every §9 governance surface maps to an existing read seam**, and lay down the **read-only governance boundary (G-1…G-7)** BEFORE any governance-status/audit/evidence display work. **This phase is strictly READ-ONLY, display-only; it exposes NO governance control.**

**IN scope:**
1. Single protected `/governance` route (R-1) under the 14-field Workspace Registry contract, `requiresAuth:true` + `noActuation:true`, `Govern` category; display name "Governance & Evidence".
2. Governance workspace frame + **data-source inventory** for the Doc 12 §9 surfaces (governance status · audit events · certification/readiness · platform health · evidence · validation summaries · version/API/route/plugin posture), each mapped to its existing read seam.
3. **Read-only G-1…G-7 guardrail framing** — GATE CLOSED (inert) · Production NOT CERTIFIED / Doc 11 HELD (inert) · TD-UI-POSTCSS-HIGH shown as open non-waivable pre-cert blocker · "AXIOM does not act."

**OUT of scope (do NOT build):**
- Governance-status/Gate/certification display (P02), audit explorer (P03), evidence/validation (P04), health/readiness/version (P05), completion (P06).
- **Any governance control** — no create/update/delete/approve governance status, no waive/accept-risk, no certify/mark-ready/approve-production, no open/close/toggle Gate, no audit create/edit/delete/redact/replay, no verdict mutation (G-1…G-4).
- Any actuation / order / broker / account / live / execute / Gate path (G-6/M-4); external AI/LLM; recompute/inference/reclassification (G-6).
- Any new backend endpoint / service / table / migration / dependency / governance-state persistence (G-7); saved-view persistence (in-memory only).
- Forbidden route/control naming (§4.3): `/admin` `/control` `/gate` `/certification-control` `Governance Control` `Open Gate` `Approve Production` etc.

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Single protected `/governance` route; **14-field registry contract unchanged** (`requiresAuth:true`+`noActuation:true`); no duplicate navigation; §4.3 forbidden naming binding. If the contract cannot be preserved cleanly, fall back to enhancing an existing surface (no new route) and state so.
- **R-2** — Certification shown as **canonical read-only posture**; **no certification endpoint**.
- **R-7 (SPINE)** — read-only governance boundary; mandatory named test `test_ui007_governance_workspace_contains_no_governance_mutation_gate_or_certification_control`; G-2 grep (`open_gate|allow_execution|gate.*toggle|certify|mark_ready|approve_production|waive|risk_accept`) + M-4 no-actuation grep + no-recompute/external-AI grep.
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.
- **R-5 note** — the TD-UI-POSTCSS-HIGH remediation Build Order (issued in parallel) is due before **P02**; P01 displays the residual honestly and introduces no dependency change.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui007_governance_workspace_mounts_inside_single_ui001_shell`
2. `test_ui007_governance_workspace_uses_single_governance_route_and_registry_contract`
3. `test_ui007_governance_workspace_maps_every_section_to_existing_read_seams`
4. `test_ui007_governance_workspace_contains_no_governance_mutation_gate_or_certification_control`
5. `test_ui007_governance_workspace_preserves_gate_closed_not_certified_verbatim_and_doc16_branding`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-007-P01.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 Read-only governance-boundary proof (G-1…G-4)** — no governance-mutation / Gate-toggle / certification-actuation / audit-mutation control present (grep + named test #4); Gate CLOSED and NOT-CERTIFIED rendered inert (no button/switch/form/palette action).
- (d) **🔴 G-2 governance-control grep CLEAN** — `open_gate|allow_execution|gate.*toggle|toggle.*gate|certify|mark_ready|approve_production|waive|risk_accept` → no output.
- (e) **🔴 M-4 whole-surface no-actuation grep CLEAN** — `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (f) **🔴 No-recompute + external-AI grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|inferRelationship|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` + `openai|gpt|external_llm|llm_summary|ai_summary`.
- (g) **Data-source inventory proof** — each §9 surface maps to an existing read seam (source grep + named test #3): governance status / `GET /api/v1/persistence/audit-events` / health `/health` `/ready` / metrics / persistence-stats / system-info / route-inventory / rbac / api-catalogue / plugin-contracts / operator-scope; certification = canonical read-only (no endpoint).
- (h) **🔴 Registry contract proof (R-1)** — `/governance` present with 14-field contract + `requiresAuth:true` + `noActuation:true`; no forbidden route names (§4.3); no duplicate navigation; named test #2.
- (i) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no governance-state persistence**; registry change limited to the single approved `/governance` entry (justified by R-1).
- (j) **Regression** — frontend Vitest **≥55f/246t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (k) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / **institutional-not-retail, and specifically not control-panel/console wording** / brand a11y (never color alone).
- (l) **Browser served-session screenshots** — logged-in `/governance` frame with the data-source inventory + GATE CLOSED (inert) + Production NOT CERTIFIED / Doc 11 HELD (inert) + TD-UI-POSTCSS-HIGH open pre-cert blocker; **no governance/Gate/certify control in the UI**; GATE CLOSED / RESEARCH-ONLY framing; logged-out `/login` block.
- (m) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR TD-W6-CI-AUDIT env-flake waiver after substantive gates green; OR `LOCAL_CI_EXIT_CODE: 1` solely the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding.**

---

## 5. Determination rule

A single CRITICAL, any governance/Gate/certification control present in this read-only phase, a new backend endpoint/table/dependency, a forbidden route name, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-007-P02 — Governance Status, Gate CLOSED, Certification Status Display) — which is additionally gated on the TD-UI-POSTCSS-HIGH remediation Build Order per R-5.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
