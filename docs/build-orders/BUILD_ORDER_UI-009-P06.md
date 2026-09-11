# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P06`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-59 — UI-009-P05 **APPROVED** (111 suites / 479 tests · 414 backend · exit 0) — Observation O-P09P05-01 (evidence logs documentary tier, continuity)
**Phase:** UI-009-P06 — Whole-Surface Harmonization & Completion Checkpoint
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §5/P06 — Whole-Surface Harmonization & Completion Checkpoint)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried to UI-009)
**Preceding Milestone:** UI-009-P05 (D-59 APPROVED) — 111 suites / 479 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 111/479 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P06 VERIFICATION ONLY** (Only §3.1 scope — no new functional development)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P06` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — UI-009 Design Plan APPROVED WITH OBSERVATIONS (O-009-01, O-009-02 — both closed D-55) |
| Preceding Milestone | UI-009-P05 (D-59) — 111/479 + 414 |
| Next Milestone | UI-009-P06 Delivery Report → ITRGA Determination → **UI-009 COMPLETE Declaration** (if approved) |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (verification/handover only — no new functional surface) |

---

## 2. PHASE OBJECTIVE

Execute the **final completion checkpoint** for `UI-009 — Institutional Design System Implementation`. Perform **whole-surface, whole-repository verification** of all P01–P05 design system surfaces (tokens → atoms → panels → tables → overlays) plus **whole-frontend token consumption audit**, **WCAG 2.1 AA accessibility audit**, and **zero-actuation/LLM grep proofs**, and produce the **final handover package** for declaration of **UI-009 COMPLETE**.

This phase is **verification and governance closure, not feature development.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Deliver:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Whole-Surface Token Consumption Audit** | Whole-frontend scan (`frontend/src`) proving 0 ad-hoc hex literals (`#[0-9A-Fa-f]{3,6}`) outside `tokens.css` — all colors via `var(--ix-*)` (extends P02–P05 component-scope proof to whole-frontend) |
| 2 | **Whole-Repository Grep Proofs** | Actuation (`frontend/src`), external LLM (`frontend/`), `dangerouslySetInnerHTML`/`eval` (`frontend/src`), secrets scan — whole-repo, exit-code proof |
| 3 | **Full Regression Suite** | Frontend 111/479 + Backend 414 — captured logs, no test added/removed without accounting |
| 4 | **TypeScript & Vite Build Proof** | `tsc -b` + `vite build` exit 0 — captured logs |
| 5 | **WCAG 2.1 AA Accessibility Audit** | Contrast >4.5:1 (body, table cells, overlay text, `0.75rem` metadata), focus `#8CC2FF`, keyboard `Tab`/`Enter`/`Space`/`Escape`, ARIA (`role="dialog"`/`aria-modal`, `role="status"`/`role="alert"`, `aria-sort`, `aria-current`), reduced-motion — axe or `accessibility.log` |
| 6 | **Cross-Workspace Surface Verification** | Spot-check at least **3 workspaces** (e.g., `/intelligence`, `/charts`, `/governance`) proving panel frames + tables + overlays render via tokens (DOM snapshots or Storybook snapshots) |
| 7 | **Branch & Governance Reconciliation (Final)** | Confirm `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L) + `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27) + `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` fidelity remain on-tree; no divergent `migration` state |
| 8 | **Project-State Final Synchronization** | `PROJECT_STATE.md` final **UI-009 COMPLETE** status (e.g., 8.76.0 `UI-009 — Institutional Design System Implementation COMPLETE`), `CHANGELOG.md`, `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md` — with diff logs (or explicit NO CHANGE) |
| 9 | **Evidence Package (Final)** | `docs/evidence/ui009/` final package — vitest, pytest, tsc/vite, grep logs, accessibility, diffs — committed to `main` |
| 10 | **Completion Handover Report** | Delivery Report with 20 sections per Amendment §13 + final **UI-009 COMPLETE** declaration readiness + next workstream recommendation (UI-010 or Production Readiness Certification) |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | New functional components or panels/tables/modals beyond P01–P05 | P06 is verification only |
| 2 | Redefinition of 5-tier token hierarchy or `theme.ts` contracts | **P01 already COMPLETE** — reuse |
| 3 | Rewrites of atomic primitives (`Button`/`Input`/`Select`/`Badge`/`Card`/`StatusChip`/`Tooltip`/`Accordion`) | **P02 already COMPLETE** — reuse |
| 4 | Rewrites of panel frames (`Panel`/`PanelHeader`/`PanelActionBar`/`Collapsible`) | **P03 already COMPLETE** — reuse |
| 5 | Rewrites of data tables/grids (`DataTable`/`SortableHeader`/`Pagination`/`formatters`) | **P04 already COMPLETE** — reuse |
| 6 | Rewrites of modals/overlays (`Dialog`/`Skeleton`/`Toast`/`ErrorBanner`/`CommandPalette.css`) | **P05 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P06 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Verification Boundaries

