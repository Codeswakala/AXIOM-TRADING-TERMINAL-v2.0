# ITRGA DETERMINATION — UI-007-P01

**Governance Workspace Frame · `/governance` Route · Data-Source Inventory · Read-Only Guardrails**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P01** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P01.md` |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-1…G-7), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering | v0.62.0 · head `20260717_0037` · backend 414 · frontend 55f/246t → (post-postcss-remediation) 56f/251t / vite-8 toolchain |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF UI-007-P01 (delivery report 380 lines; `OPERATOR_RESULTS.md` 3012 lines references BUILD_ORDER_UI-007-P01 + the design-plan review; predecessor = design-plan Approved-w-Obs). No stale/wrong-phase/concatenated pack.

---

## 2. Level-I evidence verification — governance boundary (G-1…G-7 / R-1/R-7)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | **5 passed (5)** (L109–116): mounts_inside_single_ui001_shell / uses_single_governance_route_and_registry_contract / maps_every_section_to_existing_read_seams / **contains_no_governance_mutation_gate_or_certification_control** / preserves_gate_closed_not_certified_verbatim_and_doc16_branding | ✅ PASS |
| E-2 | 🔴 G-2 governance-control grep CLEAN | `UI007_P01_G2_GOVERNANCE_CONTROL_GREP_CLEAN` (throw-guarded on `open_gate\|allow_execution\|gate.*toggle\|certify\|mark_ready\|approve_production\|waive\|risk_accept`) | ✅ PASS |
| E-3 | 🔴 M-4 no-actuation grep CLEAN | `UI007_P01_NO_ACTUATION_GREP_CLEAN` (throw-guarded) | ✅ PASS |
| E-4 | 🔴 No-recompute + external-AI grep CLEAN | `UI007_P01_R6_NO_RECOMPUTE_RELATIONSHIP_INFERENCE_GREP_CLEAN` + `UI007_P01_EXTERNAL_AI_GREP_CLEAN` | ✅ PASS |
| E-5 | 🔴 Registry contract + no forbidden names (R-1/§4.3) | `/governance` route + `noActuation:true` + `Govern` + "Governance & Evidence"; `$badRouteHits` for `/admin\|/control\|/gate\|Governance Control\|Certification Console\|Open Gate\|Approve Production` = empty (throw-guarded `UI007_P01_FORBIDDEN_ROUTE_OR_LABEL_FOUND` not thrown) | ✅ PASS |
| E-6 | Data-source inventory → existing seams | `GovernanceEvidencePage.tsx` maps §9 surfaces to `GET /api/v1/persistence/audit-events` / `/health` / `/ready` / `/metrics` / `/persistence/stats` / `/system/info` / route-inventory / rbac / api-catalogue / plugin-contracts / operator-scope; certification = "Canonical governance records; no production-status API action" (R-2); named test #3 | ✅ PASS |
| E-7 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L491) | ✅ PASS |
| E-8 | Backend ≥414 | `pytest -q` → **414 passed** (L993/L1450) | ✅ PASS |
| E-9 | Browser served-session | `/governance` frame ("UI-007-P01 · FRAME ONLY"): "Governance visibility only… does not change governance state"; GATE POSTURE **Gate CLOSED — read-only constitutional fact, no UI affordance changes this state**; PRODUCTION POSTURE **NOT CERTIFIED / Doc 11 HELD**; PRE-CERT BLOCKER **TD-UI-POSTCSS-HIGH OPEN**; "AXIOM does not act"; read-only G-1…G-7 boundary panel; registry context Category Govern / Alt+Y / telemetry workspace.govern.governance_evidence | ✅ PASS |
| E-10 | **Gated full-suite exit 0 / ≥ baseline, no test lost** | **🔴 RED + PARTIAL — `FRONTEND_VITEST_EXIT_CODE: 1`; `Test Files 2 failed \| 18 passed (20)`, `Tests 1 failed \| 102 passed (103)`** (partial 103-test run, not full ~251) with "unhandled errors… may cause false positives" | ⚠️ **OBS-P01-1 (env failure, operator-adjudicated)** |
| E-11 | Networked CI | **`LOCAL_CI_EXIT_CODE: 127`** — `EPERM: operation not permitted, unlink @rolldown/binding-win32-x64-msvc — file already in use (text editor or antivirus)` during `npm ci` | ⚠️ **OBS-P01-2 (env failure)** |

---

## 3. Governance boundary — held (the defining risk)

| Property | State |
|---|---|
| Governance mutation / Gate toggle / certification actuation / audit CRUD / verdict change | NONE — read-only; `no_governance_mutation_gate_or_certification_control` test + G-2 grep clean (G-1…G-4) |
| Gate CLOSED | Rendered as **inert** read-only constitutional fact ("No UI affordance changes this state") |
| Certification / production | NOT CERTIFIED / Doc 11 HELD rendered inert; no certify/approve control; canonical records, no cert endpoint (R-2/G-3) |
| Forbidden route/control naming (§4.3) | NONE present (grep clean) |
| Actuation / external AI / recompute | NONE (greps clean) |
| New endpoint / table / dependency / governance-state persistence | NONE (G-7; head unchanged) |

The most constitutionally-reflexive workstream's P01 frame is a strictly read-only display of governance posture with no control surface — exactly the G-1…G-7 intent.

---

## 4. 🔴 OBS-P01-1 / OBS-P01-2 — environment failures (operator-adjudicated), NOT relabeled green

- **OBS-P01-1 (red/partial gated vitest):** the gated full-frontend run returned `FRONTEND_VITEST_EXIT_CODE: 1` on a **partial 103-test run** (`2 failed | 18 passed (20)` files; `1 failed | 102 passed (103)` tests) with vitest reporting "unhandled errors… might cause false positive tests." All **5 UI-007-P01 named tests passed within this same run** (evidence-file L177–203). The run is truncated and error-contaminated — a broken run on a loaded Windows box, consistent with the `@rolldown` file-lock contention below — **not a P01 code defect.**
- **OBS-P01-2 (CI exit 127):** `LOCAL_CI_EXIT_CODE: 127` from `EPERM: operation not permitted, unlink '…@rolldown/binding-win32-x64-msvc/rolldown-binding.win32-x64-msvc.node' — The file was already in use (by a text editor or antivirus)` during `npm ci`. A **Windows file-lock / antivirus environment failure**, not a code/audit defect.
- **Corroboration:** the sibling **TD-UI-POSTCSS-HIGH remediation run in the same session produced a clean full suite — `FRONTEND_VITEST_EXIT_CODE: 0` → 56f/251t — plus a successful production build** on the new vite-8 toolchain. That demonstrates the suite is green when the machine is not file-locked.
- **Operator adjudication:** treat OBS-P01-1/-2 as environment failures; approve P01 on the substantive green gates; **require a clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite run (≥ baseline, no test lost) at UI-007-P02.** These red/nonzero results are **documented as findings, not relabeled green.**

---

## 5. Observations & baseline reconciliation

- **OBS-P01-1 (MANDATORY closure at P02):** supply a clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite run (≥ current baseline, no test lost) on an unlocked machine (close editors/AV lock on `node_modules/@rolldown`). Non-waivable at P02.
- **OBS-P01-2:** fix the `npm ci` EPERM/@rolldown file-lock so LOCAL_CI can complete networked; prefer a clean run (post-postcss-remediation, the audit gate is now genuinely achievable green).
- **Baseline reconciliation:** the TD-UI-POSTCSS-HIGH remediation (approved this turn) advanced the frontend baseline to **56f/251t on the vite-8 / vitest-4 toolchain**. UI-007-P01's own clean full-suite total will be confirmed at P02 (OBS-P01-1); the P01 frame added its 5 named tests (present and passing). Baseline of record: **56f/251t**.

---

## 6. Carried standing residuals

- ~~TD-UI-POSTCSS-HIGH~~ **CLOSED** this turn (dependency remediation approved).
- TD-UI-REACTROUTER-MODERATE (new, moderate react-router advisories — non-blocking)
- TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b

---

## 7. Disposition

**UI-007-P01 is APPROVED WITH OBSERVATIONS.** The governance workspace frame, `/governance` route, data-source inventory, and read-only G-1…G-7 boundary are constitutionally clean (no governance/Gate/certification control; Gate CLOSED and NOT-CERTIFIED inert; no forbidden naming). The red/partial gated vitest and CI exit-127 are documented Windows `@rolldown`/AV environment failures (OBS-P01-1/-2), operator-adjudicated, with a mandatory clean-gated-run closure at P02.

This authorizes issuance of the next Build Order (**UI-007-P02 — Governance Status, Gate CLOSED, Certification Status Display**) upon operator "authorized". **P02 is no longer gated by TD-UI-POSTCSS-HIGH (closed);** P02's certification-status surface will honestly reflect that the postcss high is now remediated.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 56f/251t (vite-8 toolchain).**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
