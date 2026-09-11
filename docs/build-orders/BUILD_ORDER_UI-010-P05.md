# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-010-P05`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-65 — UI-010-P04 **APPROVED** (129 suites / 534 tests · 414 backend · exit 0) — Observation O-P10P04-01 (evidence logs documentary tier, continuity)
**Phase:** UI-010-P05 — Screen-Reader, High-Contrast & Reduced-Motion Compliance
**Governing Design Plan:** `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (Approved per D-61, §5/P05 — Screen-Reader, High-Contrast & Reduced-Motion Compliance)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010)
**Preceding Milestone:** UI-010-P04 (D-65 APPROVED) — 129 suites / 534 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 129/534 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P05 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-010-P05` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-61 — UI-010 Design Plan APPROVED WITH OBSERVATIONS (O-010-01 sticky-header — closed D-63) |
| Preceding Milestone | UI-010-P04 (D-65) — 129/534 + 414 |
| Next Milestone | UI-010-P05 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-010) |
| Risk Level | Low (accessibility primitives — ARIA live regions, high-contrast, reduced-motion, no business logic) |

---

## 2. PHASE OBJECTIVE

Implement **screen-reader, high-contrast, and reduced-motion compliance** for AXIOM by codifying **ARIA live regions** (`aria-live="polite"`/`assertive`), **screen-reader-only labels** (`.ix-sr-only`), **multi-modal status encoding** (no color-alone), **high-contrast theme overrides** (`@media (prefers-contrast: more)`), and **reduced-motion zeroing** (`@media (prefers-reduced-motion: reduce)` → `0ms`) — per WCAG 1.4.1 (Use of Color), 4.1.3 (Status Messages), 1.4.3/1.4.6 (Contrast), 2.3.3 (Animation from Interactions) and `16` Brand Governance.