| Boundary | Requirement |
|----------|-------------|
| Functional surfaces | All P01 5-tier tokens → P02 8 atoms → P03 4 panel frames → P04 DataTable/SortableHeader/Pagination/formatters → P05 Dialog/Skeleton/Toast/ErrorBanner — **read-only verification only**, no new primitives |
| Token audit | Whole-frontend `frontend/src` — **not just `components/ui/`** — proves harmonization beyond library (legacy pages now via tokens) |
| Data | No mutation of persisted data — presentation-only verification |
| Branch | `main` must be single authoritative worktree after P05; `main` already contains `30169a4` baseline via prior reconciliation — confirm no divergent state |

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); verification respects layered architecture; no new bounded context; no circular deps; no backend coupling. Token audit extends P01 hierarchy verification to whole-frontend.

### 4.3 State

No new UI states beyond P01–P05 (tokens, atomic states, panel collapsed/expanded, table sorted/paginated, dialog open/closed, toast `polite`/`assertive`, skeleton `aria-busy`). Verification confirms existing states still render.

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in frontend | Grep `dangerouslySetInnerHTML` in `frontend/src/` — 0 matches |
| 4 | No `eval` / `new Function` in frontend | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` — whole-frontend | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/` (excluding `tokens.css` itself) — 0 matches (all colors via `var(--ix-*)`) |
| 7 | No new actuation/LLM via overlay `action` Button (Dialog `footer`/`ErrorBanner` `action`) — `Button` must be presentation `onClick` only, not order routing | Code review — `Button` `onClick` in `Dialog`/`ErrorBanner` must not call `placeOrder`/`executeTrade` |

### Required Security Proofs (Whole-Frontend for P06 Completion)

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — whole `frontend/src/` | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex — **whole `frontend/src/`*** | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src --exclude="tokens.css"` → exit 1 (0 matches) — *stricter than P02–P05 component-scope* |
| S-5 | Secrets scan — whole `frontend/` | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

*`*` For S-4 whole-frontend, **exclude `frontend/src/workstation/design/tokens.css` itself** (it is the *definition* of hex primitives — the source of truth). All other files must be 0 ad-hoc hex. Alternatively, prove via `grep -R -E` in `frontend/src --exclude-dir=workstation/design` if DA prefers, but document the exclusion.*

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Brand Fidelity (Whole-Surface) | All workspaces/primitives via tokens (`--ix-bg-surface-raised`, `--ix-border-subtle`, `--ix-shadow-overlay`, `--ix-color-accent/success/warning/critical`, `--ix-space-*`) — verified via whole-frontend ad-hoc hex 0 | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast (Whole-Surface) | Text/background >4.5:1 across all surfaces (Dialog, Table cells, Toast, ErrorBanner, Panel frames, `0.75rem` metadata) — `7.2:1`/`6.8:1` inherited from P01, re-verified | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding (Whole-Surface) | Toast/ErrorBanner `info`/`success`/`warning`/`error` + Badge/StatusChip still text+`◆◆◆`+`%` + `aria-live`; DataTable `↑`/`↓`/`↕` + `aria-sort` | 02 §Design, 08 |
| U-4 | Focus Visibility (Whole-Surface) | Focus rings `var(--ix-color-focus)` `#8CC2FF` on Dialog close, Toast dismiss, ErrorBanner action/dismiss, Panel collapsible triggers, DataTable SortableHeader, Pagination buttons | WCAG 2.4.7 |
| U-5 | Motion Restraint (Whole-Surface) | All transitions via `var(--ix-motion-fast)` `120ms`; `Dialog` backdrop/content, `Toast` enter/exit, `Collapsible` height, `Skeleton` shimmer — all respect `@media (prefers-reduced-motion: reduce)` → `0ms` | 08 motion |
| U-6 | Keyboard Navigation (Whole-Surface) | `Tab`/`Shift+Tab` cycles within `Dialog` (focus trap); `Escape` closes `Dialog`/focused `Toast`; `Tab` navigates panel frames + table headers + pagination + overlay actions; `Enter`/`Space` toggles Collapsible/SortableHeader/Accordion/Select + activates `ErrorBanner` action | 08 keyboard |
| U-7 | ARIA (Whole-Surface) | `Dialog` `role="dialog"` `aria-modal` `aria-labelledby`/`aria-describedby`; `Toast` `role="status"` vs `role="alert"` + `aria-live`; `ErrorBanner` `role="alert"` `aria-live="assertive"`; `DataTable` `aria-label` + `th` `aria-sort` + `Pagination` `aria-current` + `Panel` `aria-labelledby` + `Collapsible` `aria-expanded` | WCAG / 08 |
| U-8 | Dark-First + Cross-Workspace Harmonization | Spot-check `/intelligence`, `/charts`, `/governance` (or equivalent) proving panel frames + tables + overlays render via tokens on `--ix-bg-root` `#0B0E14` + `--ix-bg-surface` `#111822` + `.theme-light` override — no workspace-specific hex | 08 dark-first + 13 Part V harmonization |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `ui009_p06_wholeSurface.test.tsx` (or `verification.test.tsx`) | Whole-surface regression: at least one assertion per P01–P05 deliverable class (tokens existence, Button variant, Panel collapsed, DataTable sorted, Dialog `aria-modal`, Toast `aria-live`, Skeleton `aria-busy`) — proves cross-workspace token harmonization still holds; may be minimal 3–5 tests |
| T-2 | `ui009_p06_security_invariants.test.ts` | S-1 whole-repo actuation + S-2 LLM + S-3 sandbox + S-4 whole-frontend ad-hoc hex (`frontend/src` excluding `tokens.css`) + S-5 secrets — via `grep_*.log` transcripts (or `expect` grep exit 1 in test harness) |
| T-3 | Accessibility spot-check (if not already in `accessibility.log`) | WCAG 2.1 AA: contrast >4.5:1 sample + focus + ARIA + keyboard + reduced-motion — via `accessibility.log` |

