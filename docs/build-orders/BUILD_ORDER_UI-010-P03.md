# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-010-P03`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-63 — UI-010-P02 **APPROVED** (121 suites / 504 tests · 414 backend · exit 0) — Observation O-P10P02-01 (evidence logs documentary tier, continuity)
**Phase:** UI-010-P03 — Feedback States Standardization (Loading, Empty, Error, Toast)
**Governing Design Plan:** `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (Approved per D-61, §5/P03 — Feedback States Standardization)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010)
**Preceding Milestone:** UI-010-P02 (D-63 APPROVED) — 121 suites / 504 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 121/504 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P03 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-010-P03` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-61 — UI-010 Design Plan APPROVED WITH OBSERVATIONS (O-010-01 sticky-header — closed D-63 via `--ix-table-sticky-header-z-index:2`) |
| Preceding Milestone | UI-010-P02 (D-63) — 121/504 + 414 |
| Next Milestone | UI-010-P03 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-010) |
| Risk Level | Low (feedback-state harmonization — presentation consistency, no business logic) |

---

## 2. PHASE OBJECTIVE

Standardize **feedback states — loading, empty, error, and notification (toast) — across all 7 workspace pages** by harmonizing `Skeleton` (loading `aria-busy`), `EmptyState` (honest `role="status"`), `ErrorBanner` (`role="alert"` `aria-live="assertive"`), and `Toast`/`ToastStack` (`polite` vs `assertive`) primitives via the **P01 5-tier tokens** and **P02–P05 primitives** — per WCAG 1.3.1 / 4.1.3 and `12` Part VII §12 checklist.

