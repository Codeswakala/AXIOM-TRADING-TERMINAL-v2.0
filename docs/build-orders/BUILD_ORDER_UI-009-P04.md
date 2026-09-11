# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P04`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-57 — UI-009-P03 **APPROVED WITH OBSERVATIONS** (99 suites / 429 tests · 414 backend · exit 0) — Observations O-P09P03-01 (Badge `children` — safe, minor undeclared), O-P09P03-02 (evidence logs documentary tier)
**Phase:** UI-009-P04 — Data Tables & Visualization Grids
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §5/P04 — Data Tables & Visualization Grids)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried to UI-009)
**Preceding Milestone:** UI-009-P03 (D-57 APPROVED WITH OBSERVATIONS) — 99 suites / 429 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 99/429 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P04 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P04` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — UI-009 Design Plan APPROVED WITH OBSERVATIONS (O-009-01, O-009-02 — closed D-55) |
| Preceding Milestone | UI-009-P03 (D-57) — 99/429 + 414 |
| Next Milestone | UI-009-P04 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (table/grid presentation primitives — read-only data display, no persistence) |

---

## 2. PHASE OBJECTIVE

Standardize **institutional data tables and visualization grids** for AXIOM by codifying **DataTable**, **Monospace Numerical Alignment**, **Uncertainty Interval Formatters**, **Sortable Column Headers**, and **Pagination Controls** using the **P01 5-tier tokens** and **P02–P03 primitives** (`Panel`, `Badge`, `StatusChip`, `Button`, `Input`) — read-only data presentation, no backend mutation.

This phase is **table/grid presentation standardization, not workspace rewrite or modal work.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **DataTable — `DataTable.tsx` + `DataTable.css`** | Reusable institutional table: `columns[]` (`key`, `header`, `sortable?`, `align?: "left"|"center"|"right"|"numeric"`, `width?`, `render?`), `rows[]` (generic typed), `sortKey`/`sortDirection` (`asc`/`desc`), `onSort` callback, `loading` (skeleton rows), `empty` state (honest “No data” with icon+text), `pagination` integration slot |
| 2 | **Monospace Numerical Alignment** | Numeric columns render with `font-variant-numeric: tabular-nums` + `font-family: var(--ix-font-mono)`; values right-aligned via `align="numeric"`; applied to price/quantity/pips/percent/interval bounds |
| 3 | **Uncertainty Interval Formatters — `formatters.ts` (or `utils/formatUncertainty.ts`)** | Pure helpers: `formatUncertaintyInterval({ lower, upper, confidence })` → `"95% CI [-0.15, +0.22]"`, `formatSampleCount(n)` → `"n=120"`, `formatPearsonR(r)` → `"r=0.73"`, `formatPips(value)` / `formatPercent(value)` — all via tokens, no inline styling |
| 4 | **Sortable Column Headers — `SortableHeader.tsx` + `SortableHeader.css`** | Header button with `aria-sort="ascending|descending|none"`, `aria-label` sort direction, `sorted` + `sortDirection` props, keyboard `Enter`/`Space` toggles sort, icon indicator (`↑`/`↓`/`↕`) via `var(--ix-color-accent)` — consumes P02 `Button` or native `<button>` with `var(--ix-*)` |
| 5 | **Pagination Controls — `Pagination.tsx` + `Pagination.css`** | Controls `page` / `pageSize` / `totalRows` / `onPageChange` + `onPageSizeChange`; buttons `First`/`Prev`/`Next`/`Last` + page info `“Page 2 of 14”` + `aria-label` page navigation, `aria-current="page"` on active page, disabled states at bounds |
| 6 | **Token Consumption Enforcement** | All table/grid primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `components/ui/` |
| 7 | **Comprehensive State Tests** | Per-component suites covering rendering + sorting + pagination + numeric alignment + formatters + keyboard + ARIA + token consumption |
| 8 | **Evidence Package** | Logs committed to `docs/evidence/ui009/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Modals, Command Palette styling, dialogs, skeleton loaders, toasts, error banners | **UI-009-P05** scope |
| 2 | Whole-surface harmonization & completion checkpoint | P06 scope |
| 3 | Atomic primitives (`Button`/`Input`/`Select`/`Badge`/`Card`/`StatusChip`/`Tooltip`/`Accordion`) | **P02 already COMPLETE** — reuse |
| 4 | Panel frames (`Panel`/`PanelHeader`/`PanelActionBar`/`Collapsible`) | **P03 already COMPLETE** — reuse |
| 5 | 5-tier token hierarchy or `theme.ts` contracts | **P01 already COMPLETE** — reuse, do not redefine |
| 6 | New backend endpoints, migrations, schema changes | No persistence change |
| 7 | WebSocket / real-time push | Not in P04 design |
| 8 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 9 | External LLM integration (OpenAI/Anthropic/LangChain etc.) | Constitutionally prohibited — 12 Part I §5 |
| 10 | Order / trade / execution / broker controls | Absolutely prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Table / Grid Architecture (Per Design Plan §5 P04)

