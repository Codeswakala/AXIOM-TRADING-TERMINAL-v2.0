# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P05`

**Authority:** Independent Technical Review & Governance Authority (ITRTA)
**Determination:** D-58 — UI-009-P04 **APPROVED** (105 suites / 454 tests · 414 backend · exit 0) — Observation O-P09P04-01 (evidence logs documentary tier, continuity)
**Phase:** UI-009-P05 — Modals, Overlays & Feedback Systems
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §5/P05 — Modals, Overlays & Feedback Systems)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried to UI-009)
**Preceding Milestone:** UI-009-P04 (D-58 APPROVED) — 105 suites / 454 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 105/454 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P05 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P05` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — UI-009 Design Plan APPROVED WITH OBSERVATIONS (O-009-01, O-009-02 — closed D-55) |
| Preceding Milestone | UI-009-P04 (D-58) — 105/454 + 414 |
| Next Milestone | UI-009-P05 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (overlay primitives — presentation feedback, no persistence) |

---

## 2. PHASE OBJECTIVE

Standardize **modal, overlay, and feedback primitives** for AXIOM — **Dialog**, **Command Palette styling**, **Skeleton**, **Toast**, and **Error Recovery Banner** — using the **P01 5-tier tokens** and **P02–P04 primitives** (`Panel`, `Card`, `Button`, `Badge`) — overlay presentation only, no backend mutation, with WCAG 2.1 AA focus management and reduced-motion.

This phase is **overlay/feedback standardization, not whole-surface audit (P06) or data table rework (P04).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Dialog — `Dialog.tsx` + `Dialog.css`** | Modal overlay primitive: `open` (`boolean` controlled), `onClose` (`() => void` **required** when `open`), `title` (required) + `description?` (`aria-labelledby`/`aria-describedby` linking), `children` (body), `footer?` slot (`PanelActionBar` or `Button` group), `size?` (`sm`/`md`/`lg`/`full`), focus trap (`Tab` cycles within, `Shift+Tab` reverse), `Escape` closes, `backdrop` click closes (if `onClose` provided), `role="dialog"` `aria-modal="true"`, portal to `document.body`, motion `var(--ix-motion-fast) 120ms` → `0ms` reduced |
| 2 | **Command Palette Styling — `CommandPalette.css` (or `CommandPaletteOverlay.tsx` enhancement)** | Tokenized styling harmonization for existing Command Palette overlay (33 quick actions): background `var(--ix-bg-surface-raised)`, border `var(--ix-border-subtle)`, `var(--ix-shadow-overlay)`, spacing `var(--ix-space-*)`, focus `var(--ix-color-focus)` — **no new palette logic, no new commands** — styling only, reusing P02 search/palette routing |
| 3 | **Skeleton — `Skeleton.tsx` + `Skeleton.css`** | Loading placeholder primitive: `variant` (`text`/`rect`/`circle`), `width`/`height` (via `var(--ix-space-*)` or `px` token), `count?` (repeated lines), `aria-busy="true"` + `aria-label="Loading"`, shimmer via `var(--ix-color-surface-raised)` + `var(--ix-motion-fast)` → `0ms` reduced, 0 ad-hoc hex |
| 4 | **Toast — `Toast.tsx` + `Toast.css` + `ToastProvider.tsx` (or `ToastStack.tsx`)** | Feedback primitive: `variant` (`info`/`success`/`warning`/`error`), `title` + `description?` + `icon` via `Badge`/`StatusChip` pattern (text+symbol), `role="status"` (`info`/`success`) vs `role="alert"` (`warning`/`error`), `aria-live="polite"` vs `aria-live="assertive"`, `onDismiss` + auto-dismiss optional, `Escape` dismisses focused toast, stacked via `aria-live` region, no actuation controls inside |
| 5 | **Error Recovery Banner — `ErrorBanner.tsx` + `ErrorBanner.css`** | Inline error primitive: `variant` `error`/`warning`, `title` + `message` + `action?` (`Button` retry) + `onDismiss?`, `role="alert"` `aria-live="assertive"`, icon + text (never color alone), focus visible, dismissible via `Enter`/`Space` on close button |
| 6 | **Token Consumption Enforcement** | All overlay/feedback primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `components/ui/` |
| 7 | **Comprehensive State Tests** | Per-component suites covering rendering + props + focus trap/keyboard + ARIA + motion + token consumption |
| 8 | **Evidence Package** | Logs committed to `docs/evidence/ui009/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Whole-surface harmonization & completion checkpoint (audit of UI-009 P01→P06, WCAG audit across all workspaces) | **UI-009-P06** scope |
| 2 | Data tables & visualization grids (`DataTable`, `SortableHeader`, `Pagination`, `formatters.ts` tabular-nums) | **P04 already COMPLETE** — reuse |
| 3 | Workspace panel frames (`Panel`/`PanelHeader`/`PanelActionBar`/`Collapsible`) | **P03 already COMPLETE** — reuse |
| 4 | Atomic primitives (`Button`/`Input`/`Select`/`Badge`/`Card`/`StatusChip`/`Tooltip`/`Accordion`) | **P02 already COMPLETE** — reuse (Button is used *inside* Dialog/Pagination/Toast/ErrorBanner) |
| 5 | 5-tier token hierarchy or `theme.ts` contracts | **P01 already COMPLETE** — reuse, do not redefine |
| 6 | New backend endpoints, migrations, schema changes | No persistence change |
| 7 | WebSocket / real-time push | Not in P05 design |
| 8 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 9 | External LLM integration (OpenAI/Anthropic/LangChain etc.) | Constitutionally prohibited — 12 Part I §5 |
| 10 | Order / trade / execution / broker controls | Absolutely prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Overlay / Feedback Architecture (Per Design Plan §5 P05)