**Note:** P06 is a **verification checkpoint**, not a feature phase. DA may add **0–5** verification-only tests (T-1…T-3) if needed; must account for them per Amendment §8. Zero new functional tests is acceptable if existing 111/479 already cover whole-surface via integration snapshots.

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **479 tests — 100% pass** (or 479+ with accounting — see §8) — P06 verification must show **no regression** from D-59 (P05) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*P06 is additive verification — **0 removed / 0 modified** expected for existing tests (111 suites 479 tests from P05). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`DataTable` with `rows=[]` → `empty` `role="status"` (not `loading`); `Dialog` `open={false}` → not in DOM; `Toast` without `autoDismissMs` → not auto-dismissed; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **479+ pass** — full log (must show 111 suites/479 baseline + any new P06 verification suites) | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` whole `frontend/src` | Level II | 0 | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` whole `frontend/src` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | **Grep ad-hoc hex — WHOLE `frontend/src` (excluding `tokens.css`)** | Level II | 0 (proves **whole-surface** token consumption — strictly stronger than P02–P05 component-scope) | `docs/evidence/ui009/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Accessibility audit — whole-surface | Level II | WCAG 2.1 AA — contrast >4.5:1 + focus + ARIA + keyboard + reduced-motion across at least 3 workspaces | `docs/evidence/ui009/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` / `RISK_REGISTER.md` / `TECHNICAL_DEBT_REGISTER.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` / `changelog_diff.log` |
| E-12 | Branch / governance reconciliation | Level II | `git log --oneline --all --graph` + `git diff main..HEAD` showing `main` contains UI-009 P01→P05 artifacts + `docs/plans/` + `docs/governance/` | `docs/evidence/ui009/branch_reconciliation.log` (optional — already on-tree per P05) |
| E-13 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P06.md` with 20 sections | `DELIVERY_REPORT_UI-009-P06.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — DOM snapshots for whole-surface spot-checks if applicable, e.g., Storybook snapshots for Dialog/Toast/DataTable) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **P06 upgrades S-4 from component-scope (P02–P05) to whole-frontend scope (excluding `tokens.css` definition file).**

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

**Expected:** `VITEST_EXIT:0` with **479+ pass** (P06 will be 111→~112 suites if +1 verification suite), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) **whole `frontend/src`** | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) whole `frontend/src` | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| **Ad-hoc hex (S-4) WHOLE `frontend/src` excluding `tokens.css`** | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src --exclude="tokens.css" 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` <br> *Alt:* `grep -R -n -E "#[0-9A-Fa-f]{3,6}" frontend/src --exclude-dir=workstation/design 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src --exclude="tokens.css" 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | **Git Bash:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**Exit code contract (both platforms, identical):** **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion fixtures, documented).** For S-4 whole-frontend in P06, **exclude `tokens.css` itself** — it is the definition of hex primitives (source of truth); all other files must be 0 ad-hoc hex. Document the exclusion in `grep_ad_hoc_hex.log` header.

#### 3. Documentation Diffs & Accessibility

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui009/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui009/changelog_diff.log` |
| *(Optional axe)* `npx axe --help 2>&1 | Tee-Object -FilePath docs/evidence/ui009/accessibility.log` | `npx axe --help 2>&1 \| tee docs/evidence/ui009/accessibility.log` |