- **Location:** `frontend/src/components/ui/` (same library path as P02 atomic + P03 panels — `frontend/src/components/ui/` declared in P02/P03) — all table primitives **must live in the same library path** for single import surface.
- **Data Flow:** `DataTable` is **presentation-only** — receives `columns[]` + `rows[]` as props (generic `<T>`); **no data fetching inside**; sorting is **controlled** (`sortKey`/`sortDirection` + `onSort` callback) — DA shall not implement uncontrolled fetch.
- **Token Consumption:** Every visual value (background, border, header `background: var(--ix-bg-surface-raised)`, cell padding `var(--ix-space-*)`, monospace `var(--ix-font-mono)`, accent `var(--ix-color-accent)` for sort indicator, focus `var(--ix-color-focus)`) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`), no hardcoded `px` spacing outside `var(--ix-space-*)`.
- **No Runtime Style Injection:** No `dangerouslySetInnerHTML` for style/theme injection; no `eval`/`new Function`; no raw `<script>`; tokens are static CSS custom properties.
- **a11y Grid:** `<table>` with `<thead>`/`<tbody>`, `<th>` `scope="col"` + `aria-sort`, `<td>` semantic; `Empty` state uses `role="status"` + honest text; `Loading` uses skeleton rows with `aria-busy="true"`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); bounded context `frontend/src/components/ui/` isolated; no new bounded context; no circular deps; no backend coupling; `formatters.ts` is pure helper (no side effects).

### 4.3 Interaction Contracts

| Component / Helper | Contract |
|-----------|----------|
| `DataTable<T>` | `columns: { key: keyof T, header: string, sortable?: boolean, align?: "left"|"center"|"right"|"numeric", width?: string, render?: (value: any, row: T) => ReactNode }[]` + `rows: T[]` + `sortKey?: keyof T` + `sortDirection?: "asc"|"desc"` + `onSort?: (key: keyof T, dir: "asc"|"desc") => void` + `loading?: boolean` + `emptyText?: string` + `pagination?: { page, pageSize, totalRows, onPageChange, onPageSizeChange }` + `aria-label` |
| `SortableHeader` | `columnKey: string` + `header: string` + `sorted: boolean` + `sortDirection?: "asc"|"desc"` + `onSort: (key, dir) => void` + `aria-sort` + `aria-label` — click or `Enter`/`Space` toggles, `↑`/`↓` indicator |
| `Pagination` | `page: number` + `pageSize: number` + `totalRows: number` + `onPageChange: (page) => void` + `onPageSizeChange?: (size) => void` + `aria-label` page nav, `aria-current="page"` |
| `formatUncertaintyInterval` | `({ lower: number, upper: number, confidence?: number }) => string` e.g., `"95% CI [-0.15, +0.22]"` — pure, no DOM |
| `formatSampleCount` | `(n: number) => string` e.g., `"n=120"` |
| `formatPearsonR` | `(r: number) => string` e.g., `"r=0.73"` — respects tabular-nums when rendered |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in table/grid primitives | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` — 0 matches |
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
| U-1 | Brand Fidelity | All table/grid primitives via tokens (`--ix-bg-surface`, `--ix-bg-surface-raised`, `--ix-border-subtle`, `--ix-color-accent`, `--ix-font-mono`, `--ix-space-*`) — no inline hex | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast | Text/background >4.5:1 (header, cell text, pagination, empty/loading) — inherited from P01 `7.2:1`/`6.8:1` for metadata | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding | Sort indicator `↑`/`↓` includes `aria-sort` + text label + `aria-label`; no status color without text/symbol | 02 §Design, 08 |
| U-4 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` on `SortableHeader` button + `Pagination` buttons + `DataTable` focusable rows (if interactive) | WCAG 2.4.7 |
| U-5 | Motion Restraint | No animated sorting (instant); pagination transitions via `var(--ix-motion-fast)` `120ms` where applicable; respects `@media (prefers-reduced-motion: reduce)` → `0ms` | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` traverses `SortableHeader` buttons + `Pagination` controls; `Enter`/`Space` toggles sort; `Arrow` not required for table (headers are buttons) | 08 keyboard |
| U-7 | ARIA | `table` `aria-label`, `th` `scope="col"` + `aria-sort="ascending|descending|none"` + `aria-label` sort state, `td` semantic; `Pagination` `aria-label` page nav + `aria-current="page"`; `Empty` `role="status"` | WCAG / 08 |
| U-8 | Dark-First + Monospace | Numeric columns `font-family: var(--ix-font-mono)` + `font-variant-numeric: tabular-nums` + `text-align: right` via `align="numeric"`; renders correctly on `--ix-bg-root` `#0B0E14` + `--ix-bg-surface` `#111822` | 08 dark-first + monospace |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `DataTable.test.tsx` | Rendering + columns/rows + `align="numeric"` vs `"left"` + `loading` (skeleton `aria-busy`) + `empty` (`role="status"` honest text) + `pagination` slot |
| T-2 | `DataTable.numericAlignment.test.tsx` (or within `DataTable.test.tsx`) | Monospace tabular-nums + right alignment for numeric columns; string columns left-aligned |
| T-3 | `SortableHeader.test.tsx` | `aria-sort` ascending/descending/none + `aria-label` + click toggles `onSort` + keyboard `Enter`/`Space` toggles + icon `↑`/`↓`/`↕` |
| T-4 | `Pagination.test.tsx` | `page`/`pageSize`/`totalRows` + `onPageChange` + `First`/`Prev`/`Next`/`Last` + `Page X of Y` + `aria-current="page"` + disabled at bounds (`Prev`/`First` disabled on page 1) |
| T-5 | `formatters.test.ts` (or `formatUncertainty.test.ts`) | `formatUncertaintyInterval` (`"95% CI [-0.15, +0.22]"`), `formatSampleCount` (`"n=120"`), `formatPearsonR` (`"r=0.73"`), `formatPips`/`formatPercent` — pure, deterministic |
| T-6 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **429 tests — 100% pass** (or 429+ with accounting — see §8) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Table/grid primitives are additive — **0 removed / 0 modified** expected for existing tests (99 suites 429 tests from P03). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`DataTable` with `rows=[]` → `empty` (`role="status"` honest “No data”) not `loading`; `SortableHeader` with `sorted=false` → `aria-sort="none"`; `Pagination` with `totalRows=0` → `Page 1 of 1` or hidden + `Prev`/`Next` disabled; `formatUncertaintyInterval` with `lower===upper` → renders single bound correctly.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **429+ pass** — full log (must show 99 suites/429 baseline + new P04 suites) | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `#[0-9A-F]{3,6}` in `components/ui/` | Level II | 0 (proves token consumption) | `docs/evidence/ui009/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Accessibility spot-check | Level II | WCAG 2.1 AA — contrast >4.5:1 + focus + ARIA + keyboard (axe or `DataTable.test.tsx` excerpt) | `docs/evidence/ui009/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P04.md` with 20 sections | `DELIVERY_REPORT_UI-009-P04.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — DOM snapshots for table sorting/pagination if applicable, e.g., Storybook snapshots) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4.

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

