# BUILD ORDER — UI-001-P01

## Institutional Workspace Shell — Skeleton, Workspace Registry, Region Scaffolding & Routing/State Seam

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Programme:** Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P01 (first phase) · **Policy:** one phase per Build Order
**Date:** 2026-07-19
**Platform baseline (pre-phase):** v0.62.0 · Alembic head `20260717_0037` · backend **413 passed** · frontend **21 files / 67 tests** · Gate CLOSED · Waves 0–7 CLOSED
**Governing docs (collective):** `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` → `13` → `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` → `15_UI-001_IMPLEMENTATION_SPECIFICATION.md`; accepted `UI-001_ENGINEERING_DESIGN_PLAN.md`; `ITRGA_REVIEW_UI-001_DESIGN_PLAN.md` (UG-1…UG-15, R-1…R-6).
**Constitutional posture:** Governance Gate **CLOSED**. Presentation infrastructure only — no execution/actuation, no backend/API/schema/governance/ML change, no scope expansion, no regression. **Prove the frame before hanging the pictures.**
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Establish the **permanent Institutional Workspace Shell** as the single application frame (replacing legacy `TerminalLayout`), with Regions A–F scaffolded, a canonical **Workspace Registry** for all current routes, a **routing/state seam** that mounts every existing page inside the shell, and a **foundational design-token layer** — while proving **one integrated environment** and **zero regression** of the Wave-0–7 platform. This is the structural backbone; deeper navigation/panel/persistence/palette/a11y-hardening come in P02–P06.

---

## 2. Scope (build exactly this — P01 only)

1. **`InstitutionalWorkspaceShell`** under `AuthProvider → ProtectedRoute`, rendering Regions **A GlobalHeader · B NavigationDock · C WorkspaceHost · D ContextPanelHost · E ActivityDock · F OverlayHost** (scaffolded; deep behavior deferred).
2. **`WorkspaceRegistry`** — canonical metadata for **all** current protected routes (id/route/label/group/description/component, `requiresAuth:true`, `noActuation:true`); registry drives navigation (no page-specific sidebar entries outside it).
3. **`WorkspaceHost` routing/state seam** — mounts existing page components as workspace content by route match; **every current route resolves to its existing content** inside the shell.
4. **Foundational design tokens** — the semantic-color + typography token layer (prefer `frontend/src/workstation/design/tokens.css` + `theme.ts`, OBS-1).
5. **Accessibility foundation (P01 gate, R-6):** ARIA landmarks for regions; keyboard focus-transition between regions; logged-out block.
6. **Legacy `TerminalLayout` frame replaced** by the shell (no duplicate/competing frame after mount). Full retirement/cleanup is P06.

**Out of scope for P01 (defer):** full Navigation-Dock workflow behavior (P02); panel collapse/resize/layout-manager (P03); layout **persistence** to `operator_workspace_preferences` (P04 — R-4); full command palette + overlay/notifications + a11y hardening (P05); legacy retirement/cleanup (P06). Also barred (whole workstream): any new business/trading/research capability, execution/actuation control, external AI, backend/API/schema/governance/ML change.

---

## 3. Binding requirements (P01)

- **UG-1 / UG-2 / R-3 — no execution / no actuation, whole-shell.** No execution/order/broker/account/go-live/actuation control in ANY region A–F; command-palette entry (if scaffolded) is navigation/toggle only. Prove by test + browser.
- **UG-3 — backend/API/schema/governance/ML untouched.** UI-only change set. Prove by static diff/grep (no `backend/app/**`, `api/routes/**`, `alembic/**`, schema files changed).
- **UG-4 / R-1 — no regression (strong proof).** Backend **≥413** + frontend **≥21f/67t** actual operator-run totals; **every current route resolves to its existing content mounted in the shell** (route-by-route in-browser proof); auth/RBAC/audit intact.
- **UG-5 / R-2 — one integrated environment; shell is a frame, not a feature.** Single shell, no duplicate header/independent sidebar/competing layout; `test_shell_hosts_only_no_business_logic_in_shell` (no report/signal/ML/mutation/business logic in the shell package — grep/structural).
- **UG-6 / UG-7 — regions A–F + state ownership.** Shell owns nav/layout/routing/auth-display/notifications/theme/palette-visibility; no business logic in shell; no component assumes higher-level state.
- **UG-9 — design-system foundation.** Semantic color (green/red/blue/amber/purple/gray) with **meaning never by color alone**; typography L1–L5 tokens.
- **R-5 — Gate/research framing VISIBLE.** Global Header + Context Panel visibly show **Gate CLOSED / research-only** framing. Prove in browser.
- **R-6 — accessibility gate (P01).** ARIA landmarks + keyboard focus-transition + logged-out block — with browser focus-state evidence.
- **UG-12 — performance foundation.** Production build succeeds; report bundle-size delta; route transitions do not remount the global shell; no new dependency (UG-15).

---

## 4. Mandatory tests (frontend Vitest — deliver names + raw PASS lines)

