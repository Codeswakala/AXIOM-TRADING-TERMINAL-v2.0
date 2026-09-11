# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-010-P04`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-64 — UI-010-P03 **APPROVED WITH OBSERVATIONS** (124 suites / 519 tests · 414 backend · exit 0) — Observations O-P10P03-01 (CSS grid/viewport harmonization minor undeclared), O-P10P03-02 (report typographical + continuity documentary tier)
**Phase:** UI-010-P04 — Keyboard Interaction & Focus Management Hardening
**Governing Design Plan:** `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (Approved per D-61, §5/P04 — Keyboard Interaction & Focus Management Hardening)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010)
**Preceding Milestone:** UI-010-P03 (D-64 APPROVED WITH OBSERVATIONS) — 124 suites / 519 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 124/519 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P04 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-010-P04` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-61 — UI-010 Design Plan APPROVED WITH OBSERVATIONS (O-010-01 sticky-header — closed D-63) |
| Preceding Milestone | UI-010-P03 (D-64) — 124/519 + 414 |
| Next Milestone | UI-010-P04 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-010) |
| Risk Level | Low (keyboard/focus hardening — presentation interaction, no business logic) |

---

## 2. PHASE OBJECTIVE

Harden **keyboard interaction and focus management** across the AXIOM workstation by validating **focus traps on all modals/drawers** (`Dialog`, `CommandPalette`), **focus restoration on dismissal**, **visible focus rings** (`var(--ix-color-focus)` `#8CC2FF`), and **comprehensive keyboard shortcuts** (`Ctrl+K`, `Escape`, `Tab`/`Shift+Tab`, `Enter`/`Space`, `ArrowUp`/`ArrowDown`) — per WCAG 2.1.1 (Keyboard), 2.4.7 (Focus Visible), 2.4.3 (Focus Order) and `08_UI_UX_SPEC.md`.