This phase is **feedback-state standardization across workspaces, not new responsive, keyboard, or whole-surface audit.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **`EmptyState` — `EmptyState.tsx` + `EmptyState.css`** | Reusable empty-state primitive: `icon?` + `title` (required, `<h3>`) + `description?` + `action?` (`Button` retry) + `role="status"` + `aria-live="polite"` + `aria-label`; variants `default` / `compact`; `var(--ix-*)` only |
| 2 | **Feedback States Standardization Across 7 Workspaces** | Harmonize `Skeleton` (`aria-busy`), `EmptyState` (`role="status"`), `ErrorBanner` (`role="alert"`), `Toast`/`ToastStack` (`polite` vs `assertive`) usage across at least **7 workspace pages**: `/charts` (`ChartWorkspacePage.tsx`), `/intelligence` (`InstitutionalIntelligencePage.tsx`), `/investigate` (`SignalInvestigationPage.tsx`), `/governance` (`GovernanceEvidencePage.tsx`), `/trade-plans` (`TradePlanningPage.tsx`), `/journal` (`ManualJournalPage.tsx`), `/compare-scenarios` or `/research-management` — replace raw text ad-hoc empty/error with `EmptyState`/`ErrorBanner` |
| 3 | **Token Consumption Enforcement** | All feedback primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `workstation/` + `components/ui/` (outside `tokens.css`) |
| 4 | **Comprehensive State Tests** | Per-component suites covering rendering + `role`/`aria-live` + `action`/`onDismiss` + token consumption |
| 5 | **Evidence Package** | Logs committed to `docs/evidence/ui010/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Keyboard shortcut manager, global `Ctrl+K`, focus trap validation beyond existing `Dialog`/`SkipLink`, focus restoration | **UI-010-P04** scope — P03 is feedback states only |
| 2 | Screen-reader live regions beyond `EmptyState`/`ErrorBanner`/`Toast` already in scope (`RouteAnnouncer` `aria-live` for route transitions) | P05 scope — P03 covers feedback states only |
| 3 | `prefers-contrast` high-contrast theme overrides, `@media (prefers-contrast: more)` | P05 scope |
| 4 | Whole-surface WCAG axe audit across all 121 suites | **P06** scope — P03 is feedback-state harmonization |
| 5 | `RouteAnnouncer` / high-contrast components | P05 scope |
| 6 | Responsive breakpoint tokens redefinition (`--ix-breakpoint-*`) or panel collapse reflow | **P02 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P03 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |
| 11 | `EmptyState` for mobile <768px companion viewports | **DEFERRED** per Design Plan §9 (post-1.0) — P03 targets desktop/laptop 1280/1024 |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Feedback States Architecture (Per Design Plan §5 P03 + WCAG 1.3.1/4.1.3)

- **Location:** `frontend/src/components/ui/` — `EmptyState.tsx`/`EmptyState.css` (new primitive alongside P02 `Skeleton`/`Toast`/`ErrorBanner`); `frontend/src/workstation/` workspace pages (e.g., `InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `SignalInvestigationPage.tsx`, `GovernanceEvidencePage.tsx`, `TradePlanningPage.tsx`, `ManualJournalPage.tsx`, `ScenarioComparisonPage.tsx`/`ResearchManagementPage.tsx`) for harmonization — DA shall declare chosen workspace file set in Delivery Report §6 and use it consistently. Presentation Layer only.
- **EmptyState Contract:** `icon?: ReactNode` + `title: string` (renders `<h3>`) + `description?: string` + `action?: { label, onClick }` (`Button`) + `variant?: "default"|"compact"` — wrapper `role="status"` `aria-live="polite"` `aria-label` (title or `Empty state: ${title}`), `description` as `<p>` if present, `action` as `Button` with `onClick`.
- **Standardization Rule:** Every workspace page's empty data branch (`rows.length === 0` or `data === null`) **must render** `EmptyState` with honest text (e.g., “No research reports available — Create a new report or adjust filters”) **instead of raw `<div>No data</div>`**. `ErrorBanner` (`role="alert"`) already exists from P05 overlay — P03 shall harmonize its usage across workspaces for error branches (`error !== null`). `Skeleton` (`aria-busy`) already exists from P05 — P03 shall harmonize loading branches (`loading === true`). `Toast`/`ToastStack` for notifications remains via `role="status"`/`role="alert"` — P03 harmonizes notification feedback states where applicable.
- **Token Consumption:** Every visual value (background `var(--ix-bg-surface)`, border `var(--ix-border-subtle)`, spacing `var(--ix-space-*)`, text `var(--ix-text-primary)`/`var(--ix-text-muted)`, focus `var(--ix-color-focus)`) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` spacing outside `var(--ix-space-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `components/ui/` + `workstation/` pages); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; `EmptyState` is presentation `role="status"` primitive, not business logic.

### 4.3 Interaction Contracts