**Expected:** `VITEST_EXIT:0` with **429+ pass** (P04 will be 99→~103 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

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

DA shall produce `DELIVERY_REPORT_UI-009-P04.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P04 — Data Tables & Visualization Grids |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P04` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §5 P04 (and §10 P01 token foundation) |
| 4 | Previous Baseline | P03 D-57: 99 suites / 429 tests · 414 backend · panel frames 6 suites/22 tests |
| 5 | Implementation Summary | What table/grid primitives were built (DataTable, SortableHeader, Pagination, formatters) + monospace alignment + token consumption |
| 6 | Files Created | List with nature (expected 5+ table files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe `Panel` integration) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (8 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 99/429 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 99/429 vs current (must be ≥99/429) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + table snapshots (numeric alignment, uncertainty intervals, pagination) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Data tables complete; modals in P05” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-009-P05 Modals, Overlays & Feedback Systems |
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
- Frontend: 99 suites / 429 tests
- Backend: 414 tests

New tests physically added:
- [N tests across DataTable/SortableHeader/Pagination/formatters suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [99 or 99+N] suites / [429 or 429+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-57 UI-009-P03 (99/429 + 414)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), Panel/PanelHeader/PanelActionBar/Collapsible (P03), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 99 suites / 429 frontend + 414 backend (D-57)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P09P03-01 (Badge children — safe, retained), O-P09P03-02 (evidence on main continuity)

New Phase Scope: Data Tables — DataTable/SortableHeader/Pagination/formatters (8 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P04, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P04 APPROVED** (version increment per governance, e.g., 8.74.0) |
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
[ BUILD_ORDER_UI-009-P04 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Table/Grid Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P04 Determination ]
         ↓
[ BUILD_ORDER_UI-009-P05 — Modals, Overlays & Feedback Systems ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | DataTable renders columns/rows + `align="numeric"` vs `"left"` + `loading` (`aria-busy`) + `empty` (`role="status"`) + `pagination` slot | Mandatory | `DataTable.test.tsx` + E-12 |
| AC-2 | Monospace tabular-nums + right alignment for `align="numeric"`; string columns left-aligned | Mandatory | `DataTable.numericAlignment.test.tsx` or within `DataTable.test.tsx` |
| AC-3 | SortableHeader `aria-sort` ascending/descending/none + `aria-label` + click + `Enter`/`Space` toggles `onSort` + icon `↑`/`↓`/`↕` via `var(--ix-color-accent)` | Mandatory | `SortableHeader.test.tsx` |
| AC-4 | Pagination `page`/`pageSize`/`totalRows` + `onPageChange` + `First`/`Prev`/`Next`/`Last` + `Page X of Y` + `aria-current="page"` + disabled at bounds | Mandatory | `Pagination.test.tsx` |
| AC-5 | Formatters `formatUncertaintyInterval` (`"95% CI [-0.15, +0.22]"`) + `formatSampleCount` (`"n=120"`) + `formatPearsonR` (`"r=0.73"`) — pure, deterministic | Mandatory | `formatters.test.ts` |
| AC-6 | All 5 table/grid primitives consume `var(--ix-*)` — 0 ad-hoc hex in `components/ui/` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-7 | Zero actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-8 | Zero LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-9 | 0 `dangerouslySetInnerHTML` + 0 `eval` in `components/ui/` | Mandatory | E-6/E-7 exit 1 |
| AC-10 | Frontend regression 429 pass (or 429+ with accounting) | Mandatory | E-1 vitest.log |
| AC-11 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-12 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking** — one failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P04 implementation only** — no P05–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P04 Design | §5 Phase Breakdown — P04 Data Tables & Visualization Grids |
| Preceding Baseline | D-57: 99 suites / 429 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-57 (99/429) preserved as previous baseline |
| §3 Single Active Phase | **P04 = ACTIVE**, P05–P06 = NOT AUTHORIZED, P01–P03 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P04 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-57 99/429 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + ad-hoc hex check |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no modal/audit work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P05 not authorized until P04 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-57 preserved |
| §24 P04 Controls | Applied — table/grid + formatters + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P04 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P04**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