This phase is **keyboard/focus hardening, not responsive, feedback, or high-contrast work.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Focus Trap Hardening — `Dialog` + `CommandPalette` ( + `Select` if needed)** | Verify `Dialog` `role="dialog"` `aria-modal="true"` focus trap cycles `Tab`/`Shift+Tab` strictly within modal; `CommandPalette` `Ctrl+K` overlay same trap; `Escape` closes any trapped overlay + restores focus |
| 2 | **Focus Restoration on Dismissal** | On `Dialog` `onClose` (via `Escape`, backdrop click, close Button) and `CommandPalette` `onClose` (via `Escape`), focus returns to the **previously active trigger element** (the Button/link that opened it) — via `useRef` trigger storage + `focus()` on close |
| 3 | **Visible Focus Rings** | All focusable primitives (`Button`, `Input`, `Select` trigger, `Panel`/`Collapsible` triggers, `Dialog` close, `Toast` dismiss) render `outline: 2px solid var(--ix-color-focus)` `#8CC2FF` + `outline-offset: 2px` + `border-radius: var(--ix-radius-sm)` — via `var(--ix-color-focus)` only |
| 4 | **Global Keyboard Shortcuts Registry — `useKeyboardShortcuts.ts` (or `keyboardShortcuts.ts`)** | Centralized shortcut manager: `Ctrl+K` (or `Cmd+K` on mac) opens `CommandPalette`; `Escape` closes topmost overlay (`Dialog` → `CommandPalette` → `Toast` focused) in LIFO order; `Tab`/`Shift+Tab` order verified logical per 08 ( Regions A→B→C→D→E); `ArrowUp`/`ArrowDown` navigates `Select` options / `CommandPalette` list; `Enter`/`Space` activates focused control |
| 5 | **Token Consumption Enforcement** | All keyboard/focus primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `workstation/accessibility/` + `components/ui/` |
| 6 | **Comprehensive Keyboard/Focus Tests** | Per-component suites covering focus trap, restoration, `Escape`, `Ctrl+K`, `Tab` order, `Enter`/`Space`, `Arrow` |
| 7 | **Evidence Package** | Logs committed to `docs/evidence/ui010/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Screen-reader live regions (`RouteAnnouncer` `aria-live="polite"`/`assertive` for route transitions) | **UI-010-P05** scope — P04 is keyboard/focus only |
| 2 | `prefers-contrast` high-contrast theme overrides (`@media (prefers-contrast: more)`) | P05 scope |
| 3 | `prefers-reduced-motion` beyond existing `120ms`→`0ms` (already in P05 overlays) | P05 scope (already satisfied in P01) |
| 4 | Whole-surface WCAG axe audit across all 124 suites | **P06** scope — P04 is keyboard/focus hardening |
| 5 | `EmptyState` / `RouteAnnouncer` / high-contrast components | P05 scope |
| 6 | Responsive breakpoint tokens redefinition (`--ix-breakpoint-*`) or panel collapse reflow | **P02 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P04 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |
| 11 | Mobile <768px companion viewports | **DEFERRED** per Design Plan §9 (post-1.0) |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Keyboard / Focus Architecture (Per Design Plan §5 P04 + WCAG 2.1.1/2.4.3/2.4.7)

- **Location (Recommended):** `frontend/src/workstation/accessibility/` — `useKeyboardShortcuts.ts` (or `keyboardShortcuts.ts`) + `focusTrap.ts` helper (if needed); DA may alternatively place `useKeyboardShortcuts` in `frontend/src/hooks/` if reusing existing hooks, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **Focus Trap:** `Dialog` (already in P05) must trap `Tab`/`Shift+Tab` within modal content when `open` — first `Tab` lands on close Button or first focusable, last `Tab` cycles to first, `Shift+Tab` reverse cycles to last. Implement via `useRef` container + `keydown` handler for `Tab` (prevent default if at boundary) — or reuse existing `Dialog` focus trap logic and add `CommandPalette` trap if not already. `CommandPalette` overlay must trap same way.
- **Focus Restoration:** On `Dialog` `onClose` (via `Escape`, backdrop click, close Button) and `CommandPalette` `onClose` (via `Escape`), `previouslyActiveElementRef.current?.focus()` — where `previouslyActiveElementRef` is captured on `open` (`document.activeElement`). Must handle case where trigger was removed (fallback to `body` or `SkipLink`).
- **Visible Focus Rings:** `Button`, `Input`, `Select` trigger, `Collapsible` trigger, `Panel` `collapsible` trigger, `Dialog` close, `Toast` dismiss all render `outline: 2px solid var(--ix-color-focus)` `#8CC2FF` + `outline-offset: 2px` + `border-radius: var(--ix-radius-sm)` — via `var(--ix-color-focus)` only, not hardcoded `#8CC2FF` outside `tokens.css`.
- **Global Shortcuts:** `useKeyboardShortcuts` registers `keydown` on `window`: `Ctrl+K` (or `Meta+K` for mac) → `event.preventDefault()` + open `CommandPalette`; `Escape` → close topmost overlay in LIFO stack (`Dialog` wins over `CommandPalette` wins over focused `Toast`); no other shortcuts (`Tab`/`Shift+Tab`/`Enter`/`Space`/`Arrow` are native, not global). Must not intercept `Tab` globally — only `Ctrl+K`/`Escape`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/accessibility/` or `hooks/`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; keyboard/focus is presentation interaction, not business logic.

### 4.3 Interaction Contracts

| Component / Hook | Contract |
|-----------|----------|
| `useKeyboardShortcuts({ onOpenPalette, onCloseTopmost })` | `onOpenPalette: () => void` (for `Ctrl+K`) + `onCloseTopmost: () => void` (for `Escape`) — registers `window` `keydown` listener, cleans up on unmount; `Ctrl+K` prevents default + calls `onOpenPalette`; `Escape` calls `onCloseTopmost` (LIFO stack managed by DA) |
| `Dialog` focus trap | `open: boolean` + `onClose` + `initialFocusRef?` + `finalFocusRef?` (optional trigger ref) — when `open`, `Tab` cycles within, `Escape` → `onClose` + focus restoration to `finalFocusRef` or `previouslyActiveElement` |
| `CommandPalette` focus trap | Same as Dialog — when `open`, trap + `Escape` → `onClose` + restore |
| `SkipLink` (P01) | Still first `Tab` on page load — `Tab` order `SkipLink` → `Region A` → `Region B` → `Region C` → … must remain logical per 08 |
| Visible focus | `Button`/`Input`/`Select` trigger/`Collapsible` trigger/`Dialog` close all render `outline: 2px solid var(--ix-color-focus)` on `:focus-visible` (not just `:focus`) — `:focus-visible` for keyboard-only focus ring, not mouse click |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in keyboard/focus module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/accessibility/` + `frontend/src/hooks/` (if used) — 0 matches |
| 4 | No `eval` / `new Function` in module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/accessibility/` + `frontend/src/hooks/` + `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |
| 7 | No credential exposure via focus logging (no `value` of `<input>` in console/DOM attributes) | Code review — `useKeyboardShortcuts` must not log input values |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — keyboard/focus module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — keyboard/focus module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Focus Trap | `Dialog` + `CommandPalette` `Tab`/`Shift+Tab` cycles strictly within modal while `open` — no focus escape to `body` behind overlay | WCAG 2.4.3 Focus Order, 08 |
| U-2 | Focus Restoration | On `Dialog`/`CommandPalette` `onClose` (via `Escape`, backdrop click, close Button), focus returns to previously active trigger element (`Button` that opened it) | WCAG 2.4.3 |
| U-3 | Focus Visibility | All focusable primitives (`Button`, `Input`, `Select` trigger, `Collapsible` trigger, `Dialog` close) render `outline: 2px solid var(--ix-color-focus)` `#8CC2FF` + `outline-offset` on `:focus-visible` (keyboard-only) | WCAG 2.4.7 Focus Visible, 08 |
| U-4 | Keyboard Navigation | `Tab`/`Shift+Tab` traverses panel frames → `DataTable` headers → pagination + overlay actions at any width; `Ctrl+K` opens `CommandPalette`; `Escape` closes topmost overlay LIFO; `Enter`/`Space` activates focused control; `ArrowUp`/`ArrowDown` navigates `Select` options / `CommandPalette` list | WCAG 2.1.1 Keyboard, 08 keyboard |
| U-5 | Motion Restraint | No new motion introduced; `Dialog` backdrop/content `120ms` respected; `prefers-reduced-motion` still → `0ms` (P01 tokens) | 08 motion |
| U-6 | ARIA (Existing) | `Dialog` `role="dialog"` `aria-modal="true"` `aria-labelledby`/`aria-describedby` already in P05 — P04 validates focus trap preserves ARIA | WCAG 1.3.1/4.1.3 |
| U-7 | No Color-Alone | Focus ring `outline` is shape + color, not color alone — text+`◆◆◆`+`%` already in P05 — never color alone | 02 §Design, 08 |
| U-8 | Dark-First | Focus rings render correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `Dialog.focusTrap.test.tsx` (or within `Dialog.test.tsx`) | Focus trap `Tab`/`Shift+Tab` cycles within `Dialog` when `open` — first `Tab` lands on close Button or first focusable, last `Tab` cycles to first, `Shift+Tab` reverse cycles to last, no focus escape to `body` |
| T-2 | `Dialog.focusRestoration.test.tsx` | Focus restoration on `onClose` (via `Escape`, backdrop click, close Button) — focus returns to trigger `Button` (`document.activeElement` after close equals trigger) |
| T-3 | `useKeyboardShortcuts.test.tsx` | `Ctrl+K` opens `CommandPalette` (calls `onOpenPalette`), `Escape` closes topmost overlay (calls `onCloseTopmost` LIFO), no other key intercepted |
| T-4 | `focusVisibility.test.tsx` (or within `SkipLink.test.tsx` / `Button.test.tsx`) | Visible focus rings `var(--ix-color-focus)` on `Button`, `Input`, `Select` trigger, `Collapsible` trigger, `Dialog` close on `:focus-visible` — `outline: 2px solid var(--ix-color-focus)` + `outline-offset` |
| T-5 | `ui010_p04_security_invariants.test.ts` | S-1 whole-repo actuation + S-2 LLM + S-3 sandbox + S-4 ad-hoc hex in keyboard/focus module + S-5 secrets — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **519 tests — 100% pass** (or 519+ with accounting — see §8) — P04 adds keyboard/focus tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Keyboard/focus hardening is additive — **0 removed / 0 modified** expected for existing tests (124 suites 519 tests from UI-010-P03). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`Dialog` with `open={false}` → focus trap not active ( `Tab` not trapped) + no `aria-modal`; `Dialog` `backdropClose=false` (if supported) → backdrop click does NOT call `onClose`; `useKeyboardShortcuts` with no `onOpenPalette` → `Ctrl+K` does nothing; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui010/` on `main` — continue `ui010` directory)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **519+ pass** — full log (must show 124 suites/519 baseline + new P04 suites) | `docs/evidence/ui010/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui010/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui010/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui010/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui010/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/accessibility/` + `hooks/` | Level II | 0 | `docs/evidence/ui010/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/accessibility/` + `hooks/` | Level II | 0 | `docs/evidence/ui010/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/accessibility/` + `hooks/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui010/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui010/grep_secrets.log` |
| E-10 | Accessibility audit evidence | Level II | WCAG 2.1.1/2.4.7 + focus trap + restoration + `Ctrl+K`/`Escape` — via `Dialog.focusTrap.test.tsx` + `useKeyboardShortcuts.test.tsx` + optional `accessibility.log` | `docs/evidence/ui010/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui010/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-010-P04.md` with 20 sections | `DELIVERY_REPORT_UI-010-P04.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `Dialog` focus trap + restoration DOM queries via `Dialog.focusTrap.test.tsx`/`focusRestoration.test.tsx`) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. Continue evidence directory `docs/evidence/ui010/` (same as P01→P03).

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

