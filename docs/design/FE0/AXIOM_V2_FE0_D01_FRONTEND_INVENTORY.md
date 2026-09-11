# FE-0 / D0-1 — Existing-Frontend Inventory (Register-True)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-D01-001 |
| Parent | AXIOM-V2-FE0-DESIGN-PLAN-001 (under AXIOM-V2-DPR-001) |
| Author | DA · 2026-09-10 |
| Method | Read-only tree walk of `frontend/` at repository head `fd8d649` (canonical custody id per OD-FE0-001 §1.2a; the DA station's local clone identifies as `9c78afa` — the measurement plane, byte-clean, U3 §G.3 state of record). Zero mutation. Counts are measured, not recalled |
| Truth posture | What IS — including debt and drift. Findings are recorded for future Build Orders, never executed here (DPR §3.1) |

## 1. Stack and build

- React 18 + TypeScript, Vite (`vite.config.ts`), React Router v7 future-flags **opted in** at `main.tsx` (`v7_startTransition`, `v7_relativeSplatPath` — BO-F-00.3 OPTION A, recorded in source).
- Test: Vitest + Testing Library. **188 test files · 975 `it/test` cases** (measured by grep census; not executed this turn).
- Entry: `main.tsx` → `BrowserRouter` → `App.tsx`.

## 2. Route census (17 routes: 1 public + 16 registered workspaces)

`App.tsx` renders `/login` (public) plus the `WORKSPACE_REGISTRY` (16 entries) inside `ProtectedRoute` → `GatedRouteElement`.

| Route | Registry id | Nav category |
|---|---|---|
| `/login` | — (public `LoginPage`) | — |
| `/` | monitor.operations | Monitor |
| `/live` | monitor.live_market | Monitor |
| `/charts` | monitor.chart_workspace | Monitor |
| `/chart` | monitor.chart_alias | Monitor |
| `/signals` | research.advisory_signals | Research |
| `/analytics` | research.analytics | Research |
| `/intelligence` | research.intelligence | Research |
| `/investigate` | investigate.signal_investigation | Investigate |
| `/compare-scenarios` | compare.scenarios | Compare |
| `/trade-plans` | plan.trade_plans | Plan |
| `/execution-research` | plan.execution_research | Plan |
| `/portfolio-research` | review.portfolio_research | Review |
| `/journal` | review.journal | Review |
| `/research-management` | review.research_management | Review |
| `/governance` | govern.governance_evidence | Govern |
| `/workspace` | settings.workspace | Settings |

Registry contract (`WorkspaceRegistrationContract`) carries per-entry: rbac (`allowedRoles`), defaultLayout, context-panel/activity-dock support, search support, keyboard shortcut, telemetryId, workspaceVersion, `featureFlag` (**null on every entry — the flag mechanism exists, unused**), and two ITRGA guard literals baked into the type: `requiresAuth: true`, `noActuation: true`.

## 3. As-implemented authentication flow

- **Pages/modules:** `pages/LoginPage.tsx` (232 L) + `LoginPage.css`; `context/AuthContext.tsx` (95 L); `auth/ProtectedRoute.tsx` (21 L); `auth/tokenStorage.ts` (20 L).
- **Flow:** form POST → `apiLogin` → `POST /api/v1/auth/login` `{username, password}` → on 200 store `tokens.access_token` + `tokens.refresh_token` in **localStorage** (`axiom_access_token` / `axiom_refresh_token`) → set operator from response. Session restore on boot: `fetchCurrentOperator` (`GET /api/v1/operator/me`) if a token exists; failure clears tokens. Logout: best-effort `POST /api/v1/auth/logout`, then local clear.
- **Backend auth surface (what IS supported)** — `app/api/routes/auth.py`: `POST /auth/login` (LoginRequest: username 1–64, password 1–128; 401 with typed detail on `AuthError`) · `POST /auth/refresh` (rotate) · `POST /auth/logout` (revoke) · `POST /auth/ws-ticket` (short-lived WS ticket; access JWT never in query string). `OperatorRead`: id/username/role/is_active/display_name/last_login_at/created_at. **NO SSO. NO password reset. NO self-registration. NO MFA/step-up at login.** No account-lockout policy found in `app/auth/service.py`.
- **Route protection:** `ProtectedRoute` (loading → "Checking operator session…", unauthenticated → redirect `/login` with `state.from`); `GatedRouteElement` checks `operator.role ∈ rbac.allowedRoles` and renders a truthful typed denial ("This workspace is not available to your operator role. This is an access restriction, not an empty result.") — an existing invariant-§B.3-conformant pattern worth ADOPT.
- **Roles:** `OperatorRole = "admin" | "operator" | "unprivileged" | string`; default `allowedRoles = ["admin","operator"]`.

## 4. API client surface

`api/client.ts` (1,880 L): **81 exported functions**, **~83 unique endpoint path shapes**, families: auth(4) · operator/me · system/health/ready/metrics · alerts · analytics · signals · intelligence (correlation/regime/scenario/portfolio-risk/signal-validation) · execution-research (simulated-runs/fills/ledger/analytics/experiments/risk-reports) · collaboration (journal/trade-plans/chart-annotations) · institutional-platform (route-inventory/rbac/api-catalogue/plugin-contracts/workspace-preferences/research-collections/tags/management/portfolio-research/operator-scope-records) · market/live (start/stop/stats/seed-history) · persistence. Plus `api/assistantClient.ts` (352 L), `drawingTools.ts`, `indicatorRegistry.ts`, `timeframes.ts`.

Mechanics: single `request<T>()`; `API_BASE = VITE_API_BASE_URL ?? ""` (relative-URL default — preview/proxy-safe); Accept/Content-Type JSON; Bearer header when `auth=true`; non-OK → `Error` with `detail` and **`.status` attached** (SURF-P03, lets callers distinguish 403 denial from transport failure); 204 → undefined.

**Zero corridor consumption:** no `live_exec` path appears anywhere in the client (re-verified; matches U3 §G.3).

## 5. Design tokens / primitives

- `workstation/design/tokens.css`: **282 custom properties**, 5-tier hierarchy (Foundation → Semantic → Component → Workspace → Runtime `.theme-light`), documented brand standard (Midnight Black `#0B0E14`, Graphite `#1A1F2C`, Electric Blue `#2563EB`, Success Green `#10B981`, Warning Amber `#F59E0B`, Critical Red `#EF4444`), WCAG 2.1 AA conformance notes in-file. `theme.ts` typed accessors (`BRAND_TOKENS`, `TYPOGRAPHY_SCALE`, …); invariant: all visual values via `var(--ix-*)`. `styles/global.css`: 277 `--ix-` references.
- `components/ui/`: **21 primitives** (Accordion, Badge, Button, Card, Collapsible, DataTable, Dialog, EmptyState, ErrorBanner, Input, Pagination, Panel, PanelActionBar, PanelHeader, Select, Skeleton, SortableHeader, StatusChip, Toast, ToastStack, Tooltip), each with co-located tests.
- Workstation platform: `workstation/` (registry, navigation, commands, search, overlays, panels, persistence, accessibility, events, workflows, governance, investigation, market, research, ai, artifacts) — the shared-shell substrate FE-U02 will evolve.

## 6. Debt and drift (truthful; recorded as findings, NOT executed)

| # | Finding | Class |
|---|---|---|
| F-1 | **LoginPage hardcodes pre-auth governance state**: literals `GATE: CLOSED`, `RESEARCH-ONLY · NON-ACTUATING`, footer `SAL-2 (Internal) · Hardware Security & Audit Trail Active` are static strings, not backend-sourced — a §B.2/§B.3 breach at the door (fabricated-looking state, even if currently true). Backend offers **no unauthenticated mode/posture read** (`/api/v1/v2/mode` requires `RequireV2ModeRead`); truthful pre-auth posture needs either a public read-only posture fact endpoint (backend finding → future BO) or an honest "unverified until sign-in" presentation. **FE-U01's central design problem** — carried into the D0-4 contract |
| F-2 | **`rememberWorkstation` checkbox is dead state**: component-local `useState`, never read by any other module, no persistence semantics. Renders a control that does nothing — §B.3-adjacent | 
| F-3 | **No LoginPage test file** (`LoginPage.tsx` has no co-located or `src/test/` coupon) — the only uncouponed page-level surface found |
| F-4 | **No automatic token rotation**: `refreshTokens()` exists in the client and `/auth/refresh` exists on the backend, but `AuthContext` never calls it — access-token expiry silently degrades to failed requests until re-login |
| F-5 | **Tokens in `localStorage`** (XSS-readable). Standing V1 posture, works, but a hardening candidate for the U01 BO's risk section (httpOnly-cookie or in-memory + rotation designs are backend-coupled → future BO) |
| F-6 | Decorative login scene (3D candlestick/particles/waves) renders synthetic market-like shapes pre-auth; currently `aria-hidden`, purely decorative, no values shown — §B.9-lawful but must stay value-free; pinned in the U01 contract |
| F-7 | `featureFlag` mechanism present on every registry entry, used by none — dormant capability, fine; note for route/flag behavior gates (§E) |
| F-8 | `/chart` is a duplicate alias of `/charts` (two registry entries, one surface family) — V1 regression scope must cover both |

All eight are **findings for future Build Orders**. Nothing was changed.
