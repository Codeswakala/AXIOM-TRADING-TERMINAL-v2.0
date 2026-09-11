# DELIVERY REPORT — UI-001-P01

## Institutional Workspace Shell — Skeleton, Workspace Registry, Region Scaffolding & Routing/State Seam

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P01 |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P01.md` |
| Baseline platform | v0.62.0 |
| Alembic head | `20260717_0037` unchanged |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / browser evidence / ITRGA review |

---

## 1. Executive summary

UI-001-P01 has been implemented as the first Institutional UI Transformation slice. It establishes the permanent institutional shell skeleton, canonical workspace registry, route-hosting seam, foundational design tokens, ARIA landmarks, keyboard focus transitions, and a navigation-only command palette scaffold.

The active protected application frame now uses:

```text
InstitutionalWorkspaceShell
```

instead of the legacy active `TerminalLayout` frame.

The shell renders Regions A–F:

```text
A — Global Header
B — Navigation Dock
C — Primary Workspace / WorkspaceHost
D — Context Panel
E — Activity Dock
F — Overlay Layer
```

Every current protected route is represented in `WorkspaceRegistry` and mounts existing page content through the shell.

UI-001-P01 is presentation infrastructure only. No backend business logic, API contract, schema, governance behavior, ML workflow, trading/research capability, execution path, external AI, or dependency was added.

The Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Institutional shell

Created:

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx
frontend/src/workstation/components/InstitutionalWorkspaceShell.css
```

The shell includes:

- Global Header with platform identity, active workspace title, operator controls;
- Gate CLOSED / Research-only framing in the header;
- workflow Navigation Dock;
- Primary Workspace region hosting existing routes;
- Context Panel with workspace context and governance framing;
- Activity Dock scaffold;
- Overlay Layer for command palette scaffold.

### B. WorkspaceHost

Created:

```text
frontend/src/workstation/components/WorkspaceHost.tsx
```

The host wraps the current route's existing content inside the Primary Workspace region and exposes workspace metadata through the active route.

### C. WorkspaceRegistry

Created:

```text
frontend/src/workstation/registry/workspaceRegistry.tsx
```

The registry contains canonical metadata for all current protected routes:

```text
/
/live
/charts
/chart
/signals
/analytics
/intelligence
/investigate
/compare-scenarios
/trade-plans
/execution-research
/portfolio-research
/journal
/research-management
/workspace
```

Every registry entry declares:

```text
requiresAuth: true
noActuation: true
```

### D. Design token foundation

Created:

```text
frontend/src/workstation/design/tokens.css
frontend/src/workstation/design/theme.ts
```

The token layer establishes semantic colors, typography scale, spacing, region sizing, focus, border, and surface tokens for the institutional shell.

### E. App routing integration

Modified:

```text
frontend/src/App.tsx
```

The protected route frame now uses:

```text
<InstitutionalWorkspaceShell />
```

and generates protected workspace routes from:

```text
WORKSPACE_REGISTRY
```

The legacy `TerminalLayout` remains as a file for later P06 cleanup, but it is no longer the active protected frame.

### F. Tests

Created:

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.test.tsx
```

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| UG-1 / UG-2 no execution / no scope expansion | Preserved. Shell exposes no execution/order/broker/account/go-live controls and adds no business capability. |
| UG-3 backend/API/schema/governance/ML untouched | Preserved. Implementation is frontend shell/docs only. No backend/schema/API/ML code was changed for P01. |
| UG-4 no regression | Preserved locally. Backend 413 passed; frontend 22 files / 76 tests passed; build clean. |
| UG-5 one integrated environment | Implemented. Protected app frame now uses `InstitutionalWorkspaceShell`; route metadata is centralized in `WorkspaceRegistry`. |
| UG-6 Regions A–F | Implemented and tested. Header, Navigation Dock, WorkspaceHost, Context Panel, Activity Dock, Overlay Layer render. |
| UG-7 state ownership | Implemented as shell-level navigation/layout/overlay state only. Workspaces retain business/research state. |
| UG-9 design tokens | Implemented initial semantic token layer and typography token foundation. |
| UG-10 accessibility foundation | Implemented/tested ARIA landmarks, protected logged-out block, command palette focus, Alt+1–4 focus transitions. |
| UG-12 performance foundation | Build succeeds; route transitions keep shell frame active; no new dependency. |
| UG-13 browser evidence | Evidence pack requires served screenshots for regions, route hosting, no actuation, command palette, focus, logged-out block. |
| UG-15 no unspiked dependency | Preserved. No dependency added. |

---

## 4. Files changed or added for UI-001-P01

### Frontend created

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx
frontend/src/workstation/components/InstitutionalWorkspaceShell.css
frontend/src/workstation/components/InstitutionalWorkspaceShell.test.tsx
frontend/src/workstation/components/WorkspaceHost.tsx
frontend/src/workstation/registry/workspaceRegistry.tsx
frontend/src/workstation/design/tokens.css
frontend/src/workstation/design/theme.ts
```

