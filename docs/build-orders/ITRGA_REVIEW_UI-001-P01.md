# ITRGA REVIEW — UI-001-P01
## Institutional Workspace Shell — Skeleton · Workspace Registry · Region Scaffolding · Routing/State Seam · Design Tokens

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P01
**Build Order under review:** `BUILD_ORDER_UI-001-P01.md` (as issued; see reconciliation memo for disposition of the truncated-spec fork)
**Evidence pack:** `DELIVERY_REPORT_UI-001-P01.md`, `operator results.md` (target PowerShell transcript, `C:\Users\Swakala\.vscode\AXIOM\axiom`, Python 3.14.6, PostgreSQL), 5 served-session screenshots.
**Determination:** ✅ **APPROVED WITH OBSERVATIONS**
**Authorizes:** `BUILD_ORDER_UI-001-P02` (Navigation Dock & workflow routing)
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity verification (done FIRST)
- Pack is **of P01**: `DELIVERY_REPORT_UI-001-P01.md` self-declares Phase P01, references `BUILD_ORDER_UI-001-P01.md`, baseline v0.62.0. Not a stale/concatenated re-attachment.
- DA disposition: **not self-approved** ("This is not an approval… does not self-authorize UI-001-P02"). Correct posture.
- Operator transcript is a genuine on-target run (env vars set: `AXIOM_DATABASE_URL` asyncpg → PostgreSQL, bootstrap admin, `AXIOM_ALLOW_INSECURE_DEV=true` for dev evidence). `Test-Path` confirms all 8 delivered artifacts exist.

---

## 1. Verification matrix (Level-I, line-by-line)

