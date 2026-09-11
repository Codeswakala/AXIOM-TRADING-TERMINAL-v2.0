# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-010-P01`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-61 — UI-010 Design Plan **APPROVED WITH OBSERVATIONS** (O-010-01 — responsive table sticky-header z-index detail, non-blocking)
**Phase:** UI-010-P01 — Accessibility Foundation & Semantic Audit
**Governing Design Plan:** `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (Approved per D-61, §10 Proposed P01)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010)
**Preceding Milestone:** UI-009 COMPLETE (D-60) / UI-010 Design Plan (D-61) — 113 suites / 485 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 113/485 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P01 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-010-P01` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-61 — UI-010 Design Plan APPROVED WITH OBSERVATIONS (O-010-01) |
| Preceding Milestone | UI-009 COMPLETE (D-60) — 113/485 + 414 |
| Next Milestone | UI-010-P01 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-010) |
| Risk Level | Low (accessibility foundation — semantic audit + skip link, no business logic) |

---

## 2. PHASE OBJECTIVE

Establish the **accessibility foundation** for AXIOM by implementing **skip-link landmark navigation** and a **comprehensive automated semantic audit harness** that verifies ARIA landmark completeness, heading hierarchy, and focusability across the harmonized workstation (113/485). This phase is **semantic foundation only, not responsive, feedback, or whole-surface audit.**