### Frontend modified

```text
frontend/src/App.tsx
```

### Docs created/updated

```text
docs/build-orders/BUILD_ORDER_UI-001-P01.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-001-P01.md
docs/evidence/UI-001-P01_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-001-P01.md
```

No backend application, API route, Alembic/schema, ML, or governance behavior implementation files were changed for UI-001-P01.

---

## 5. Mandatory tests implemented

Frontend tests in:

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.test.tsx
```

Implemented named tests:

```text
InstitutionalWorkspaceShell renders Regions A–F (header/nav/workspace/context/activity/overlay)
WorkspaceRegistry contains every current protected route (canonical, noActuation)
WorkspaceHost mounts each existing page content by route (no page regression)
test_shell_hosts_only_no_business_logic_in_shell
test_command_palette_navigation_only_no_business_actions
shell exposes no execution/order/broker/account/go-live/actuation controls (any region)
shell displays Gate CLOSED / research-only framing
shell provides ARIA landmarks and keyboard focus-transition between regions
protected shell route blocks logged-out access / redirects to login
```

---

## 6. Local validation performed by DA

### Frontend named tests

```bash
cd /home/user/axiom/frontend
npm test -- InstitutionalWorkspaceShell.test.tsx
```

Result:

```text
1 file / 9 tests passed
```

### Frontend full suite

```bash
cd /home/user/axiom/frontend
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 22 files / 76 tests passed
TypeScript: clean
Build: successful
```

Build output after P01:

```text
dist/assets/index-COqdn7T8.css   28.28 kB │ gzip: 5.50 kB
dist/assets/index-L-kdOvrT.js   440.77 kB │ gzip: 129.12 kB
```

Prior W7-U08 local build reference:

```text
CSS ≈ 22.85 kB
JS  ≈ 435.70 kB
```

Approximate raw delta:

```text
CSS +5.43 kB
JS  +5.07 kB
```

### Backend regression

```bash
cd /home/user/axiom/backend
ruff check .
pytest tests/test_broker_integration.py tests/test_wave7_closeout.py -q
pytest -q
```

Results:

```text
Ruff: All checks passed
Broker + closeout targeted: 12 passed, 1 warning
Backend full suite: 413 passed, 1 warning
```

---

## 7. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/UI-001-P01_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell/browser commands for:

1. build identity;
2. UI-only static diff and unchanged Alembic head;
3. named frontend tests;
4. full frontend regression/build;
5. backend regression/broker/Gate tests;
6. shell-is-frame grep;
7. no-actuation grep;
8. served browser screenshots for shell regions A–F;
9. route-by-route in-shell checks;
10. command palette and keyboard focus evidence;
11. logged-out block;
12. full local CI.

---

## 8. Deferred / explicitly not implemented

Deferred to later UI-001 phases:

- full Navigation Dock workflow behavior;
- panel collapse/resize/layout manager;
- persistence to `operator_workspace_preferences`;
- full command palette behavior;
- overlay notifications;
- advanced accessibility hardening;
- legacy layout cleanup/retirement beyond replacing active frame.

Explicitly not implemented:

- backend business logic change;
- API/schema/governance/ML change;
- new table or migration;
- new dependency;
- new trading/research capability;
- execution/order/broker/account/Gate controls;
- external AI/LLM;
- production certification.

---

## 9. DA disposition

UI-001-P01 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve UI-001-P01, does not self-authorize UI-001-P02, does not certify production readiness, does not expand platform capability, and does not modify the Governance Gate.

Next required step: operator runs `docs/evidence/UI-001-P01_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/browser environment and submits transcript + screenshots to ITRGA for review.

---

**End of DELIVERY_REPORT_UI-001-P01.md**