| Component | Contract |
|-----------|----------|
| `EmptyState` | `title: string` + `description?: string` + `icon?: ReactNode` + `action?: { label, onClick }` + `variant?: "default"|"compact"` — `role="status"` `aria-live="polite"` `aria-label` + `description` as `<p>` + `action` as `Button` |
| Workspace Pages (harmonized) | `loading` → `Skeleton` `aria-busy="true"`; `empty` → `EmptyState` `role="status"`; `error` → `ErrorBanner` `role="alert"`; notification → `Toast` `role="status"`/`role="alert"` — all via `var(--ix-*)` |
| `Skeleton` (reused) | `variant` `text`/`rect`/`circle` + `aria-busy` + `aria-label="Loading"` — already in P05 |
| `ErrorBanner` (reused) | `variant` `error`/`warning` + `role="alert"` `aria-live="assertive"` + `action` Button — already in P05 |
| `Toast`/`ToastStack` (reused) | `variant` `info`/`success` vs `warning`/`error` + `role="status"` vs `role="alert"` + `aria-live` — already in P05 |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in feedback-state primitives | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` + `frontend/src/workstation/` — 0 matches |
| 4 | No `eval` / `new Function` in primitives | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/components/ui/` + `frontend/src/workstation/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — feedback-state files | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/components/ui/ frontend/src/workstation/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Brand Fidelity | All feedback primitives via tokens (`--ix-bg-surface`, `--ix-text-primary`/`--ix-text-muted`, `--ix-border-subtle`, `--ix-space-*`, `--ix-color-focus`) — no inline hex | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast | Text/background >4.5:1 (EmptyState title/description, ErrorBanner/Toast title/message) — inherited from P01 `7.2:1`/`6.8:1` for metadata | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding | `EmptyState` icon + text + description; `ErrorBanner`/`Toast` still text+`◆◆◆`+`%` + `aria-live` — never color alone | 02 §Design, 08 |
| U-4 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` on `EmptyState` `action` Button + `ErrorBanner` `action`/`onDismiss` + panel frames | WCAG 2.4.7 |
| U-5 | Motion Restraint | No new motion; `EmptyState` fade via `var(--ix-motion-fast)` `120ms` if any → `0ms` reduced (`prefers-reduced-motion`) | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` reaches `EmptyState` `action` Button + `ErrorBanner` `action`/`onDismiss` + `Toast` dismiss | WCAG 2.1.1/2.4.7 |
| U-7 | ARIA | `EmptyState` `role="status"` `aria-live="polite"` + `aria-label`; `ErrorBanner` `role="alert"` `aria-live="assertive"`; `Skeleton` `role="status"` `aria-busy`; `Toast` `role="status"` vs `role="alert"` + `aria-live` | WCAG 1.3.1/4.1.3, 08 |
| U-8 | Dark-First | Empty/error/loading states render correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `EmptyState.test.tsx` | Rendering + `role="status"` `aria-live="polite"` + `aria-label` + `title` (`<h3>`) + `description` + `action` Button `onClick` + variants `default`/`compact` + no color-alone |
| T-2 | Workspace feedback-state integration tests (e.g., `InstitutionalIntelligencePage.feedback.test.tsx` or `feedbackStates.test.tsx` — DA to declare file names, at least **2 workspaces** + `EmptyState` unit) | `loading` → `Skeleton` `aria-busy` + `empty` → `EmptyState` `role="status"` + `error` → `ErrorBanner` `role="alert"` — prove harmonization across at least 2 representative workspaces (e.g., `/intelligence` + `/charts`) plus one direct `EmptyState` unit test; covers `aria-live` `polite` vs `assertive` |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **504 tests — 100% pass** (or 504+ with accounting — see §8) — P03 adds `EmptyState` + harmonization tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Feedback-state harmonization is additive — **0 removed / 0 modified** expected for existing tests (121 suites 504 tests from UI-010-P02). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`EmptyState` without `action` → no Button rendered + `role="status"` still correct; `EmptyState` `variant="compact"` → compact padding via `var(--ix-space-*)`; `DataTable` empty branch → `EmptyState` not raw text; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui010/` on `main` — continue `ui010` directory)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **504+ pass** — full log (must show 121 suites/504 baseline + new P03 suites) | `docs/evidence/ui010/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui010/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui010/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui010/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui010/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` + `workstation/` | Level II | 0 | `docs/evidence/ui010/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` + `workstation/` | Level II | 0 | `docs/evidence/ui010/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `components/ui/` + `workstation/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui010/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui010/grep_secrets.log` |
| E-10 | Accessibility audit evidence | Level II | WCAG 1.3.1/4.1.3 + `EmptyState` `role="status"` + `ErrorBanner` `role="alert"` + `aria-live` — via `EmptyState.test.tsx` + `accessibility.log` | `docs/evidence/ui010/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui010/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-010-P03.md` with 20 sections | `DELIVERY_REPORT_UI-010-P03.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `EmptyState` `role="status"` + `ErrorBanner` `role="alert"` DOM queries via `EmptyState.test.tsx`) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. Continue evidence directory `docs/evidence/ui010/` (same as P01/P02 — do not create new `ui010-p03/`).

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