This phase **closes the gap** identified in UI-010 Design Plan §6: *Missing top-level skip links (`#main-content`) for immediate keyboard bypass of Regions A/B* and *Incomplete landmark/heading inventory* — per WCAG 2.4.1 (Bypass Blocks) and 1.3.1 (Info & Relationships).

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **`SkipLink` — `SkipLink.tsx` + `SkipLink.css`** | Landmark bypass link: renders as first focusable element in `InstitutionalWorkspaceShell.tsx` Region A, visually hidden until focused (`position: absolute; left: -9999px` → `:focus { left: var(--ix-space-4); top: var(--ix-space-2); }`), `href="#main-content"`, `onClick` smoothly scrolls/focuses `#main-content` `main` landmark, `aria-label="Skip to main content"` |
| 2 | **Shell Region A Landmark Integration** | Ensure `InstitutionalWorkspaceShell.tsx` Regions A–F have explicit ARIA landmarks: `Region A` (`<header role="banner">` or `<div role="banner">`), `Region B` (`<nav role="navigation" aria-label="Primary">`), `Region C` (`<main id="main-content" role="main" tabindex="-1">`), `Region D` (`<aside role="complementary" aria-label="Context">`), `Region E` (`<section role="region" aria-label="Activity">`), `Region F` (overlay layer — no landmark needed, portaled overlays `aria-modal` as appropriate) |
| 3 | **Semantic Audit Harness — `accessibilityAudit.test.ts`** | Automated test suite querying all 113 test suites' rendered shells/pages for: (a) landmark completeness (exactly one `banner`, one `main`, one `navigation` primary, at least one `complementary` when Context Panel present), (b) heading hierarchy `h1` → `h2` → `h3` unbroken (no skipped levels, at least one `h1` per page), (c) all interactive elements are focusable via `Tab` (`getByRole` `button`/`link`/`combobox`/`textbox` etc. focusable), (d) `SkipLink` `href="#main-content"` points to existing `#main-content` |
| 4 | **Token Consumption Enforcement** | `SkipLink` via `var(--ix-*)` (`--ix-color-focus` `#8CC2FF`, `--ix-space-*`, `--ix-bg-surface`) — 0 ad-hoc hex / 0 hardcoded spacing in `workstation/accessibility/` |
| 5 | **Style Safety** | 0 `dangerouslySetInnerHTML` / 0 `eval` / 0 raw `<script>` in accessibility module |
| 6 | **Evidence Package** | Logs committed to `docs/evidence/ui010/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Responsive breakpoint tokens (`--ix-breakpoint-*`), panel collapse reflow at 1280/1024 | **UI-010-P02** scope |
| 2 | Feedback state standardization (`EmptyState` primitive, Loading/Empty/Error/Toast harmonization across 7 workspaces) | P03 scope |
| 3 | Keyboard shortcut manager, global `Ctrl+K`, focus trap validation beyond `SkipLink`, focus restoration | P04 scope — `SkipLink` focus itself is P01, global shortcut matrix is P04 |
| 4 | Screen-reader live regions (`RouteAnnouncer` `aria-live`), `prefers-contrast` high-contrast, `prefers-reduced-motion` | P05 scope |
| 5 | Whole-surface WCAG audit (axe full scan across all 113 suites) | **P06** scope — P01 is foundation audit sample, not whole-surface |
| 6 | `EmptyState` / `RouteAnnouncer` / high-contrast theme components | P03/P05 scope |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P01 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Accessibility Foundation Architecture (Per Design Plan §10)

- **Location (Recommended):** `frontend/src/workstation/accessibility/` — new module `SkipLink.tsx`, `SkipLink.css`, `accessibilityAudit.test.ts` — DA may alternatively place `SkipLink` in `frontend/src/components/ui/` if reusing library path, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **SkipLink Behavior:** First child of `InstitutionalWorkspaceShell.tsx` `Region A` (or `body` top). Visually hidden (`clip` or `left: -9999px`) until `:focus` → visible `position: fixed` top `var(--ix-space-2)` left `var(--ix-space-4)` with `background: var(--ix-bg-surface-raised)`, `border: var(--ix-border-subtle)`, `outline: 2px solid var(--ix-color-focus)` `#8CC2FF`. `href="#main-content"` must match `<main id="main-content" tabindex="-1">` in Region C. On `click`, prevent default, `document.getElementById('main-content')?.focus()` (with `tabindex="-1"` to allow programmatic focus without `Tab` stop).
- **Landmark Integration:** `InstitutionalWorkspaceShell.tsx` must render explicit ARIA roles: `banner` (Region A), `navigation` (Region B), `main#main-content` (Region C), `complementary` (Region D when present), `region` + `aria-label` (Region E when present). No landmark needed for Region F (portaled overlays have `aria-modal`). All landmarks via semantic HTML5 (`<header>`, `<nav>`, `<main>`, `<aside>`, `<section>`) or equivalent `role`.
- **Audit Harness:** `accessibilityAudit.test.ts` uses `@testing-library/react` + `vitest` + `axe-core` (optional) to render `InstitutionalWorkspaceShell` + representative workspace pages (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `GovernanceEvidencePage.tsx` etc.) and asserts: `getByRole('banner')` exists, `getByRole('navigation')` exists, `getByRole('main')` exists with `id="main-content"`, all `h1`→`h2`→`h3` hierarchy via `heading` queries, and `SkipLink` `href="#main-content"` points to existing element. Must run in `jsdom` with `vitest`.
- **Token Consumption:** Every visual value (focus ring `var(--ix-color-focus)`, background `var(--ix-bg-surface-raised)`, spacing `var(--ix-space-*)`) **must reference P01 5-tier tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` spacing outside `var(--ix-space-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/accessibility/` or `components/ui/`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; `SkipLink` is presentation link, not business logic.

### 4.3 Interaction Contracts

| Component | Contract |
|-----------|----------|
| `SkipLink` | `href="#main-content"` (required) + `aria-label="Skip to main content"` + `onClick?` (optional smooth focus) — visually hidden until `:focus` — first `Tab` stop on page load |
| `InstitutionalWorkspaceShell.tsx` Regions | `Region A`: `<header role="banner">` or `<div role="banner">` contains `SkipLink` as first child; `Region B`: `<nav role="navigation" aria-label="Primary">`; `Region C`: `<main id="main-content" role="main" tabindex="-1">`; `Region D`: `<aside role="complementary" aria-label="Context">`; `Region E`: `<section role="region" aria-label="Activity">` |
| `accessibilityAudit.test.ts` | No props — renders shell + pages and asserts landmark count + heading order + SkipLink target existence + focusability via `getByRole` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in accessibility module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/accessibility/` (or chosen path) — 0 matches |
| 4 | No `eval` / `new Function` in accessibility module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/accessibility/` (or `components/ui/`) — 0 matches (all colors via `var(--ix-*)`) |
| 7 | No credential exposure via focus logging (no `value` of `<input>` in console/DOM attributes) | Code review — `SkipLink`/`accessibilityAudit` must not log input values |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — accessibility module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — accessibility module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/accessibility/` → exit 1 (0 matches) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | SkipLink Visibility | Visually hidden until `:focus` → visible `position: fixed` `top: var(--ix-space-2)` `left: var(--ix-space-4)` with `background: var(--ix-bg-surface-raised)` `border: var(--ix-border-subtle)` | WCAG 2.4.1 Bypass Blocks |
| U-2 | Focus Visibility | Focus ring `var(--ix-color-focus)` `#8CC2FF` (contrast ≥8.9:1 on `var(--ix-bg-surface)` `#111822`) on `SkipLink` when focused | WCAG 2.4.7 Focus Visible, 08 |
| U-3 | ARIA Landmarks | Regions A–F have explicit landmark roles (`banner`, `navigation`, `main#main-content`, `complementary`, `region`) — `accessibilityAudit.test.ts` verifies existence | WCAG 1.3.1 Info & Relationships |
| U-4 | Heading Hierarchy | `h1` → `h2` → `h3` unbroken across shell and workspace pages — no skipped levels, at least one `h1` per page (audit via heading queries) | WCAG 1.3.1 |
| U-5 | Keyboard Bypass | `Tab` (first press) lands on `SkipLink`; `Enter` on `SkipLink` moves focus to `#main-content` `main` landmark (skip of Regions A/B) | WCAG 2.4.1 + 08 keyboard |
| U-6 | No Color-Alone | SkipLink not color-dependent — text label `Skip to main content` + focus ring plus semantic role | 02 §Design, 08 |
| U-7 | Dark-First | SkipLink renders correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `SkipLink.test.tsx` | Renders `href="#main-content"`, `aria-label="Skip to main content"`, visually hidden until `:focus` (class/style), `onClick` focuses `#main-content`; receives focus on first `Tab` |
| T-2 | `accessibilityAudit.test.ts` — landmark completeness | Exactly one `banner`, one `main` (`id="main-content"`), one `navigation` primary, at least one `complementary` when Context Panel present — across shell + at least 2 workspace pages |
| T-3 | `accessibilityAudit.test.ts` — heading hierarchy | No skipped `h1`→`h2`→`h3` levels; at least one `h1` per page; `PanelHeader` `headingLevel 2|3` → `<h2>`/`<h3>` correctly |
| T-4 | `accessibilityAudit.test.ts` — focusability | All `button`/`link`/`combobox`/`textbox` in shell are focusable via `Tab` (no `tabIndex="-1"` on interactive except `main#main-content` which is programmatic-only) |
| T-5 | `SkipLink` token consumption | No ad-hoc hex in `workstation/accessibility/` — via `grep_ad_hoc_hex.log` |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **485 tests — 100% pass** (or 485+ with accounting — see §8) — P01 adds accessibility foundation tests, no existing test should break |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*SkipLink + audit harness are additive — **0 removed / 0 modified** expected for existing tests (113 suites 485 tests from UI-009 COMPLETE). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`SkipLink` with `href="#non-existent"` → test fails (must point to existing `#main-content`); `accessibilityAudit` with removed `role="main"` → fails; `SkipLink` not first focusable → fails (must be first `Tab`).

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui010/` on `main` — new `ui010` evidence directory for UI-010)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **485+ pass** — full log (must show 113 suites/485 baseline + new P01 suites) | `docs/evidence/ui010/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui010/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui010/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui010/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui010/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/accessibility/` | Level II | 0 | `docs/evidence/ui010/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/accessibility/` | Level II | 0 | `docs/evidence/ui010/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `#[0-9A-F]{3,6}` in `workstation/accessibility/` | Level II | 0 (proves token consumption) | `docs/evidence/ui010/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui010/grep_secrets.log` |
| E-10 | Accessibility audit evidence | Level II | `accessibilityAudit.test.ts` run log excerpt + optional `accessibility.log` axe summary (landmarks/headings/focus) | `docs/evidence/ui010/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui010/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-010-P01.md` with 20 sections | `DELIVERY_REPORT_UI-010-P01.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `SkipLink` first-Tab focus + audit heading queries — captured via `SkipLink.test.tsx`/`accessibilityAudit.test.ts`) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **New evidence directory `docs/evidence/ui010/` is required for UI-010 (separate from `ui009`).**

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs. **For reliable cross-platform `grep` on Windows, use *Git Bash* (bundled with Git for Windows) — it runs identical Bash commands as DA's Linux.**

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Create evidence dir | `New-Item -ItemType Directory -Force -Path docs/evidence/ui010` | `mkdir -p docs/evidence/ui010` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui010/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui010/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui010/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui010/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui010/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **485+ pass** (P01 will be 113→~114 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `workstation/accessibility/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `workstation/accessibility/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/accessibility/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | **Git Bash:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**Exit code contract (both platforms, identical):** **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion fixtures, documented).**

#### 3. Documentation Diffs

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui010/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui010/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui010/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui010/changelog_diff.log` |

**All logs must be committed to `docs/evidence/ui010/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both deterministic. **Git Bash on Windows gives identical `grep` exit codes as DA's Linux** — strongly recommended.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-010-P01.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-010-P01 — Accessibility Foundation & Semantic Audit |
| 2 | Governing Build Order | `BUILD_ORDER_UI-010-P01` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` §10 (Proposed P01) |
| 4 | Previous Baseline | UI-009 COMPLETE (D-60): 113 suites / 485 tests · 414 backend · whole-surface harmonization |
| 5 | Implementation Summary | What accessibility foundation was built (SkipLink, landmark integration, audit harness) + token consumption |
| 6 | Files Created | List with nature (expected 2–3 accessibility files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `InstitutionalWorkspaceShell.tsx` Region A + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (6 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 113/485 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 113/485 vs current (must be ≥113/485) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0 in `workstation/accessibility/`) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + skip-link snapshots + audit evidence |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Foundation audit complete; responsive reflow in P02” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-010-P02 Responsive Behaviour & Adaptive Layouts |
| 20 | DA Sign-off | Governance Declaration per Amendment §25 |

### 9.1 Mandatory Registers

**Deviation Register (§5):**
```text
## Deviations From Approved Build Order

[NO DEVIATIONS] — or deviation table with rationale
```

**Test Accounting (§8):**
```text
Previous Baseline:
- Frontend: 113 suites / 485 tests
- Backend: 414 tests

New tests physically added:
- [N tests across SkipLink + accessibilityAudit suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [113 or 113+N] suites / [485 or 485+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-60 UI-009 COMPLETE (113/485 + 414) + D-61 Design Plan (1 minor observation O-010-01)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), whole-surface harmonization (P06), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 113 suites / 485 frontend + 414 backend (D-60) — plus D-61 design plan (no code)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-010-01 (responsive sticky-header z-index — minor, for P02)

New Phase Scope: Accessibility Foundation — SkipLink + semantic audit (6 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P01, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-010-P01 APPROVED** (version increment per governance, e.g., 8.77.0) |
| `CHANGELOG.md` | Record P01 completion |
| `RISK_REGISTER.md` | Verify no new risks, or record with mitigation |
| `TECHNICAL_DEBT_REGISTER.md` | Verify 0 new debt, or record with rationale |

If no change required for a file, Delivery Report §15 must state explicitly:
```text
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

---

## 11. BUILD ORDER SEQUENCE

```text
[ BUILD_ORDER_UI-010-P01 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Accessibility Foundation Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P01 Determination ]
         ↓
[ BUILD_ORDER_UI-010-P02 — Responsive Behaviour & Adaptive Layouts ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | SkipLink renders and receives focus on initial Tab; links to `#main-content`; `href="#main-content"` points to existing `id="main-content"`; `aria-label="Skip to main content"` | Mandatory | `SkipLink.test.tsx` + E-12 |
| AC-2 | Shell Regions A–F provide explicit ARIA landmark roles (`banner`, `navigation`, `main#main-content`, `complementary`, `region`) | Mandatory | `accessibilityAudit.test.ts` |
| AC-3 | Automated semantic audit verifies all headings `h1` → `h2` → `h3` follow strict unbroken hierarchy | Mandatory | `accessibilityAudit.test.ts` |
| AC-4 | Pure token consumption: 0 ad-hoc hex in `workstation/accessibility/` (`--ix-*` only) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-5 | Constitutional invariants: Zero actuation, zero external LLMs, zero `dangerouslySetInnerHTML`/`eval` in accessibility module | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-6 | Frontend regression baseline ≥485 tests (expected 490) — 100% pass; Backend 414 pass; `tsc` and `vite build` exit 0 | Mandatory | E-1/E-2/E-3 |
| AC-7 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 7 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**Observations O-010-01 (sticky-header z-index) will be verified as closed via P02 responsive implementation, not P01.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P01 implementation only** — no P02–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L, D-61 APPROVED WITH OBSERVATIONS) |
| P01 Design | §10 Proposed P01 (7-part re-baseline — `SkipLink` + semantic audit) |
| Preceding Baseline | D-60: 113 suites / 485 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 + Workspace Shell Regions A–F |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — §7 User Experience & Accessibility — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-60 (113/485) preserved as previous baseline |
| §3 Single Active Phase | **P01 = ACTIVE**, P02–P06 = NOT AUTHORIZED, UI-009 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §10 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-60 113/485 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no responsive/feedback/shortcut work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P02 not authorized until P01 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui010/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-61 preserved |
| §24 P01 Controls | Applied — SkipLink + semantic audit |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P01 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-010-P01**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

