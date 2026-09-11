# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P04`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-71 — UI-011-P03 **APPROVED WITH OBSERVATIONS** (142 suites / 579 tests · 414 backend · exit 0) — Observations O-P11P03-01 (beneficial expanded harmonization — 16 vs 5 named, retained), O-P11P03-02 (evidence logs documentary tier, continuity)
**Phase:** UI-011-P04 — Optical Typography & Monospace Financial Data Polish
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §5/P04 — Optical Typography & Monospace Financial Data Polish)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-011-P03 (D-71 APPROVED WITH OBSERVATIONS) — 142 suites / 579 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 142/579 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P04 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P04` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01 — matrix summary, closed) |
| Preceding Milestone | UI-011-P03 (D-71) — 142/579 + 414 |
| Next Milestone | UI-011-P04 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (typography polish — optical hierarchy, tabular-nums, no business logic) |

---

## 2. PHASE OBJECTIVE

Refine **optical typography and monospace financial data presentation** for AXIOM by **standardizing typography scale** (`0.75rem` metadata → `0.9rem` body → `0.85rem` panel headings → workspace titles → display), **optical label/value contrast**, and **strict `tabular-nums` monospace alignment for all financial figures** (spreads, prices, confidence percentages, ECE metrics) — per `12` Part VI §17 (Clean Typography, Balanced Information Density) and `08_UI_UX_SPEC.md` (Typography hierarchy, monospace numerical alignments).

This phase is **typography and monospace polish, not cross-workspace cohesion (P05) or whole-surface handover (P06).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Typography Scale Harmonization — `tokens.css` + `theme.ts` typography tokens** | Harmonize `font-size` / `font-weight` / `line-height` / `letter-spacing` for Display Titles (`1.5rem`), Workspace Titles (`1.2rem`), Section Headings (`1.0rem`), Panel Headings (`0.85rem`), Body (`0.9rem`), Metadata/Monospace (`0.75rem`) via `var(--ix-font-size-*)` / `var(--ix-font-weight-*)` / `var(--ix-typography-*)` — ensure hierarchy `h1`→`h2`→`h3`→`h4` optical contrast via size/weight, not just `font-size` outside tokens |
| 2 | **Monospace Tabular-Nums Enforcement — `DataTable.css` + `formatters.ts` + financial columns** | Enforce `font-family: var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` for **every** financial figure column (`--ix-numeric-*` or `align="numeric"` already in P04 DataTable) across all 7 workspace data tables (`Price`, `Spread`, `Pips`, `Percent`, `ECE`, `Brier`, `Correlation r`, `Confidence %`) — no left-aligned numbers, no proportional-nums on financial data |
| 3 | **Optical Contrast Refinement — `theme.ts` typography contracts** | Define optical size/weight/contrast tokens: metadata `0.75rem` (`#94A3B8` 6.8:1) vs body `0.9rem` (`#EEF4FC` 15.8:1) vs panel heading `0.85rem` (`#EEF4FC` 15.8:1) — ensure label/value optical separation via `color: var(--ix-text-muted)` vs `var(--ix-text-primary)` + `font-variant-numeric` |
| 4 | **Test Harness — `typographyPolish.test.tsx` + invariants** | New suite `typographyPolish.test.tsx` (typography scale via `var(--ix-font-size-*)`/`var(--ix-typography-*)`, `tabular-nums` alignment via `getComputedStyle` `fontVariantNumeric`, monospace `var(--ix-font-mono)`, `text-align: right` for financial columns) plus security/token invariants |
| 5 | **Token Consumption Enforcement** | All typography via `var(--ix-*)` (`var(--ix-font-size-*)`, `var(--ix-typography-*)`, `var(--ix-font-mono)`, `var(--ix-text-*)`) — 0 ad-hoc `font-size: 14px` / `font-family: Arial` outside `tokens.css` |
| 6 | **Evidence Package** | Logs committed to `docs/evidence/ui011/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Cross-workspace cohesion & visual regression audit (multi-workspace spot-checks) | **UI-011-P05** scope |
| 2 | Whole-surface Version 1.0 handover & completion checkpoint | P06 scope |
| 3 | Font family swaps outside `theme.ts` (changing `Inter` → `Roboto` or similar) — font families defined in `theme.ts` `font-sans`/`font-mono` only, no arbitrary swap | Not in P04 design — typography refinement must use existing `Inter`/`JetBrains Mono` via tokens |
| 4 | Mobile viewports (<768px) | **DEFERRED** per Design Plan §10 — post-1.0 |
| 5 | Information hierarchy tokens redefinition (`--ix-hierarchy-*`/`--ix-elevation-*`) | **P01 already COMPLETE** — reuse |
| 6 | Panel balance redefinition beyond typography (header/body/footer `var(--ix-space-*)` padding already harmonized) | **P02 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P04 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Typography & Monospace Architecture (Per Design Plan §5 P04 + 12 Part VI §17 Clean Typography + Balanced Information Density)

- **Location (Recommended):** `frontend/src/workstation/design/tokens.css` — extend typography tokens (`--ix-font-size-display: 1.5rem`, `--ix-font-size-workspace-title: 1.2rem`, `--ix-font-size-section-heading: 1.0rem`, `--ix-font-size-panel-heading: 0.85rem`, `--ix-font-size-body: 0.9rem`, `--ix-font-size-metadata: 0.75rem`, `--ix-font-mono: 'JetBrains Mono', monospace`); `frontend/src/workstation/design/theme.ts` — typed contracts `TYPOGRAPHY_TOKENS`; DA may alternatively harmonize via `frontend/src/components/ui/` typography utilities if reusing existing, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **Typography Scale:** `Display` `1.5rem` (`--ix-font-size-display`), `Workspace Title` `1.2rem`, `Section Heading` `1.0rem`, `Panel Heading` `0.85rem`, `Body` `0.9rem`, `Metadata` `0.75rem` — each via `var(--ix-font-size-*)` + `var(--ix-font-weight-*)` + `var(--ix-text-*)` for color. Must **not** use hardcoded `font-size: 14px` outside `tokens.css`.
- **Monospace Tabular-Nums:** Every financial figure column (`Price`, `Spread`, `Pips`, `Percent`, `Brier`, `ECE`, `Correlation r`, `Confidence %`) **must render** `font-family: var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` (via `DataTable` `align="numeric"` or `formatters.ts` span class `ix-numeric`). No proportional-nums on financial data — `tabular-nums` ensures digit columns align vertically for rapid scanning.
- **Optical Contrast:** Metadata `0.75rem` (`#94A3B8` 6.8:1 on `#111822`) vs body `0.9rem` (`#EEF4FC` 15.8:1) — ensures label/value optical separation via `color: var(--ix-text-muted)` vs `var(--ix-text-primary)` + `font-variant-numeric`, not just `font-size` outside tokens.
- **Token Consumption:** Every visual value (`font-size` `var(--ix-font-size-*)`, `font-family` `var(--ix-font-mono)`, `color` `var(--ix-text-*)`, `font-variant-numeric`) **must reference P01 tokens** (`var(--ix-*)`). No inline `font-family: Arial` outside `tokens.css`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/design/tokens.css` + `components/ui/`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; typography is presentation, not business logic.

### 4.3 Interaction Contracts

| Component / Token | Contract |
|-----------|----------|
| `--ix-font-size-display` | `1.5rem` — Display Titles via `var(--ix-font-size-display)` |
| `--ix-font-size-workspace-title` | `1.2rem` — Workspace Titles |
| `--ix-font-size-section-heading` | `1.0rem` — Section Headings |
| `--ix-font-size-panel-heading` | `0.85rem` — Panel Headings `h3`/`h4` |
| `--ix-font-size-body` | `0.9rem` — Body Content |
| `--ix-font-size-metadata` | `0.75rem` — Metadata/Monospace `0.75rem` (`#94A3B8` 6.8:1) — must be `>4.5:1` via `var(--ix-text-muted)` |
| `--ix-font-mono` | `'JetBrains Mono', monospace` — Monospace financial figures via `var(--ix-font-mono)` + `tabular-nums` |
| `DataTable` financial columns | `align="numeric"` → `font-family: var(--ix-font-mono); font-variant-numeric: tabular-nums; text-align: right;` |
| `formatters.ts` | `formatPips`/`formatPercent`/`formatPearsonR` spans with `className="ix-numeric"` → `var(--ix-font-mono)` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in typography module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/design/` — 0 matches |
| 4 | No `eval` / `new Function` in module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/design/` + `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |
| 7 | No credential exposure via typography (no `value` of `<input>` in DOM attributes) | Code review — typography tokens must not log input values |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — typography module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — typography module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/design/ frontend/src/components/ui/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Typography Scale | `Display` 1.5rem / `Workspace Title` 1.2rem / `Section Heading` 1.0rem / `Panel Heading` 0.85rem / `Body` 0.9rem / `Metadata` 0.75rem via `var(--ix-font-size-*)` — `h1`→`h2`→`h3`→`h4` optical hierarchy | `12` Part VI §17 (Clean Typography) |
| U-2 | Monospace Tabular-Nums | Every financial figure column `font-family: var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` — prices, spreads, pips, percents, ECE/Brier, correlation r, confidence % | `08_UI_UX_SPEC.md` (monospace numerical alignment), 03 tabular-nums |
| U-3 | Optical Label/Value Contrast | Metadata `0.75rem` (`#94A3B8` 6.8:1) vs body `0.9rem` (`#EEF4FC` 15.8:1) — label/value optical separation via `color: var(--ix-text-muted)` vs `var(--ix-text-primary)` + `font-variant-numeric` | WCAG 1.4.3, 12 Part VI §17 |
| U-4 | Visual Consistency | No hardcoded `font-size: 14px` / `font-family: Arial` outside `tokens.css` — all via `var(--ix-*)` | 16 Brand Governance |
| U-5 | Dark-First | Typography hierarchy renders correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `typographyPolish.test.tsx` | Typography scale `var(--ix-font-size-*)` existence + `theme.ts` `TYPOGRAPHY_TOKENS` contract + `Panel` header `0.85rem` + `Card` body `0.9rem` + `DataTable` numeric `tabular-nums` via `getComputedStyle` |
| T-2 | `typographyMonospace.test.tsx` (or within `typographyPolish.test.tsx`) | Monospace `var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` for every financial column (`Price`, `Spread`, `Pips`, `Percent`, `ECE`, `Brier`, `Correlation r`) |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **579 tests — 100% pass** (or 579+ with accounting — see §8) — P04 adds typography tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Typography polish is additive — **0 removed / 0 modified** expected for existing tests (142 suites 579 tests from UI-011-P03). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`typographyPolish` with missing `--ix-font-size-metadata: 0.75rem` → test fails; `DataTable` financial column without `tabular-nums` → test fails via `getComputedStyle` `fontVariantNumeric`; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — continue `ui011` evidence directory for UI-011)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **579+ pass** — full log (must show 142 suites/579 baseline + new P04 suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/design/` + `components/ui/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Typography polish evidence | Level II | `typographyPolish.test.tsx` typography scale + `tabular-nums` + `var(--ix-font-mono)` | `docs/evidence/ui011/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P04.md` with 20 sections | `DELIVERY_REPORT_UI-011-P04.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `typographyPolish.test.tsx` DOM snapshot of typography hierarchy) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **Continue evidence directory `docs/evidence/ui011/` is required for UI-011 (separate from `ui010` 136/556 → 113/485 baseline).**

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs. **For reliable cross-platform `grep` on Windows, use *Git Bash* (bundled with Git for Windows) — it runs identical Bash commands as DA's Linux.**

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Create evidence dir | `New-Item -ItemType Directory -Force -Path docs/evidence/ui011` | `mkdir -p docs/evidence/ui011` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui011/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui011/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui011/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui011/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui011/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **579+ pass** (P04 will be 142→~144 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `workstation/design/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/design/ 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/workstation/design/ 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/workstation/design/ 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/workstation/design/ 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `workstation/design/` + `components/ui/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/design/ frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/workstation/design/ frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | **Git Bash:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**Exit code contract (both platforms, identical):** **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion fixtures, documented).**

#### 3. Documentation Diffs

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui011/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui011/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui011/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui011/changelog_diff.log` |

**All logs must be committed to `docs/evidence/ui011/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both deterministic. **Git Bash on Windows gives identical `grep` exit codes as DA's Linux** — strongly recommended.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-011-P04.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P04 — Optical Typography & Monospace Financial Data Polish |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P04` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §5 P04 + §10 P01 hierarchy |
| 4 | Previous Baseline | UI-011-P03 D-71: 142 suites / 579 tests · 414 backend · micro-interaction + motion restraint |
| 5 | Implementation Summary | What typography/monospace polish was built (typography scale harmonization + tabular-nums alignment + optical contrast) + token consumption |
| 6 | Files Created | List with nature (expected `typographyPolish.test.tsx` + maybe `Card.css` typography harmonization + evidence logs) |
| 7 | Files Modified | List with nature (likely `tokens.css` typography tokens + `theme.ts` + `Panel.css`/`Card.css` typography + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (6 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 142/579 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 142/579 vs current (must be ≥142/579) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Typography visual proof (monospace snapshots) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Typography complete; cross-workspace cohesion in P05” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-011-P05 Cross-Workspace Cohesion & Visual Regression Audit |
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
- Frontend: 142 suites / 579 tests
- Backend: 414 tests

New tests physically added:
- [N tests across typographyPolish tests]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [142 or 142+N] suites / [579 or 579+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-71 UI-011-P03 (142/579 + 414)
- Commit: [current HEAD]

Inherited Components: hierarchy tokens (--ix-hierarchy-*, --ix-elevation-level-*), 5-tier tokens, Panel/PanelHeader/PanelActionBar/Collapsible, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 142 suites / 579 frontend + 414 backend (D-71)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P11P03-01 (beneficial expanded harmonization — 16 vs 5 named, retained), O-P11P03-02 (evidence on main continuity)

New Phase Scope: Typography — scale harmonization + tabular-nums + optical contrast (6 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P04, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P04 APPROVED** (version increment per governance, e.g., 8.86.0) |
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
[ BUILD_ORDER_UI-011-P04 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Typography Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P04 Determination ]
         ↓
[ BUILD_ORDER_UI-011-P05 — Cross-Workspace Cohesion & Visual Regression Audit ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Typography scale `var(--ix-font-size-*)` harmonized — `Display` 1.5rem / `Workspace Title` 1.2rem / `Section Heading` 1.0rem / `Panel Heading` 0.85rem / `Body` 0.9rem / `Metadata` 0.75rem via `var(--ix-font-size-*)` | Mandatory | `typographyPolish.test.tsx` DOM snapshot |
| AC-2 | Monospace `var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` for every financial figure column (Price/Spread/Pips/Percent/ECE/Brier/Correlation r) | Mandatory | `typographyPolish.test.tsx` |
| AC-3 | Optical label/value contrast — metadata `0.75rem` (`#94A3B8` 6.8:1) vs body `0.9rem` (`#EEF4FC` 15.8:1) — `color: var(--ix-text-muted)` vs `var(--ix-text-primary)` | Mandatory | `typographyPolish.test.tsx` |
| AC-4 | Zero ad-hoc hex literals across `frontend/src/workstation/design/` + `frontend/src/components/ui/` (outside `tokens.css`) — all colors via `var(--ix-*)` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-5 | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-6 | Full platform regression suite passes with 100% success (≥579 frontend, 414 backend) | Mandatory | E-1/E-2 vitest/pytest logs |
| AC-7 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | Mandatory | E-3 tsc/vite logs |
| AC-8 | Delivery Report 20 sections + Governance Declaration per §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**O-011-01 (matrix summary) will be re-verified as harmonized via P04 typography polish.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P04 implementation only** — no P05–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P04 Design | §5 Phase Specifications — P04 Optical Typography & Monospace Financial Data Polish |
| Preceding Baseline | D-71: 142 suites / 579 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-71 (142/579) preserved as previous baseline |
| §3 Single Active Phase | **P04 = ACTIVE**, P05–P06 = NOT AUTHORIZED, UI-011-P01→P03 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P04 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-71 142/579 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no cross-workspace cohesion beyond typography |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P05 not authorized until P04 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-71 preserved |
| §24 P04 Controls | Applied — typography + monospace + optical contrast |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P04 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P04**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

