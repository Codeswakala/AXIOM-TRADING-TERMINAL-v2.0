# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-010-P02`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-62 — UI-010-P01 **APPROVED** (116 suites / 495 tests · 414 backend · exit 0) — Observation O-P10P01-01 (evidence logs documentary tier, continuity)
**Phase:** UI-010-P02 — Responsive Behaviour & Adaptive Layouts
**Governing Design Plan:** `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (Approved per D-61, §5/P02 — Responsive Behaviour & Adaptive Layouts)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010)
**Preceding Milestone:** UI-010-P01 (D-62 APPROVED) — 116 suites / 495 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 116/495 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P02 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-010-P02` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-61 — UI-010 Design Plan APPROVED WITH OBSERVATIONS (O-010-01 sticky-header z-index, non-blocking) |
| Preceding Milestone | UI-010-P01 (D-62) — 116/495 + 414 |
| Next Milestone | UI-010-P02 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-010) |
| Risk Level | Low (responsive tokens + layout reflow — presentation adaptation, no business logic) |

---

## 2. PHASE OBJECTIVE

Implement **responsive behaviour and adaptive layouts** for AXIOM by codifying **breakpoint tokens** (`--ix-breakpoint-*`), **adaptive panel collapsing** (desktop → laptop), **table horizontal scrolling with sticky headers**, and **layout reflow without horizontal page scrolling** at 1280px and 1024px widths — per WCAG 1.4.10 (Reflow) and 12 Part V §9 Responsive Behaviour.

This phase is **responsive adaptivity, not feedback-state, keyboard, or whole-surface audit.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Responsive Breakpoint Tokens — `tokens.css` Extension** | Codify `--ix-breakpoint-lg: 1280px`, `--ix-breakpoint-md: 1024px` (and `--ix-breakpoint-sm: 768px` if needed for future, but not required for P02) under Tier 1 Foundation tokens; define `--ix-table-sticky-header-z-index: 2` (addresses O-010-01 sticky-header stacking) and `--ix-nav-dock-collapsed-width` token for collapsed dock |
| 2 | **Adaptive Panel Collapsing** | Shell Regions A–F adapt at 1280px and 1024px: Region B Navigation Dock collapses to icon-only + toggle button, Region D Context Panel collapses/docks bottom on laptop, Region A Global Command Bar condenses — **no horizontal page scrolling at 1280px/1024px** |
| 3 | **Table Horizontal Scrolling with Sticky Headers** | `DataTable` wrapper provides `overflow-x: auto` + `max-width: 100%` + sticky `<thead>` `position: sticky; top: 0; z-index: var(--ix-table-sticky-header-z-index); background: var(--ix-table-header-bg)` — headers remain visible while body scrolls horizontally at narrow widths |
| 4 | **Layout Reflow Verification** | Prove zero horizontal page scrolling at 1280px and 1024px viewport widths — no `overflow-x: scroll` on `<body>`/`html`; all panels `max-width: 100%` + `box-sizing: border-box` |
| 5 | **Token Consumption Enforcement** | All responsive primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded `px` breakpoint outside tokens in `workstation/accessibility/` + `components/ui/` + `styles/` |
| 6 | **Responsive Tests** | Suites covering breakpoint tokens existence, panel collapse at 1280/1024, table sticky header, overflow, and `prefers-reduced-motion` still respected |
| 7 | **Evidence Package** | Logs committed to `docs/evidence/ui010/` (vitest, tsc/vite, greps, diffs, accessibility/responsive spot-check) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Feedback state standardization (`EmptyState` primitive, Loading/Empty/Error/Toast harmonization across 7 workspaces) | **UI-010-P03** scope |
| 2 | Keyboard shortcut manager, global `Ctrl+K`, focus trap validation beyond SkipLink, focus restoration | P04 scope — SkipLink focus itself is P01 completeness |
| 3 | Screen-reader live regions (`RouteAnnouncer` `aria-live`), `prefers-contrast` high-contrast, `prefers-reduced-motion` beyond existing 120ms→0ms | P05 scope |
| 4 | Whole-surface WCAG axe audit across all 116 suites | **P06** scope — P02 is responsive reflow, not whole-surface |
| 5 | `EmptyState` / `RouteAnnouncer` / high-contrast theme components | P03/P05 scope |
| 6 | New backend endpoints, migrations, schema changes | No persistence change |
| 7 | WebSocket / real-time push alterations | Not in P02 design |
| 8 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 9 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |
| 10 | Mobile <768px companion viewports | **DEFERRED** per Design Plan §9 (post-1.0) — P02 targets 1280/1024 only |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Responsive Foundation Architecture (Per Design Plan §10 + §14 Responsive Breakpoints)