**Expected:** `VITEST_EXIT:0` with **504+ pass** (P03 will be 121→~123 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui010/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui010/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `components/ui/` + `workstation/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `components/ui/` + `workstation/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ frontend/src/workstation/ 2>&1 \| tee docs/evidence/ui010/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
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

DA shall produce `DELIVERY_REPORT_UI-010-P03.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-010-P03 — Feedback States Standardization (Loading, Empty, Error, Toast) |
| 2 | Governing Build Order | `BUILD_ORDER_UI-010-P03` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` §5 P03 + §10 P01 foundation |
| 4 | Previous Baseline | UI-010-P02 D-63: 121 suites / 504 tests · 414 backend · responsive reflow |
| 5 | Implementation Summary | What feedback-state harmonization was built (EmptyState primitive + workspace empty/error/loading/toast harmonization) + token consumption |
| 6 | Files Created | List with nature (expected `EmptyState.tsx` + test file + workspace page harmonization + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe `Panel`/`DataTable` integration) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (5 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 121/504 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 121/504 vs current (must be ≥121/504) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + `EmptyState` `role="status"` snapshots |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Feedback states complete; keyboard & focus in P04” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-010-P04 Keyboard Interaction & Focus Management Hardening |
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
- Frontend: 121 suites / 504 tests
- Backend: 414 tests

New tests physically added:
- [N tests across EmptyState + feedback harmonization suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [121 or 121+N] suites / [504 or 504+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-63 UI-010-P02 (121/504 + 414)
- Commit: [current HEAD]

Inherited Components: SkipLink.tsx/.css, accessibilityAudit.test.tsx, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), whole-surface harmonization (P06), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 121 suites / 504 frontend + 414 backend (D-63)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P10P02-01 (evidence on main continuity)

New Phase Scope: Feedback States — EmptyState + workspace loading/empty/error/toast harmonization (5 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P03, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-010-P03 APPROVED** (version increment per governance, e.g., 8.79.0) |
| `CHANGELOG.md` | Record P03 completion |
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
[ BUILD_ORDER_UI-010-P03 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Feedback-State Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P03 Determination ]
         ↓
[ BUILD_ORDER_UI-010-P04 — Keyboard Interaction & Focus Management Hardening ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | `EmptyState` renders `role="status"` `aria-live="polite"` + `aria-label` + `title` (`<h3>`) + `description` + `action` Button `onClick` + variants `default`/`compact` | Mandatory | `EmptyState.test.tsx` |
| AC-2 | Feedback-state harmonization: `loading` → `Skeleton` `aria-busy`, `empty` → `EmptyState` `role="status"`, `error` → `ErrorBanner` `role="alert"` across at least 2 representative workspaces (e.g., `/intelligence` + `/charts`) + `Toast` `polite` vs `assertive` correctly used | Mandatory | Workspace integration tests + `EmptyState.test.tsx` |
| AC-3 | All feedback primitives via `var(--ix-*)` — 0 ad-hoc hex in `components/ui/` + `workstation/` (outside `tokens.css`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-4 | Zero actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-5 | Zero LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-6 | 0 `dangerouslySetInnerHTML` + 0 `eval` in `components/ui/` + `workstation/` | Mandatory | E-6/E-7 exit 1 |
| AC-7 | Frontend regression 504 pass (or 504+ with accounting) | Mandatory | E-1 vitest.log |
| AC-8 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-9 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-10 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 10 criteria are **blocking** — one failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P03 implementation only** — no P04–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L, D-61 APPROVED WITH OBSERVATIONS) |
| P03 Design | §5 Phase Breakdown — P03 Feedback States Standardization |
| Preceding Baseline | D-63: 121 suites / 504 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 + Workspace Shell Regions A–F |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — §7 User Experience & Accessibility — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-63 (121/504) preserved as previous baseline |
| §3 Single Active Phase | **P03 = ACTIVE**, P04–P06 = NOT AUTHORIZED, UI-010-P01→P02 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P03 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-63 121/504 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + ad-hoc hex check |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no keyboard/high-contrast/whole-surface work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P04 not authorized until P03 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui010/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-63 preserved |
| §24 P03 Controls | Applied — feedback states + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P03 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-010-P03**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