| # | Requirement | Evidence | Verdict |
|---|---|---|---|
| **Constitutional line** | Gate CLOSED, no execution/actuation anywhere (UG-1/2, R-3) | No-actuation grep on shell **source** (test files excluded) → **clean, no output**; browser shots show only Refresh (read) + Command palette (nav); header `GATE CLOSED`/`RESEARCH-ONLY`/`PRESENTATION SHELL` | **PASS (proven)** |
| **No backend/schema drift** | No backend/app, api/routes, alembic, schema, pyproject, requirements change (R-1, UG-3) | `git diff --name-only -- backend\app backend\alembic backend\tests\test_system.py backend\pyproject.toml backend\requirements.txt` → **empty output** | **PASS (proven)** |
| **Alembic head unchanged** | head `20260717_0037` | `Select-String 20260717_0037` **printed no matched line** (G-2); corroborated by empty backend/alembic diff + 413 pytest against real DB at that head | **PASS w/ Observation (G-2)** |
| **Backend regression** | ≥413 | Local CI pytest transcript: **`413 passed, 1910 warnings in 263.75s`** on target PostgreSQL after `alembic upgrade head` | **PASS (proven)** |
| **Frontend regression + growth** | grow from 21f/67t, no regression | Vitest full: **`22 files / 76 tests passed`** (+1 file / +9 tests) | **PASS (proven)** |
| **Shell is a frame, not a feature** | R-2 two CRITICAL named tests | #2 `test_command_palette_navigation_only_no_business_actions` **displayed passing** (lines 87, 123). #1 `test_shell_hosts_only_no_business_logic_in_shell` **listed + file reports 9/9** but **name not displayed** by Vitest's truncated reporter (G-1) | **PASS w/ Observation (G-1)** |
| **Regions A–F rendered (browser)** | UG-6, R-1 | Shot 01 (`/`): A Header + B Nav Dock + C WorkspaceHost(Operations) + D Context Panel visibly rendered; E/F scaffolded per report | **PASS (A–D proven in browser; E/F scaffold)** |
| **Every route mounts in shell** | R-1 route-by-route | Registry lists 15 routes; browser shows `/`, `/signals`, `/portfolio-research` mounted in-shell; `WorkspaceHost mounts each existing page content by route (no page regression)` test passing | **PASS (proven for sampled routes)** |
| **Gate/research framing visible** | R-5 | Header badges + Context-Panel GOVERNANCE (GATE CLOSED / RESEARCH-ONLY) + Portfolio "Hypothetical research only" + Signals "Research advisory only" disclaimers | **PASS (proven)** |
| **Accessibility gate** | R-6 ARIA landmarks + keyboard focus + logged-out block | `shell provides ARIA landmarks and keyboard focus-transition between regions` test passing; Alt+1–4 focus + Ctrl+K palette scaffold; **logged-out `/login` shot shows NO shell chrome** (block confirmed) | **PASS (proven)** |
| **Design tokens present** | UG-9 | `tokens.css` + `theme.ts` created (semantic color/typography/spacing/sizing/focus/border/surface); F-3 partial (see Observations) | **PASS w/ Observation (F-3)** |
| **Registry extensibility** | §4.1 hard-line (defeats §12 if hardcoded) | `App.tsx: WORKSPACE_REGISTRY.map(({ route, Component }) => ...)` — routing is **data-driven off the registry**, widenable to 14-field contract without rewrite | **PASS (proven) — hard-line satisfied** |
| **No barred dependency** | UG-15 | `added 0` net deps; build clean; no LLM/broker/compiled dep | **PASS (proven)** |
| **Build success + bundle delta** | perf foundation | Build OK; CSS 22.85→28.28 kB (+5.43), JS 435.70→440.77 kB (+5.07) — proportionate for a shell skeleton | **PASS (proven)** |
| **Local CI** | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` **solely** from offline `npm audit` (`getaddrinfo ENOTFOUND registry.npmjs.org`) **AFTER** alembic/ruff/pytest-413/frontend-deps all green = **TD-W6-CI-AUDIT** env-class | **WAIVED by operator** (per standing precedent) |

---

## 2. Observations (non-blocking; carried to P02 intake)

**Evidence-completeness (R7) — close with a one-line re-run at P02 intake:**
- **OBS-P01-1 (G-1):** Resubmit a Vitest run that **displays `test_shell_hosts_only_no_business_logic_in_shell` passing by name** (e.g. `vitest run --reporter=verbose` or `-t "test_shell_hosts_only_no_business_logic_in_shell"`). The file-level `9 tests passed` + DA listing is corroborating but does not individually display this CRITICAL R-2 test.
- **OBS-P01-2 (G-2):** Resubmit `alembic current` output (or the `Select-String 20260717_0037` matched line) showing the head string. The empty backend/alembic diff already corroborates no-migration.

**Spec-conformance carried forward (per fairness rule §4.1 of `ITRGA_SPEC_RECONCILIATION_UI-001_DOC15_FULL.md` — DA built against a truncated spec in good faith; foundation proven extensible ⇒ Observation, not Corrective):**
- **OBS-P01-3 (F-1):** Widen the `WorkspaceRegistry` entry type to the **14-field canonical Workspace Registration Contract** (Doc 15 Part V §5): Identifier, Display Name, Navigation Category, Route, Icon, RBAC, Default Layout, Context-Panel Support, Activity-Dock Support, Search Support, Keyboard Shortcut, Telemetry Id, Version, Optional Feature Flag. Retain the ITRGA guard fields `requiresAuth` + `noActuation:true` on top. **Bind to P02** (Navigation is registry-driven).
- **OBS-P01-4 (F-2):** Scaffold Region F as the **three-layer overlay family** (Overlay · Global Dialog · Notification) per Doc 15 Part IV §5 (containers only, no actuation). **Bind to P05** (Overlay/Notifications/Palette).
- **OBS-P01-5 (F-3):** Complete the token architecture toward Doc 15 Part VIII §4's 11 categories and §5's 18 semantic color roles — priority on the AXIOM roles **Governance / Research / Execution Research / Intelligence** that carry constitutional framing; enforce "no component defines independent color." **Bind across P02–P05.**

---

## 3. Determination & rationale
**APPROVED WITH OBSERVATIONS.** Every *substantive* acceptance condition is positively proven on target: constitutional line held (Gate CLOSED, no-actuation source grep clean, browser confirms), zero regression (backend 413, frontend 22f/76t up from 21f/67t), no backend/schema/API/dependency drift (empty diff), data-driven registry that satisfies the extensibility hard-line, browser-judged regions A–D + Gate/research framing + logged-out block + accessibility test. The two R7 gaps (G-1 named-test display, G-2 head-match line) are **proof-display gaps corroborated by independent evidence**, not substantive failures — dispositioned as Observations to close with trivial re-runs at P02 intake. The CI exit-1 is the standing TD-W6-CI-AUDIT env-flake occurring after all substantive gates green — **waived by operator**. F-1/F-2/F-3 are forward-carried under the truncated-spec fairness rule because the delivered foundation is provably extensible without a contract-breaking rewrite.

Per the UI-Transformation vocabulary, **Approved with Observations authorizes progression.** → **`BUILD_ORDER_UI-001-P02` is authorized** (fold OBS-P01-3 as a binding P02 requirement; require OBS-P01-1/2 closure at P02 intake).

Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

*We don't guess. We prove.*