This phase is **screen-reader/high-contrast/reduced-motion compliance, not whole-surface axe audit (P06) or keyboard trap (P04).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **RouteAnnouncer — `RouteAnnouncer.tsx` + `RouteAnnouncer.css`** | Global live region announcing route transitions: `aria-live="polite"` `aria-atomic="true"` `role="status"` + `aria-label="Route announcements"`; rendered once in `InstitutionalWorkspaceShell.tsx` `Region A` (or `WorkspaceHost.tsx`); announces `Navigated to ${workspaceTitle}` on route change via `useEffect` listening to router `location` |
| 2 | **Screen-Reader-Only Utility — `.ix-sr-only` in `tokens.css` (or `accessibility.css`) + `SrOnly.tsx` (optional helper)** | Utility class: `position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); whiteSpace: nowrap; border: 0;` — plus optional `<span className="ix-sr-only">{label}</span>` helper component |
| 3 | **Multi-Modal Status Encoding Audit** | Verify no component communicates status by color alone — every `Badge`/`StatusChip`/`Toast`/`ErrorBanner` already in P02/P05 combines text label + Unicode symbol (`◆◆◆`, `✓`, `ℹ`, `⚠`, `✕`) + semantic token color — add `multiModalStatus.test.tsx` asserting text+symbol+color for at least 2 status variants |
| 4 | **High-Contrast Theme Overrides — `tokens.css` + `theme.ts`** | `@media (prefers-contrast: more)` overrides: `--ix-bg-root` → `#000000`, `--ix-text-primary` → `#FFFFFF`, `--ix-border-subtle` → `#FFFFFF` (or appropriate high-contrast tokens), `--ix-color-focus` → `#FFFF00` (or `#8CC2FF` at higher contrast) — via `var(--ix-*)` tokens, not hardcoded hex outside `tokens.css` |
| 5 | **Reduced-Motion Compliance** | Verify `@media (prefers-reduced-motion: reduce)` → all `transition: var(--ix-motion-fast) 120ms` → `0ms` and `animation: none` for `Skeleton` shimmer, `Dialog` backdrop, `Collapsible` height, `Accordion` motion — already in P05 but re-verified for `RouteAnnouncer` |
| 6 | **Token Consumption Enforcement** | All accessibility primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `workstation/accessibility/` |
| 7 | **Comprehensive Accessibility Tests** | Per-component suites covering `RouteAnnouncer` `aria-live`, `.ix-sr-only` utility, high-contrast media query, reduced-motion, multi-modal status |
| 8 | **Evidence Package** | Logs committed to `docs/evidence/ui010/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Whole-surface WCAG axe audit across all 129 suites | **UI-010-P06** scope — P05 is screen-reader/high-contrast/reduced-motion compliance for new primitives, not whole-surface |
| 2 | Keyboard shortcut manager re-architecture (`Ctrl+K`/`Escape` LIFO already in P04) | **P04 already COMPLETE** — reuse, do not rewrite |
| 3 | Responsive breakpoint tokens redefinition (`--ix-breakpoint-*`) or panel collapse reflow | **P02 already COMPLETE** — reuse |
| 4 | New backend endpoints, migrations, schema changes | No persistence change |
| 5 | WebSocket / real-time push alterations | Not in P05 design |
| 6 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 7 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |
| 8 | Mobile <768px companion viewports | **DEFERRED** per Design Plan §9 (post-1.0) — P05 targets desktop/laptop |
| 9 | `EmptyState` / `RouteAnnouncer` beyond `RouteAnnouncer` itself (Feedback states already in P03) | P03 already COMPLETE — reuse `EmptyState` |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Accessibility Primitives Architecture (Per Design Plan §5 P05 + WCAG 4.1.3/1.4.1)

- **Location (Recommended):** `frontend/src/workstation/accessibility/` — `RouteAnnouncer.tsx`, `RouteAnnouncer.css` (if needed), `SrOnly.tsx` (optional), `multiModalStatus.test.tsx` — DA may alternatively place `SrOnly` utility in `frontend/src/components/ui/` alongside `Badge`/`StatusChip`, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only. `tokens.css` high-contrast overrides live in `frontend/src/workstation/design/tokens.css` (or existing `tokens.css`).
- **RouteAnnouncer:** Single `<div aria-live="polite" aria-atomic="true" role="status" aria-label="Route announcements" className="ix-sr-only">` rendered once in `InstitutionalWorkspaceShell.tsx` (Region A or `WorkspaceHost`) — `useEffect` watches `useLocation()` (or router) and sets `announcement = `Navigated to ${routeTitle}``; screen reader announces route change without visual change. Must be `aria-live="polite"` (not `assertive`) for route transitions (not error).
- **SrOnly Utility:** CSS class `.ix-sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); whiteSpace: nowrap; border: 0; }` — plus optional `<span className="ix-sr-only">` helper component for icon-only controls (e.g., `Button` icon-only `aria-label` fallback).
- **High-Contrast:** In `tokens.css`, add `@media (prefers-contrast: more) { :root { --ix-bg-root: #000000; --ix-text-primary: #FFFFFF; --ix-border-subtle: #FFFFFF; --ix-color-focus: #FFFF00; } }` (or equivalent high-contrast tokens — DA to declare exact values, must be via `var(--ix-*)` tokens, not hardcoded outside `tokens.css`).
- **Reduced-Motion:** Ensure `RouteAnnouncer` has no motion (static live region); existing `Skeleton`/`Dialog`/`Collapsible` `120ms` → `0ms` via `@media (prefers-reduced-motion: reduce)` already in P05, re-verify for `RouteAnnouncer`.
- **Multi-Modal Status:** `Badge`/`StatusChip`/`Toast`/`ErrorBanner` already in P02/P05 combine text + symbol + color — `multiModalStatus.test.tsx` proves at least 2 variants (e.g., `StatusChip HIGH` text+`◆◆◆`+`#10B981`, `Toast error` text+`✕`+`#EF4444`).
- **Token Consumption:** Every visual value (background, text, border, focus) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` spacing outside `var(--ix-space-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/accessibility/`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; accessibility primitives are presentation ARIA/live regions, not business logic.

### 4.3 Interaction Contracts

| Component / Utility | Contract |
|-----------|----------|
| `RouteAnnouncer` | No props (or `routeTitle?: string` if controlled) — renders `aria-live="polite"` `aria-atomic="true"` `role="status"` `aria-label="Route announcements"` + `className="ix-sr-only"` live region; announces `Navigated to ${title}` on route change via `useEffect` |
| `.ix-sr-only` | CSS class — `position: absolute; width: 1px; height: 1px; ... clip: rect(0,0,0,0);` — visually hidden but screen-reader accessible |
| `SrOnly` (optional helper) | `children: ReactNode` — renders `<span className="ix-sr-only">{children}</span>` |
| High-Contrast | `@media (prefers-contrast: more)` in `tokens.css` — overrides `--ix-bg-root`, `--ix-text-primary`, etc. to high-contrast values via tokens |
| Reduced-Motion | `@media (prefers-reduced-motion: reduce)` in `tokens.css` — all `transition: var(--ix-motion-fast)` → `0ms`, `animation: none` |
| Multi-Modal Status | `Badge`/`StatusChip`/`Toast`/`ErrorBanner` `variant` → text label + symbol + semantic token color — never color alone |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in accessibility module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/accessibility/` — 0 matches |
| 4 | No `eval` / `new Function` in accessibility module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/accessibility/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |
| 7 | No credential exposure via live region (no `value` of `<input>` in `aria-live` announcement) | Code review — `RouteAnnouncer` must announce `routeTitle` only, not input values |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — accessibility module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — accessibility module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/accessibility/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Screen-Reader Announcements | `RouteAnnouncer` `aria-live="polite"` `aria-atomic="true"` `role="status"` announces route transitions without visual change | WCAG 4.1.3 Status Messages, 08 |
| U-2 | Sr-Only Utility | `.ix-sr-only` visually hidden but screen-reader accessible — `position: absolute; width:1px; height:1px; ... clip` | WCAG 1.3.1, 08 |
| U-3 | No Color-Alone Encoding | All status primitives (`Badge`/`StatusChip`/`Toast`/`ErrorBanner`) combine text + symbol + color — re-verified via `multiModalStatus.test.tsx` | WCAG 1.4.1 Use of Color, 02 §Design |
| U-4 | High-Contrast | `@media (prefers-contrast: more)` high-contrast tokens (`#000000` bg + `#FFFFFF` text + `#FFFF00` focus or equivalent) via `var(--ix-*)` | WCAG 1.4.3, 1.4.6, 16 Part XII |
| U-5 | Reduced-Motion | `@media (prefers-reduced-motion: reduce)` → all `transition`/`animation` → `0ms`/`none` for `RouteAnnouncer` (static) + existing `Dialog`/`Skeleton`/`Collapsible` | WCAG 2.3.3, 08 |
| U-6 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` already in P04 — `RouteAnnouncer` has no focus (live region is not focusable, correct) | WCAG 2.4.7 |
| U-7 | ARIA | `RouteAnnouncer` `role="status"` `aria-live="polite"` `aria-atomic` + `aria-label="Route announcements"`; `Badge`/`StatusChip`/`Toast` `role` + `aria-label` already in P02/P05 | WCAG 4.1.3, 08 |
| U-8 | Dark-First | `RouteAnnouncer` live region not visible (sr-only), so dark-first not applicable; high-contrast overrides render correctly on `var(--ix-bg-root)` | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `RouteAnnouncer.test.tsx` | Renders `aria-live="polite"` `aria-atomic="true"` `role="status"` `aria-label="Route announcements"` + `className="ix-sr-only"` + announces `routeTitle` on `location` change |
| T-2 | `SrOnly.test.tsx` (or within `RouteAnnouncer.test.tsx` / `accessibilityAudit.test.tsx`) | `.ix-sr-only` class visually hidden but accessible — `position: absolute` + `clip: rect(0,0,0,0)` + not `display: none` (screen-reader still reads) |
| T-3 | `multiModalStatus.test.tsx` | At least 2 status variants text+symbol+color (e.g., `Badge` `critical` text+`✕`+`#EF4444`, `StatusChip` `HIGH` text+`◆◆◆`+`#10B981` + `Toast` `warning` text+`⚠`+`#F59E0B`) — never color alone |
| T-4 | `highContrast.test.tsx` (or within `SrOnly.test.tsx`) | `@media (prefers-contrast: more)` high-contrast tokens present in `tokens.css` (`#000000`/`#FFFFFF`/`#FFFF00` or equivalent) |
| T-5 | `ui010_p05_security_invariants.test.ts` | S-1 whole-repo actuation + S-2 LLM + S-3 sandbox + S-4 ad-hoc hex in accessibility module + S-5 secrets — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **534 tests — 100% pass** (or 534+ with accounting — see §8) — P05 adds screen-reader/high-contrast/reduced-motion tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Screen-reader/high-contrast/reduced-motion primitives are additive — **0 removed / 0 modified** expected for existing tests (129 suites 534 tests from UI-010-P04). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`RouteAnnouncer` with no `routeTitle` → still renders live region but announces empty (not crash); `SrOnly` with `display: none` → test fails (must be `clip`-hidden, not `display:none`); `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui010/` on `main` — continue `ui010` directory)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **534+ pass** — full log (must show 129 suites/534 baseline + new P05 suites) | `docs/evidence/ui010/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui010/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui010/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui010/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui010/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/accessibility/` | Level II | 0 | `docs/evidence/ui010/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/accessibility/` | Level II | 0 | `docs/evidence/ui010/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/accessibility/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui010/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui010/grep_secrets.log` |
| E-10 | Accessibility audit evidence | Level II | WCAG 1.4.1/4.1.3 + `RouteAnnouncer` `aria-live` + `.ix-sr-only` + high-contrast + reduced-motion | `docs/evidence/ui010/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui010/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-010-P05.md` with 20 sections | `DELIVERY_REPORT_UI-010-P05.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `RouteAnnouncer` `aria-live` + `.ix-sr-only` DOM queries via `RouteAnnouncer.test.tsx`) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. Continue evidence directory `docs/evidence/ui010/` (same as P01→P04).

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

**Expected:** `VITEST_EXIT:0` with **534+ pass** (P05 will be 129→~133 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

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

DA shall produce `DELIVERY_REPORT_UI-010-P05.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-010-P05 — Screen-Reader, High-Contrast & Reduced-Motion Compliance |
| 2 | Governing Build Order | `BUILD_ORDER_UI-010-P05` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` §5 P05 + §10 P01 foundation |
| 4 | Previous Baseline | UI-010-P04 D-65: 129 suites / 534 tests · 414 backend · keyboard/focus |
| 5 | Implementation Summary | What screen-reader/high-contrast/reduced-motion primitives were built (RouteAnnouncer, .ix-sr-only, multi-modal re-verification, high-contrast tokens, reduced-motion) + token consumption |
| 6 | Files Created | List with nature (expected RouteAnnouncer + SrOnly utility + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `InstitutionalWorkspaceShell.tsx` Region A + `tokens.css` + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (8 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 129/534 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 129/534 vs current (must be ≥129/534) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0 in `workstation/accessibility/`) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + `RouteAnnouncer` `aria-live` + `.ix-sr-only` |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Screen-reader/high-contrast complete; whole-surface audit in P06” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-010-P06 Whole-Surface Accessibility Audit & Completion Checkpoint |
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
- Frontend: 129 suites / 534 tests
- Backend: 414 tests

New tests physically added:
- [N tests across RouteAnnouncer/SrOnly/multiModalStatus/highContrast/reducedMotion suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [129 or 129+N] suites / [534 or 534+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-65 UI-010-P04 (129/534 + 414)
- Commit: [current HEAD]

Inherited Components: SkipLink.tsx/.css, accessibilityAudit.test.tsx, breakpoint tokens (P02), EmptyState.tsx, DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), Panel/PanelHeader/PanelActionBar/Collapsible (P03), tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 129 suites / 534 frontend + 414 backend (D-65)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P10P04-01 (evidence on main continuity)

New Phase Scope: Screen-Reader & High-Contrast — RouteAnnouncer + .ix-sr-only + multi-modal re-verification + high-contrast tokens + reduced-motion (8 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P05, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-010-P05 APPROVED** (version increment per governance, e.g., 8.81.0) |
| `CHANGELOG.md` | Record P05 completion |
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
[ BUILD_ORDER_UI-010-P05 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Screen-Reader/High-Contrast Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P05 Determination ]
         ↓
[ BUILD_ORDER_UI-010-P06 — Whole-Surface Accessibility Audit & Completion Checkpoint ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | `RouteAnnouncer` renders `aria-live="polite"` `aria-atomic="true"` `role="status"` `aria-label="Route announcements"` + `className="ix-sr-only"` + announces `routeTitle` on `location` change | Mandatory | `RouteAnnouncer.test.tsx` |
| AC-2 | `.ix-sr-only` visually hidden but screen-reader accessible — `position: absolute; width:1px; height:1px; clip: rect(0,0,0,0)` + not `display:none` | Mandatory | `SrOnly.test.tsx` or within `RouteAnnouncer.test.tsx` |
| AC-3 | Multi-modal status re-verified: at least 2 status variants text+symbol+color (e.g., `Badge` `critical` text+`✕`+`#EF4444`, `StatusChip` `HIGH` text+`◆◆◆`+`#10B981` + `Toast` `warning` text+`⚠`+`#F59E0B`) — never color alone | Mandatory | `multiModalStatus.test.tsx` |
| AC-4 | High-contrast tokens via `@media (prefers-contrast: more)` (`#000000`/`#FFFFFF`/`#FFFF00` or equivalent) in `tokens.css` | Mandatory | `highContrast.test.tsx` |
| AC-5 | Pure token consumption: 0 ad-hoc hex in `workstation/accessibility/` (outside `tokens.css`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-6 | Constitutional invariants: Zero actuation, zero external LLMs, zero `dangerouslySetInnerHTML`/`eval` in accessibility module | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-7 | Frontend regression baseline ≥534 tests — 100% pass; Backend 414 pass; `tsc` and `vite build` exit 0 | Mandatory | E-1/E-2/E-3 |
| AC-8 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P05 implementation only** — no P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L, D-61 APPROVED WITH OBSERVATIONS) |
| P05 Design | §5 Phase Breakdown — P05 Screen-Reader, High-Contrast & Reduced-Motion Compliance |
| Preceding Baseline | D-65: 129 suites / 534 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 + Workspace Shell Regions A–F |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — §7 User Experience & Accessibility — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-65 (129/534) preserved as previous baseline |
| §3 Single Active Phase | **P05 = ACTIVE**, P06 = NOT AUTHORIZED, UI-010-P01→P04 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P05 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-65 129/534 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no whole-surface audit work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P06 not authorized until P05 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui010/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-65 preserved |
| §24 P05 Controls | Applied — screen-reader/high-contrast/reduced-motion + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P05 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-010-P05**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