**Expected:** `VITEST_EXIT:0` with **519+ pass** (P04 will be 124→~128 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `workstation/accessibility/` + `hooks/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `workstation/accessibility/` + `hooks/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/accessibility/ frontend/src/hooks/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
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

DA shall produce `DELIVERY_REPORT_UI-010-P04.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-010-P04 — Keyboard Interaction & Focus Management Hardening |
| 2 | Governing Build Order | `BUILD_ORDER_UI-010-P04` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` §5 P04 + §10 P01 foundation |
| 4 | Previous Baseline | UI-010-P03 D-64: 124 suites / 519 tests · 414 backend · feedback states |
| 5 | Implementation Summary | What keyboard/focus hardening was built (focus trap, restoration, visible focus, global shortcuts) + token consumption |
| 6 | Files Created | List with nature (expected focus trap + keyboard hook + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `Dialog.tsx`/`CommandPalette` integration + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (7 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 124/519 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 124/519 vs current (must be ≥124/519) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0 in `workstation/accessibility/`+`hooks/`) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + focus trap/restoration + shortcuts evidence |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Keyboard & focus complete; screen-reader/high-contrast in P05” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-010-P05 Screen-Reader, High-Contrast & Reduced-Motion Compliance |
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
- Frontend: 124 suites / 519 tests
- Backend: 414 tests

New tests physically added:
- [N tests across Dialog.focusTrap/Dialog.focusRestoration/useKeyboardShortcuts/focusVisibility suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [124 or 124+N] suites / [519 or 519+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-64 UI-010-P03 (124/519 + 414)
- Commit: [current HEAD]

Inherited Components: SkipLink.tsx/.css, accessibilityAudit.test.tsx, breakpoint tokens (P02), EmptyState.tsx, DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), Panel/PanelHeader/PanelActionBar/Collapsible (P03), tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 124 suites / 519 frontend + 414 backend (D-64)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P10P03-01 (CSS grid/viewport harmonization — documented), O-P10P03-02 (evidence on main continuity)

New Phase Scope: Keyboard & Focus — focus trap + restoration + visible focus + global shortcuts (7 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P04, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-010-P04 APPROVED** (version increment per governance, e.g., 8.80.0) |
| `CHANGELOG.md` | Record P04 completion |
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
[ BUILD_ORDER_UI-010-P04 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Keyboard/Focus Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P04 Determination ]
         ↓
[ BUILD_ORDER_UI-010-P05 — Screen-Reader, High-Contrast & Reduced-Motion Compliance ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Focus trap `Tab`/`Shift+Tab` cycles strictly within `Dialog` + `CommandPalette` while `open` — no focus escape to `body` | Mandatory | `Dialog.focusTrap.test.tsx` |
| AC-2 | Focus restoration on `onClose` (via `Escape`, backdrop click, close Button) — focus returns to previously active trigger element | Mandatory | `Dialog.focusRestoration.test.tsx` |
| AC-3 | Visible focus rings `var(--ix-color-focus)` `#8CC2FF` on all interactive primitives (`Button`, `Input`, `Select` trigger, `Collapsible` trigger, `Dialog` close) on `:focus-visible` | Mandatory | `focusVisibility.test.tsx` |
| AC-4 | Global shortcuts `Ctrl+K` opens `CommandPalette` + `Escape` closes topmost overlay LIFO (Dialog → CommandPalette → focused Toast) | Mandatory | `useKeyboardShortcuts.test.tsx` |
| AC-5 | Pure token consumption: 0 ad-hoc hex in `workstation/accessibility/` + `hooks/` (outside `tokens.css`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-6 | Constitutional invariants: Zero actuation, zero external LLMs, zero `dangerouslySetInnerHTML`/`eval` in keyboard/focus module | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-7 | Frontend regression baseline ≥519 tests — 100% pass; Backend 414 pass; `tsc` and `vite build` exit 0 | Mandatory | E-1/E-2/E-3 |
| AC-8 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P04 implementation only** — no P05–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L, D-61 APPROVED WITH OBSERVATIONS) |
| P04 Design | §5 Phase Breakdown — P04 Keyboard Interaction & Focus Management Hardening |
| Preceding Baseline | D-64: 124 suites / 519 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 + Workspace Shell Regions A–F |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — §7 User Experience & Accessibility — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-64 (124/519) preserved as previous baseline |
| §3 Single Active Phase | **P04 = ACTIVE**, P05–P06 = NOT AUTHORIZED, UI-010-P01→P03 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P04 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-64 124/519 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no screen-reader/high-contrast/whole-surface work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P05 not authorized until P04 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui010/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-64 preserved |
| §24 P04 Controls | Applied — focus trap + restoration + visible focus + shortcuts |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P04 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-010-P04**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