- **Location (Recommended):** `frontend/src/workstation/design/tokens.css` — extend Tier 1 Foundation with breakpoint tokens; DA may alternatively place responsive logic in `frontend/src/styles/responsive.css` if reusing existing responsive file, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **Breakpoint Tokens:** `--ix-breakpoint-lg: 1280px`, `--ix-breakpoint-md: 1024px` (and optionally `--ix-breakpoint-sm: 768px` for future) — must be CSS custom properties (not hardcoded `@media (max-width: 1280px)` literals outside tokens). Sticky header `z-index` via `--ix-table-sticky-header-z-index: 2` (closes O-010-01).
- **Panel Collapse:** `InstitutionalWorkspaceShell.tsx` Regions B (Navigation Dock) + D (Context Panel) apply `@media (max-width: var(--ix-breakpoint-lg))` / `1024px` (via CSS `max-width` media queries using tokens where possible) to collapse to icon-only / bottom dock. Must **not** introduce horizontal page scroll: `html, body { overflow-x: hidden; max-width: 100vw; }` pattern or equivalent flex containment.
- **Table Sticky Header:** `DataTable.css` / `DataTable.tsx` wrapper `overflow-x: auto` + `table { min-width: 640px; }` (or appropriate) + `thead { position: sticky; top: 0; z-index: var(--ix-table-sticky-header-z-index); background: var(--ix-table-header-bg); }` — headers remain visible while body scrolls horizontally at narrow widths.
- **Token Consumption:** Every visual value (breakpoint, `z-index`, spacing, background, border) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` breakpoint outside `var(--ix-breakpoint-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/design/` or `styles/` + `InstitutionalWorkspaceShell.tsx` Regions A–F); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; responsive behaviour is presentation adaptation, not business logic.

### 4.3 Interaction Contracts

| Component / Token | Contract |
|-----------|----------|
| `--ix-breakpoint-lg` | `1280px` — CSS custom property — used in `@media (max-width: 1280px)` (or `min-width` alternative) |
| `--ix-breakpoint-md` | `1024px` — same |
| `--ix-table-sticky-header-z-index` | `2` (or `1`/`3` — DA to declare, must be `>1` to stack above table rows) — used in `thead { z-index: var(--ix-table-sticky-header-z-index); }` |
| `InstitutionalWorkspaceShell.tsx` Regions | At `≤1280px`: Region B `nav` collapses to icon-only width via `--ix-nav-dock-collapsed-width`; at `≤1024px`: Region D `aside` collapses/docks bottom or hides with toggle; `html`/`body` `overflow-x` hidden, no horizontal page scroll |
| `DataTable` wrapper | `overflow-x: auto` + `max-width: 100%` + `thead` sticky — horizontal scroll is **inside table wrapper**, not page |
| `DataTable` `thead` | `position: sticky; top: 0; z-index: var(--ix-table-sticky-header-z-index); background: var(--ix-table-header-bg);` — remains visible while `tbody` scrolls |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in responsive module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/design/` + `frontend/src/styles/` (if used) — 0 matches |
| 4 | No `eval` / `new Function` in responsive module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/` + `frontend/src/styles/` + `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors/spacings via `var(--ix-*)`) |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — responsive module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — responsive module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/design/ frontend/src/styles/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Breakpoint Tokens | `--ix-breakpoint-lg: 1280px` + `--ix-breakpoint-md: 1024px` present in `tokens.css` | WCAG 1.4.10 Reflow (no horizontal scrolling at 320px CSS pixel equivalent; adapted to 1280/1024 institutional desktop), 08 responsive |
| U-2 | No Horizontal Page Scroll | At 1280px and 1024px viewport widths, `document.documentElement.scrollWidth === window.innerWidth` (no `overflow-x: scroll` on `html`/`body`) — panels reflow via collapse, not page scroll | WCAG 1.4.10 |
| U-3 | Panel Collapse | Region B `nav` collapses to icon-only + toggle at ≤1280px; Region D `aside` collapses/docks at ≤1024px — focus order preserved (`Tab` still reaches collapsed toggle) | 12 Part V §16 Responsive Behaviour |
| U-4 | Table Horizontal Scroll + Sticky Header | `DataTable` wrapper `overflow-x: auto` + `thead` sticky `z-index: var(--ix-table-sticky-header-z-index)` — headers remain visible while `tbody` rows scroll horizontally at narrow widths | WCAG 1.4.10 + 08 data table pattern |
| U-5 | Motion Restraint | No new motion introduced; existing `120ms` motion respected; `prefers-reduced-motion` still → `0ms` (P01 tokens) | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` still traverses panel frames → `DataTable` headers → pagination + overlay actions at narrow widths; `SkipLink` still first `Tab` | WCAG 2.1.1/2.4.7 |
| U-7 | ARIA | No new ARIA required for responsive reflow (landmarks/headings already in P01); `DataTable` sticky header retains `aria-sort` + `scope="col"` | WCAG 1.3.1 |
| U-8 | Dark-First | Responsive collapse renders correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `responsiveTokens.test.ts` | Breakpoint tokens `--ix-breakpoint-lg: 1280px`, `--ix-breakpoint-md: 1024px`, `--ix-table-sticky-header-z-index: 2` present in `tokens.css` (via `getComputedStyle` or `theme.ts` contract) |
| T-2 | `responsiveLayout.test.tsx` | Panel collapse at 1280px (Region B `nav` icon-only + toggle) + at 1024px (Region D `aside` collapsed/docked) — render shell at mocked `window.innerWidth` 1280/1024 |
| T-3 | `DataTable.stickyHeader.test.tsx` (or within `DataTable.test.tsx`) | `DataTable` wrapper `overflow-x: auto` + `thead` `position: sticky` + `z-index: var(--ix-table-sticky-header-z-index)` + no `overflow-x: scroll` on `html`/`body` at 1280/1024 |
| T-4 | `responsiveReflow.test.tsx` | Zero horizontal page scroll at 1280px and 1024px: `document.documentElement.scrollWidth <= window.innerWidth` after render — no `overflow-x: scroll` on `html`/`body` |
| T-5 | `ui010_p02_security_invariants.test.ts` | S-1 whole-repo actuation + S-2 LLM + S-3 sandbox + S-4 ad-hoc hex in responsive module + S-5 secrets — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **495 tests — 100% pass** (or 495+ with accounting — see §8) — P02 adds responsive tests, no existing test should break |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Responsive tokens + layout reflow are additive — **0 removed / 0 modified** expected for existing tests (116 suites 495 tests from UI-010-P01). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`DataTable` at `window.innerWidth=1024` with `columns×6` wide table → wrapper `overflow-x: auto` (scrollable) but `html`/`body` not scrollable; `Panel` collapsed at 1024 → still focusable via toggle; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui010/` on `main` — continue `ui010` directory)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **495+ pass** — full log (must show 116 suites/495 baseline + new P02 suites) | `docs/evidence/ui010/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui010/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui010/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui010/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui010/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/design/` + `styles/` | Level II | 0 | `docs/evidence/ui010/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/design/` + `styles/` | Level II | 0 | `docs/evidence/ui010/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/design/` + `styles/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui010/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui010/grep_secrets.log` |
| E-10 | Responsive audit evidence | Level II | `responsiveLayout.test.tsx` + `DataTable.stickyHeader.test.tsx` + `responsiveReflow.test.tsx` run log excerpt + optional `accessibility.log` viewport note (1280/1024) | `docs/evidence/ui010/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui010/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-010-P02.md` with 20 sections | `DELIVERY_REPORT_UI-010-P02.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `DataTable` sticky header + panel collapse at 1280/1024 — captured via `responsiveLayout.test.tsx` DOM queries) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. Continue evidence directory `docs/evidence/ui010/` (same as P01 — do not create new `ui010-p02/`).

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs. **For reliable cross-platform `grep` on Windows, use *Git Bash* (bundled with Git for Windows) — it runs identical Bash commands as DA's Linux.**

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Create evidence dir (if needed) | `New-Item -ItemType Directory -Force -Path docs/evidence/ui010` | `mkdir -p docs/evidence/ui010` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui010/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui010/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui010/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui010/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui010/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui010/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui010/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **495+ pass** (P02 will be 116→~120 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `workstation/design/` + `styles/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `workstation/design/` + `styles/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/design/ frontend/src/styles/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
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

DA shall produce `DELIVERY_REPORT_UI-010-P02.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-010-P02 — Responsive Behaviour & Adaptive Layouts |
| 2 | Governing Build Order | `BUILD_ORDER_UI-010-P02` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` §5 P02 + §10 P01 foundation |
| 4 | Previous Baseline | UI-010-P01 D-62: 116 suites / 495 tests · 414 backend · SkipLink + semantic audit |
| 5 | Implementation Summary | What responsive behaviour was built (breakpoint tokens, panel collapse at 1280/1024, DataTable sticky header + horizontal scroll, layout reflow) + token consumption |
| 6 | Files Created | List with nature (expected 3–4 responsive files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `tokens.css` + `InstitutionalWorkspaceShell.tsx` Regions B/D + `DataTable.css` + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (7 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 116/495 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 116/495 vs current (must be ≥116/495) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + responsive snapshots (1280/1024) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Responsive reflow complete; feedback states in P03” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-010-P03 Feedback States Standardization |
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
- Frontend: 116 suites / 495 tests
- Backend: 414 tests

New tests physically added:
- [N tests across responsiveTokens/responsiveLayout/DataTable.stickyHeader/responsiveReflow suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [116 or 116+N] suites / [495 or 495+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-62 UI-010-P01 (116/495 + 414)
- Commit: [current HEAD]

Inherited Components: SkipLink.tsx/.css, accessibilityAudit.test.tsx, tokens.css 5-tier + --ix-breakpoint-*, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), whole-surface harmonization (P06), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 116 suites / 495 frontend + 414 backend (D-62)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P10P01-01 (evidence on main continuity)

New Phase Scope: Responsive Behaviour — breakpoint tokens + adaptive panel collapse + DataTable sticky header + reflow (7 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P02, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-010-P02 APPROVED** (version increment per governance, e.g., 8.78.0) |
| `CHANGELOG.md` | Record P02 completion |
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
[ BUILD_ORDER_UI-010-P02 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Responsive Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P02 Determination ]
         ↓
[ BUILD_ORDER_UI-010-P03 — Feedback States Standardization ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Breakpoint tokens `--ix-breakpoint-lg: 1280px`, `--ix-breakpoint-md: 1024px`, `--ix-table-sticky-header-z-index: 2` present in `tokens.css` | Mandatory | `responsiveTokens.test.ts` + E-12 |
| AC-2 | Panel collapse at 1280px (Region B `nav` icon-only + toggle) + at 1024px (Region D `aside` collapsed/docked) — focus order preserved | Mandatory | `responsiveLayout.test.tsx` |
| AC-3 | DataTable wrapper `overflow-x: auto` + `thead` sticky `z-index: var(--ix-table-sticky-header-z-index)` + no `overflow-x: scroll` on `html`/`body` at 1280/1024 | Mandatory | `DataTable.stickyHeader.test.tsx` |
| AC-4 | Zero horizontal page scroll at 1280px and 1024px — `document.documentElement.scrollWidth <= window.innerWidth` | Mandatory | `responsiveReflow.test.tsx` |
| AC-5 | Pure token consumption: 0 ad-hoc hex in `workstation/design/` + `styles/` (outside `tokens.css`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-6 | Constitutional invariants: Zero actuation, zero external LLMs, zero `dangerouslySetInnerHTML`/`eval` in responsive module | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-7 | Frontend regression baseline ≥495 tests — 100% pass; Backend 414 pass; `tsc` and `vite build` exit 0 | Mandatory | E-1/E-2/E-3 |
| AC-8 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**Observation O-010-01 (sticky-header z-index) will be verified as closed via AC-1 (`--ix-table-sticky-header-z-index`) + AC-3 (sticky header test).**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P02 implementation only** — no P03–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L, D-61 APPROVED WITH OBSERVATIONS) |
| P02 Design | §5 Phase Breakdown — P02 Responsive Behaviour & Adaptive Layouts |
| Preceding Baseline | D-62: 116 suites / 495 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 + Workspace Shell Regions A–F |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — §7 User Experience & Accessibility — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-62 (116/495) preserved as previous baseline |
| §3 Single Active Phase | **P02 = ACTIVE**, P03–P06 = NOT AUTHORIZED, UI-010-P01 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P02 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-62 116/495 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no feedback/keyboard/high-contrast work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P03 not authorized until P02 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui010/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-62 preserved |
| §24 P02 Controls | Applied — responsive tokens + adaptive collapse + sticky header + reflow |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P02 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-010-P02**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