```
InstitutionalWorkspaceShell renders Regions A–F (header/nav/workspace/context/activity/overlay)
WorkspaceRegistry contains every current protected route (canonical, noActuation)
WorkspaceHost mounts each existing page content by route (no page regression)
test_shell_hosts_only_no_business_logic_in_shell                     # R-2 CRITICAL
test_command_palette_navigation_only_no_business_actions             # R-2 CRITICAL (palette scaffold)
shell exposes no execution/order/broker/account/go-live/actuation controls (any region)   # R-3
shell displays Gate CLOSED / research-only framing                   # R-5
shell provides ARIA landmarks and keyboard focus-transition between regions               # R-6
protected shell route blocks logged-out access / redirects to login  # R-6
```
Backend regression must remain green (**≥413**); standing `test_broker_integration.py` + Gate-closed tests green. Frontend total must grow from 21 files (report actual).

---

## 5. Mandatory evidence (operator-run on target — Level-I; + browser screenshots)

Deliver `DELIVERY_REPORT_UI-001-P01.md` + `operator results.md` (+ screenshots), **inline**:

**(a) Build identity.** `Test-Path` new shell files (`InstitutionalWorkspaceShell`, `WorkspaceRegistry`, `WorkspaceHost`, tokens) + proof the pack is OF **UI-001-P01**; platform/version bump target stated.
**(b) Frontend test transcript.** The named Vitest tests + full frontend totals (files/tests).
**(c) Backend regression.** Full backend suite **≥413** green; broker + Gate-closed suites green (no regression from a UI change).
**(d) R-1 route-by-route no-regression.** Evidence every current route (`/`, `/live`, `/charts`, `/signals`, `/analytics`, `/intelligence`, `/investigate`, `/compare-scenarios`, `/trade-plans`, `/execution-research`, `/portfolio-research`, `/journal`, `/research-management`, `/workspace`) resolves to its existing content **inside the shell** (test + browser).
**(e) R-1 UI-only static diff.** `git diff --stat` (or equivalent) proving **no** `backend/app/**`, `api/routes/**`, `alembic/**`, or schema file changed; head `alembic current = 20260717_0037` unchanged.
**(f) R-2 shell-is-a-frame.** `test_shell_hosts_only_no_business_logic_in_shell` + `test_command_palette_navigation_only_no_business_actions` PASS; grep the shell package for business/mutation/service-compute imports → none.
**(g) R-3 whole-shell no-actuation.** grep shell components for `buy|sell|place_order|submit.*order|execute|go.?live|connect.?broker|account_id|order_ticket` → none (or only disclosed rejection-list strings) + the browser no-actuation shot.
**(h) R-5 Gate/research framing.** browser shot: shell Header + Context Panel show **Gate CLOSED / research-only**.
**(i) R-6 accessibility.** ARIA-landmark + keyboard-focus tests PASS; browser focus-state shot; logged-out block shot (protected shell route → `/login`).
**(j) BROWSER EVIDENCE (UG-13).** served-session shots: full shell (Regions A–F visible); Operations + ≥1 research workspace mounted inside the shell; no-actuation view; Gate/research framing; logged-out block.
**(k) No barred dependency (UG-15).** grep empty; state any dep change accurately (none expected).
**(l) Performance (UG-12).** `npm run build` success + bundle-size delta reported.
**(m) CI (UG-14).** Git-Bash → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (offline-`npm audit` recurs → disclose under TD-W6-CI-AUDIT; never `strict-ssl false`).

---

## 6. Acceptance criteria (P01 determination)

**Approved** requires ALL of (a)–(m); named tests + backend regression green with actual totals; **every current route mounts in the shell with no regression** (R-1) + UI-only diff; **shell is a frame not a feature** (R-2); **no actuation controls anywhere** (R-3); **Gate/research framing visible** (R-5); **accessibility gate met** (R-6); regions A–F present; design tokens present; no barred dependency; build succeeds; CI exit 0.

- A constitutional violation (any execution/actuation control or path; any Gate reach/mutation; any backend/API/schema/governance/ML change; scope expansion) ⇒ **Rejected**.
- A regression of an approved capability, a duplicate/competing frame, or business logic in the shell ⇒ **Corrective Actions Required** (fix + re-submit; ≈ CONDITIONAL) — or **Rejected** if architectural.
- Missing/sandbox-only browser shots, or a named raw proof present only as a passing test where the BO names the raw form, ⇒ **Corrective Actions Required**.
- **Approved with Observations** if every risk item is proven and only non-blocking observations remain.

**Only an Approved (or Approved-with-Observations) determination authorizes progression to UI-001-P02.** On Approved: platform/version bump as stated; head `20260717_0037` (unchanged — no migration); onboarding updated; `BUILD_ORDER_UI-001-P02.md` (Navigation Dock & workflow routing) becomes next authorizable.

---

## 7. Reminders to DA

- **Prove the frame, don't hang the pictures:** shell skeleton + registry + routing/state seam + no-regression — no P02–P06 behavior yet.
- Shell is a **frame, not a feature** — no business logic, no actuation, palette navigation-only.
- Route-by-route in-shell proof + UI-only static diff are mandatory (R-1). Accessibility is a P01 gate, not deferred (R-6). Gate/research framing stays visible (R-5).
- UI judged in the browser — served-session shots mandatory. Verify the pack is OF UI-001-P01; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