**All logs must be committed to `docs/evidence/ui009/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both deterministic. **Git Bash on Windows gives identical `grep` exit codes as DA's Linux** — strongly recommended.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-009-P06.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P06 — Whole-Surface Harmonization & Completion Checkpoint |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P06` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §5 P06 (and §10 P01 token foundation) |
| 4 | Previous Baseline | P05 D-59: 111 suites / 479 tests · 414 backend · overlay/feedback 6 suites/25 tests |
| 5 | Implementation Summary | What whole-surface verification was performed (whole-frontend token audit, whole-repo greps, WCAG audit, cross-workspace spot-checks) — no new functional development beyond 0–1 verification harness |
| 6 | Files Created | List with nature (expected 0–1 verification harness + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe `Panel`/`DataTable` integration if harmonized) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (10 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 111/479 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 111/479 vs current (must be ≥111/479) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo proofs (whole-frontend ad-hoc hex 0 excluding `tokens.css`) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + whole-surface WCAG audit + cross-workspace snapshots |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “None — UI-009 verification complete; whole-surface harmonized” or remaining observation |
| 18 | Evidence Index | Complete list E-1…E-13 |
| 19 | Next Phase Recommendation | **UI-009 COMPLETE** declaration (or next workstream UI-010 / 11 Certification) |
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
- Frontend: 111 suites / 479 tests
- Backend: 414 tests

New tests physically added:
- [N tests in ui009_p06 verification harness — or 0]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [111 or 111+N] suites / [479 or 479+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-59 UI-009-P05 (111/479 + 414)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), DataTable/SortableHeader/Pagination/formatters (P04), Dialog/Skeleton/Toast/ErrorBanner (P05), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 111 suites / 479 frontend + 414 backend (D-59)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P09P05-01 (evidence on main continuity)

New Phase Scope: Whole-Surface Harmonization — whole-frontend token audit + whole-repo greps + WCAG audit + cross-workspace spot-checks (10 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P06, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P06 APPROVED** and **UI-009 — Institutional Design System Implementation COMPLETE** (e.g., 8.76.0 `UI-009 COMPLETE`) |
| `CHANGELOG.md` | Record P06 completion |
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
[ BUILD_ORDER_UI-009-P06 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Whole-Surface Verification & Evidence Capture ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P06 Determination → UI-009 COMPLETE (if APPROVED) ]
         ↓
[ UI-009 COMPLETE Declaration → Next Workstream UI-010 or Production Readiness Certification (11) — Separate Governance ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Whole-surface token audit — 0 ad-hoc hex in `frontend/src` **excluding `tokens.css`** (all colors via `var(--ix-*)`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-2 | Whole-repo actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-3 | Whole-repo LLM grep (whole `frontend/`) — 0 functional | Mandatory | E-5 exit 1 |
| AC-4 | Sandbox safety — **whole `frontend/src`** 0 `dangerouslySetInnerHTML` + 0 `eval`/`new Function` | Mandatory | E-6/E-7 exit 1 |
| AC-5 | Secrets scan — 0 real secrets | Mandatory | E-9 exit 1 |
| AC-6 | Cross-workspace spot-check — at least 3 workspaces (`/intelligence`, `/charts`, `/governance` or equivalent) prove panel frames + tables + overlays render via tokens | Mandatory | Level I DOM snapshots or integration test evidence |
| AC-7 | WCAG 2.1 AA audit — contrast >4.5:1 + focus + ARIA + keyboard + reduced-motion across whole-surface | Mandatory | E-10 `accessibility.log` (axe or spot-check) |
| AC-8 | Frontend regression 479 pass (or 479+ with accounting) | Mandatory | E-1 `vitest.log` |
| AC-9 | Backend regression 414 pass | Mandatory | E-2 `pytest.log` |
| AC-10 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-11 | Project-state docs synchronized — `PROJECT_STATE.md` final `UI-009 COMPLETE` + `CHANGELOG.md` + diff logs | Mandatory | E-11 |
| AC-12 | No new functional development beyond 0–1 verification harness — 0 deviations beyond verification | Mandatory | §10 `NO DEVIATIONS` |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking** — one failure = CORRECT/RESUBMIT. Upgrading S-4 from component-scope (P02–P05) to whole-frontend scope is the key P06 hardening.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P06 verification only** — no new functional development beyond 0–1 verification harness per §3.1.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P06 Design | §5 Phase Breakdown — P06 Whole-Surface Harmonization & Completion Checkpoint |
| Preceding Baseline | D-59: 111 suites / 479 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-59 (111/479) preserved as previous baseline |
| §3 Single Active Phase | **P06 = ACTIVE**, UI-010+ = NOT YET AUTHORIZED, P01–P05 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P06 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-59 111/479 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + whole-frontend ad-hoc hex |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no new functional scope |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — UI-009 COMPLETE only after P06 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-59 preserved |
| §24 P06 Controls | Applied — whole-surface harmonization + WCAG audit + token audit |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P06 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P06**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