- **Location:** `frontend/src/components/ui/` (same library path as P02 atomic + P03 panels + P04 tables — `frontend/src/components/ui/` declared in P02) — all overlay primitives **must live in the same library path** for single import surface.
- **Portal & Focus:** `Dialog` portals to `document.body`; focus trap cycles `Tab`/`Shift+Tab` within dialog when `open`; `Escape` closes via `onClose`; `backdrop` click closes only if `onClose` provided; initial focus lands on `Dialog` title or first focusable; on `open→false`, focus returns to trigger. `Toast` lives in `aria-live` region outside dialog.
- **Token Consumption:** Every visual value (overlay `background: var(--ix-bg-surface-raised)`, `border: var(--ix-border-subtle)`, `shadow: var(--ix-shadow-overlay)`, `padding: var(--ix-space-*)`, focus `var(--ix-color-focus)`, motion `var(--ix-motion-fast)`) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` spacing outside `var(--ix-space-*)`, no ad-hoc `transition` duration outside `var(--ix-motion-fast)`.
- **No Runtime Style Injection:** No `dangerouslySetInnerHTML` for style/theme injection; no `eval`/`new Function`; no raw `<script>`; tokens are static CSS custom properties. `Dialog` `title`/`description` are ReactNode strings (text), not HTML.
- **Composition:** `Dialog` reuses `PanelHeader`/`PanelActionBar`/`Card`/`Button` internally; `Toast` reuses `Badge`/`StatusChip` pattern (text+`◆◆◆`); `ErrorBanner` reuses `Card` variant; `Skeleton` is pure placeholder.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); bounded context `frontend/src/components/ui/` isolated; no new bounded context; no circular deps; no backend coupling; `ToastProvider` (if used) is React context provider for stacking — not business logic; `CommandPalette` styling is CSS-only harmonization, not new routing.

### 4.3 Interaction Contracts

| Component | Contract |
|-----------|----------|
| `Dialog` | `open: boolean` + `onClose?: () => void` + `title: string` + `description?: string` + `children: ReactNode` + `footer?: ReactNode` + `size?: "sm"|"md"|"lg"|"full"` + `backdropClose?: boolean` (default true if `onClose`) — `role="dialog"` `aria-modal="true"` `aria-labelledby` title id + `aria-describedby` description id; `Escape` + backdrop click → `onClose` |
| `CommandPalette` (styling) | No new props — CSS harmonization only; consumes existing palette's `open`/`onSelect`/`options[]` routing; styling via `CommandPalette.css` token overrides |
| `Skeleton` | `variant?: "text"|"rect"|"circle"` + `width?: string` + `height?: string` + `count?: number` (default 1) + `aria-busy="true"` + `aria-label="Loading"` — shimmer via `var(--ix-color-surface-raised)` |
| `Toast` | `variant: "info"|"success"|"warning"|"error"` + `title: string` + `description?: string` + `onDismiss?: () => void` + `autoDismissMs?: number` — `role="status"` (`info`/`success`) vs `role="alert"` (`warning`/`error`) + `aria-live` + `aria-atomic="true"`; `Escape` dismisses focused toast |
| `ToastProvider` / `ToastStack` | `toasts: Toast[]` + `setToasts`; `aria-live="polite"` region for `info`/`success`, `aria-live="assertive"` for `warning`/`error` — stacked `role="region"` `aria-label="Notifications"` |
| `ErrorBanner` | `variant: "error"|"warning"` + `title: string` + `message: string` + `action?: { label, onClick }` (Button) + `onDismiss?: () => void` — `role="alert"` `aria-live="assertive"` + dismissible `Button` with `aria-label="Dismiss"` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in overlay/feedback primitives | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` — 0 matches |
| 4 | No `eval` / `new Function` in primitives | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/components/ui/` — 0 matches (all colors via `var(--ix-*)`) |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/components/ui/` → exit 1 (0 matches) — proves token consumption |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Brand Fidelity | All overlay/feedback primitives via tokens (`--ix-bg-surface-raised`, `--ix-border-subtle`, `--ix-shadow-overlay`, `--ix-space-*`, `--ix-color-accent`, `--ix-color-success/warning/critical`) — no inline hex | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast | Text/background >4.5:1 (Dialog title/description, Toast title/message, ErrorBanner title/message, Skeleton not applicable) — inherited from P01 `7.2:1`/`6.8:1` for metadata | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding | Toast `info`/`success`/`warning`/`error` + ErrorBanner `warning`/`error` include text label + icon (`StatusChip` pattern `◆◆◆`) + `aria-live` role — never color alone | 02 §Design, 08 |
| U-4 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` on `Dialog` close button, `Toast` `onDismiss` button, `ErrorBanner` `onDismiss`/`action` Button, `Skeleton` not focusable (but `aria-busy`) | WCAG 2.4.7 |
| U-5 | Motion Restraint | `Dialog` backdrop + content transitions via `var(--ix-motion-fast)` `120ms`; `Toast` enter/exit `120ms`; `Skeleton` shimmer `120ms`; all respect `@media (prefers-reduced-motion: reduce)` → `0ms` | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` cycles within `Dialog` (focus trap); `Escape` closes `Dialog` + focused `Toast`; `Tab` navigates `Toast` dismiss buttons + `ErrorBanner` `onDismiss`/`action`; `Enter`/`Space` activates `ErrorBanner` action | 08 keyboard |
| U-7 | ARIA | `Dialog` `role="dialog"` `aria-modal="true"` `aria-labelledby`/`aria-describedby`; `Toast` `role="status"` vs `role="alert"` + `aria-live="polite"` vs `"assertive"` + `aria-atomic`; `ErrorBanner` `role="alert"` `aria-live="assertive"`; `Skeleton` `aria-busy="true"` `aria-label` | WCAG / 08 |
| U-8 | Dark-First | Overlays render correctly on `backdrop` dim (`rgba(0,0,0,0.5)`) + `--ix-bg-surface-raised` `#1A1F2C` + `.theme-light` override | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `Dialog.test.tsx` | `open` renders/closes + `role="dialog"` `aria-modal` + `aria-labelledby`/`aria-describedby` + `Escape` closes + backdrop click closes (when `onClose`) + focus trap `Tab`/`Shift+Tab` + `size` variants + footer slot |
| T-2 | `CommandPaletteStyling.test.tsx` (or within `Dialog.test.tsx` / visual) | Token consumption — no ad-hoc hex in `CommandPalette.css` + focus/motion tokens applied (or `CommandPalette.test.tsx` styling override proof) |
| T-3 | `Skeleton.test.tsx` | Variants `text`/`rect`/`circle` + `width`/`height` + `count` + `aria-busy="true"` + `aria-label="Loading"` + shimmer class |
| T-4 | `Toast.test.tsx` | Variants `info`/`success`/`warning`/`error` + `role="status"` vs `role="alert"` + `aria-live` + `aria-atomic` + `onDismiss` + `Escape` dismisses focused toast + auto-dismiss optional |
| T-5 | `ErrorBanner.test.tsx` | Variants `error`/`warning` + `role="alert"` `aria-live="assertive"` + `title`/`message` + `action` Button `onClick` + `onDismiss` + `aria-label="Dismiss"` + icon+text |
| T-6 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **454 tests — 100% pass** (or 454+ with accounting — see §8) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Overlay primitives are additive — **0 removed / 0 modified** expected for existing tests (105 suites 454 tests from P04). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`Dialog` with `open={false}` → not in DOM (or `hidden`) + no focus trap; `Dialog` `backdropClose=false` (if supported) → backdrop click does NOT call `onClose`; `Toast` `autoDismissMs` missing → not auto-dismissed; `Skeleton` `count=0` → 0 placeholders.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **454+ pass** — full log (must show 105 suites/454 baseline + new P05 suites) | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `#[0-9A-F]{3,6}` in `components/ui/` | Level II | 0 (proves token consumption) | `docs/evidence/ui009/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Accessibility spot-check | Level II | WCAG 2.1 AA — contrast >4.5:1 + focus + ARIA + keyboard (axe or `Dialog.test.tsx`/`Toast.test.tsx` excerpt) | `docs/evidence/ui009/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P05.md` with 20 sections | `DELIVERY_REPORT_UI-009-P05.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — DOM snapshots for Dialog focus trap / Toast `aria-live` if applicable, e.g., Storybook snapshots) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4.

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs. **For reliable cross-platform `grep` on Windows, use *Git Bash* (bundled with Git for Windows) — it runs identical Bash commands as DA's Linux.**

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui009/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui009/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui009/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui009/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui009/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **454+ pass** (P05 will be 105→~110 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `components/ui/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | **Git Bash:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**Exit code contract (both platforms, identical):** **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion fixtures, documented).**

#### 3. Documentation Diffs

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui009/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui009/changelog_diff.log` |

**All logs must be committed to `docs/evidence/ui009/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both deterministic. **Git Bash on Windows gives identical `grep` exit codes as DA's Linux** — strongly recommended.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-009-P05.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P05 — Modals, Overlays & Feedback Systems |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P05` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §5 P05 (and §10 P01 token foundation) |
| 4 | Previous Baseline | P04 D-58: 105 suites / 454 tests · 414 backend · panel tables 6 suites/25 tests |
| 5 | Implementation Summary | What overlay/feedback primitives were built (Dialog, CommandPalette styling, Skeleton, Toast, ErrorBanner) + token consumption |
| 6 | Files Created | List with nature (expected 5+ overlay files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe `Panel` integration) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (8 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 105/454 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 105/454 vs current (must be ≥105/454) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + overlay snapshots (Dialog focus trap, Toast `aria-live`) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Overlays complete; whole-surface audit in P06” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-009-P06 Whole-Surface Harmonization & Completion Checkpoint |
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
- Frontend: 105 suites / 454 tests
- Backend: 414 tests

New tests physically added:
- [N tests across Dialog/Skeleton/Toast/ErrorBanner suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [105 or 105+N] suites / [454 or 454+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-58 UI-009-P04 (105/454 + 414)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), DataTable/SortableHeader/Pagination/formatters (P04), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 105 suites / 454 frontend + 414 backend (D-58)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P09P04-01 (evidence on main continuity)

New Phase Scope: Modals & Overlays — Dialog/CommandPalette/Skeleton/Toast/ErrorBanner (8 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P05, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P05 APPROVED** (version increment per governance, e.g., 8.75.0) |
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
[ BUILD_ORDER_UI-009-P05 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Overlay/Feedback Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P05 Determination ]
         ↓
[ BUILD_ORDER_UI-009-P06 — Whole-Surface Harmonization & Completion Checkpoint ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Dialog renders `open` + `role="dialog"` `aria-modal` + `aria-labelledby`/`aria-describedby` + `Escape` closes + backdrop click closes (when `onClose`) + focus trap `Tab`/`Shift+Tab` + `size` variants | Mandatory | `Dialog.test.tsx` + E-12 |
| AC-2 | Command Palette styling harmonized via tokens (`--ix-bg-surface-raised` etc.) — 0 ad-hoc hex in `CommandPalette.css` | Mandatory | `CommandPaletteStyling.test.tsx` or visual proof + E-8 |
| AC-3 | Skeleton variants `text`/`rect`/`circle` + `width`/`height` + `count` + `aria-busy`/`aria-label` + shimmer `var(--ix-color-surface-raised)` | Mandatory | `Skeleton.test.tsx` |
| AC-4 | Toast variants `info`/`success`/`warning`/`error` + `role="status"` vs `role="alert"` + `aria-live` + `onDismiss` + `Escape` dismisses focused toast | Mandatory | `Toast.test.tsx` |
| AC-5 | ErrorBanner variants `error`/`warning` + `role="alert"` `aria-live="assertive"` + `title`/`message` + `action` Button + `onDismiss` | Mandatory | `ErrorBanner.test.tsx` |
| AC-6 | All 5 overlay/feedback primitives consume `var(--ix-*)` — 0 ad-hoc hex in `components/ui/` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-7 | Zero actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-8 | Zero LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-9 | 0 `dangerouslySetInnerHTML` + 0 `eval` in `components/ui/` | Mandatory | E-6/E-7 exit 1 |
| AC-10 | Frontend regression 454 pass (or 454+ with accounting) | Mandatory | E-1 vitest.log |
| AC-11 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-12 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking** — one failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P05 implementation only** — no P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P05 Design | §5 Phase Breakdown — P05 Modals, Overlays & Feedback Systems |
| Preceding Baseline | D-58: 105 suites / 454 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-58 (105/454) preserved as previous baseline |
| §3 Single Active Phase | **P05 = ACTIVE**, P06 = NOT AUTHORIZED, P01–P04 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P05 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-58 105/454 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + ad-hoc hex check |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no table/audit work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P06 not authorized until P05 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-58 preserved |
| §24 P05 Controls | Applied — overlay/feedback + token consumption + focus trap |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P05 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P05**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

