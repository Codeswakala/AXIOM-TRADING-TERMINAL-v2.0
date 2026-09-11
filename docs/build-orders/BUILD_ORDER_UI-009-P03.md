# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P03`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-56 — UI-009-P02 **APPROVED WITH OBSERVATIONS** (93 suites / 407 tests · 414 backend · exit 0) — Observations O-P09P02-01 (Input password/email undeclared, minor), O-P09P02-02 (evidence logs documentary tier)
**Phase:** UI-009-P03 — Workspace Panels & Frame Harmonization
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §5/P03 — Workspace Panels & Frame Harmonization)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried to UI-009)
**Preceding Milestone:** UI-009-P02 (D-56 APPROVED WITH OBSERVATIONS) — 93 suites / 407 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 93/407 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P03 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — all verification commands in §8.2 are provided in **both PowerShell (Windows) and Bash (Linux/macOS)**. Either platform produces identical verification outcomes.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P03` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — UI-009 Design Plan APPROVED WITH OBSERVATIONS (O-009-01, O-009-02 — closed D-55) |
| Preceding Milestone | UI-009-P02 (D-56) — 93/407 + 414 |
| Next Milestone | UI-009-P03 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (panel frame harmonization — presentation wrappers, no business logic) |

---

## 2. PHASE OBJECTIVE

Harmonize **workspace panel infrastructure** across all AXIOM workspaces (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/research-management` and other primary workspaces) by unifying **panel wrappers, headers, action bars, and collapsible containers** using the **P01 5-tier tokens** and **P02 atomic primitives** (Button, Card, Accordion, etc.) — no data table, modal, or whole-surface work.

This phase is **panel frame unification, not workspace content rewrite.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Panel Frame Primitive — `Panel.tsx` + `Panel.css`** | Unified wrapper for all workspace panels: header slot, `actionBar` slot, `collapsible` prop (`aria-expanded`/`aria-controls`), `padding` via `var(--ix-space-*)`, variants `default` / `raised` / `ghost` |
| 2 | **Panel Header — `PanelHeader.tsx` + `PanelHeader.css`** | Title + subtitle + icon + `actions` slot (Button group); heading hierarchy `h2`/`h3` with typography tokens; `aria-labelledby` |
| 3 | **Panel Action Bar — `PanelActionBar.tsx` + `PanelActionBar.css`** | Horizontal action grouping for panel header/body/footer; spacing via `--ix-space-*`, wraps with flex, respects `prefers-reduced-motion` |
| 4 | **Collapsible Container — `Collapsible.tsx` + `Collapsible.css`** | Reusable collapsible section (extends P02 Accordion pattern for panel-level collapse): trigger + `aria-expanded`, `aria-controls`, keyboard `Enter`/`Space`, motion `var(--ix-motion-fast) 120ms` → `0ms` reduced; smooth `height` transition via tokens |
| 5 | **Workspace Panel Integration** | Apply `Panel` + `PanelHeader` + `PanelActionBar` + `Collapsible` to at least **3 representative workspaces** (e.g., `/intelligence`, `/charts`, `/governance`) — prove reuse, not just library existence |
| 6 | **Token Consumption Enforcement** | All panel frames via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing / 0 `dangerouslySetInnerHTML` in `components/ui/` |
| 7 | **Comprehensive State Tests** | Per-component suites covering rendering + props + collapsible states + keyboard + ARIA + token consumption |
| 8 | **Evidence Package** | Logs committed to `docs/evidence/ui009/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash commands produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Data tables & visualization grids (sortable headers, monospace alignments, uncertainty formatters, pagination) | **UI-009-P04** scope |
| 2 | Modals, Command Palette styling, dialogs, skeleton loaders, toasts, error banners | P05 scope |
| 3 | Whole-surface harmonization & completion checkpoint | P06 scope |
| 4 | Atomic primitives themselves (`Button`/`Input`/`Select`/`Badge`/`Card`/`StatusChip`/`Tooltip`/`Accordion`) | **P02 already COMPLETE** — reuse, do not rewrite |
| 5 | 5-tier token hierarchy or `theme.ts` contracts | **P01 already COMPLETE** — reuse, do not redefine |
| 6 | New backend endpoints, migrations, schema changes | No persistence change |
| 7 | WebSocket / real-time push | Not in P03 design |
| 8 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 9 | External LLM integration (OpenAI/Anthropic/LangChain etc.) | Constitutionally prohibited — 12 Part I §5 |
| 10 | Order / trade / execution / broker controls | Absolutely prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Panel Frame Architecture (Per Design Plan §5 P03)

- **Location:** `frontend/src/components/ui/` (reuse P02 library path — same `frontend/src/components/ui/` declared in P02: `Button.tsx` etc.) — all panel frames **must live in the same library path** for single import surface.
- **Composition:** `Panel` wraps `PanelHeader` + `PanelActionBar` + `children` (body) + optional `Collapsible` sections; `Panel.css` consumes Tier 3 Component tokens (`--ix-panel-*`, `--ix-card-*`, `--ix-space-*`) + Tier 2 Semantic (`--ix-bg-surface`, `--ix-border-subtle`).
- **Token Consumption:** Every visual value (background, border, spacing, typography, elevation, motion) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…`) outside `tokens.css`, no hardcoded `px` spacing outside `var(--ix-space-*)`, no ad-hoc `transition` duration outside `var(--ix-motion-fast)`.
- **No Runtime Style Injection:** No `dangerouslySetInnerHTML` for style/theme injection; no `eval`/`new Function`; no raw `<script>`; tokens are static CSS custom properties.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); bounded context `frontend/src/components/ui/` isolated; no new bounded context; no circular deps; no backend coupling; `Panel` is presentation wrapper, not business logic.

### 4.3 Interaction Contracts

| Component | Contract |
|-----------|----------|
| `Panel` | `header` (ReactNode — typically `PanelHeader`) + `actionBar` (ReactNode — typically `PanelActionBar`) + `children` + `collapsible?: boolean` + `defaultCollapsed?: boolean` + `onToggle?` + `padding?: "none"|"sm"|"md"|"lg"` |
| `PanelHeader` | `title: string` + `subtitle?: string` + `icon?: ReactNode` + `actions?: ReactNode` (`Button` group) + `headingLevel?: 2|3` — renders `aria-labelledby` linking title id |
| `PanelActionBar` | `children` (Button group) + `align?: "start"|"end"|"between"` + `wrap?: boolean` — flex layout via tokens |
| `Collapsible` | `title: string` + `children` + `defaultExpanded?: boolean` + `expanded?: boolean` (controlled) + `onToggle?` — trigger `aria-expanded` + `aria-controls` + content id, keyboard `Enter`/`Space`, motion `var(--ix-motion-fast)` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in panel frames | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` — 0 matches |
| 4 | No `eval` / `new Function` in panel frames | Grep `eval\(|new Function` — 0 matches |
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
| U-1 | Brand Fidelity | All panel frames via tokens (`--ix-bg-surface`, `--ix-border-subtle`, `--ix-space-*`, `--ix-color-accent`) — no inline hex | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast | Text/background >4.5:1 (panel title, header actions, collapsible trigger); large headings >3:1 — inherited from P01 `7.2:1`/`6.8:1` | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding | Panel status (if any) includes text label + symbol — reuse `Badge`/`StatusChip` pattern | 02 §Design, 08 |
| U-4 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` on `Panel` interactive, `Collapsible` trigger, `PanelActionBar` buttons | WCAG 2.4.7 |
| U-5 | Motion Restraint | Collapsible transitions via `var(--ix-motion-fast)` `120ms`; respects `@media (prefers-reduced-motion: reduce)` → `0ms` | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` traverses Panel → Header actions → Collapsible triggers; `Enter`/`Space` toggles `Collapsible`/`Panel` collapse | 08 keyboard |
| U-7 | ARIA | `Panel` `aria-labelledby` → `PanelHeader` title id; `Collapsible` `aria-expanded`/`aria-controls`/`aria-labelledby`; `PanelActionBar` not ARIA role (grouped via flex) | WCAG / 08 |
| U-8 | Dark-First | Panels render correctly on `--ix-bg-root` `#0B0E14` + `--ix-bg-surface` `#111822` + `.theme-light` override | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `Panel.test.tsx` | Variants (default/raised/ghost) + header/actionBar/children slots + padding + `aria-labelledby` + `collapsible` states |
| T-2 | `PanelHeader.test.tsx` | Title/subtitle/icon/actions + headingLevel `h2`/`h3` + `aria-labelledby` |
| T-3 | `PanelActionBar.test.tsx` | Align/wrap + button group rendering + flex layout |
| T-4 | `Collapsible.test.tsx` | Collapsed/expanded + `aria-expanded`/`aria-controls` + keyboard `Enter`/`Space` + motion `120ms` |
| T-5 | `Panel.integration.test.tsx` | `Panel` + `PanelHeader` + `PanelActionBar` + `Collapsible` composed together; applied to at least one workspace page mock |
| T-6 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **407 tests — 100% pass** (or 407+ with accounting — see §8) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Panel frames are additive — **0 removed / 0 modified** expected for existing tests (96 pre-UI-009 + 99 UI-008 + 26 P02 atomic + 5 P01 tokens). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

Panel `collapsible` disabled → not togglable; `Collapsible` `defaultExpanded=false` → content hidden initially and not focusable; keyboard `Enter` on disabled trigger → no toggle.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **407+ pass** — full log (must show 93 suites/407 baseline + new P03 suites) | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `#[0-9A-F]{3,6}` in `components/ui/` | Level II | 0 (proves token consumption) | `docs/evidence/ui009/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Accessibility spot-check | Level II | WCAG 2.1 AA — contrast >4.5:1 + focus + ARIA + keyboard (axe or `Panel.test.tsx` excerpt) | `docs/evidence/ui009/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P03.md` with 20 sections | `DELIVERY_REPORT_UI-009-P03.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — DOM snapshots for panel frames if applicable, e.g., Storybook snapshots) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4.

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs.

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui009/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui009/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui009/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui009/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui009/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui009/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **407+ pass**, `PYTEST_EXIT:0` with **414 pass**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | `Select-String -Path frontend/src -Recurse -Pattern "buy|sell|place.*order|execute.*trade|order.*ticket" -CaseSensitive:$false 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_actuation.log; if ($?) { echo "ACTUATION_GREP_EXIT:0" } else { echo "ACTUATION_GREP_EXIT:1" }` <br> *Note: In PowerShell, exit 0 = matches found (BLOCKER), exit 1 = clean. Use `Select-String` inverse: no output + `$LASTEXITCODE 1` = CLEAN.* <br> **Simpler cross-platform (Git Bash on Windows):** If you have Git for Windows, run the **Bash column** in Git Bash — identical to DA. | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | `Select-String -Path frontend -Recurse -Pattern "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" -CaseSensitive:$false 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_llm.log` <br> **Or Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `components/ui/` | `Select-String -Path frontend/src/components/ui -Recurse -Pattern "dangerouslySetInnerHTML" 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_sandbox_danger.log` <br> **Or Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | `Select-String -Path frontend/src/components/ui -Recurse -Pattern "eval\(|new Function" 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_eval.log` <br> **Or:** `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `components/ui/` | `Select-String -Path frontend/src/components/ui -Recurse -Pattern "#[0-9A-Fa-f]{3,6}" 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_ad_hoc_hex.log` <br> **Or:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | `Select-String -Path frontend -Recurse -Pattern "api.?key|secret|jwt.?secret|password" -CaseSensitive:$false 2>&1 | Tee-Object -FilePath docs/evidence/ui009/grep_secrets.log` <br> **Or:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**For reliable cross-platform results on Windows, the DA strongly recommends using *Git Bash* (bundled with Git for Windows) — it runs the *identical Bash commands* as DA's Linux.** All `grep` exit codes are identical: **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion test fixtures, which must be documented).**

#### 3. Documentation Diffs (Both Platforms)

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui009/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui009/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui009/changelog_diff.log` |

**All logs must be committed to `docs/evidence/ui009/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both are deterministic. If you use **Git Bash on Windows, your `grep` exit codes will be identical to DA's Linux codes** — ideal for direct comparison.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-009-P03.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P03 — Workspace Panels & Frame Harmonization |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P03` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §5 P03 (and §10 P01 token foundation) |
| 4 | Previous Baseline | P02 D-56: 93 suites / 407 tests · 414 backend · panel library path `frontend/src/components/ui/` |
| 5 | Implementation Summary | What panel frames were built (Panel/PanelHeader/PanelActionBar/Collapsible) + integration into ≥3 workspaces + token consumption |
| 6 | Files Created | List with nature (expected 4+ panel frame files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe workspace pages) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (8 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 93/407 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 93/407 vs current (must be ≥93/407) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + panel frame snapshots |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Panel frames complete; data tables in P04” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-009-P04 Data Tables & Visualization Grids |
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
- Frontend: 93 suites / 407 tests
- Backend: 414 tests

New tests physically added:
- [N tests across Panel/PanelHeader/PanelActionBar/Collapsible suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [93 or 93+N] suites / [407 or 407+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-56 UI-009-P02 (93/407 + 414)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion (P02), InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 93 suites / 407 frontend + 414 backend (D-56)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P09P02-01 (Input password/email — safe extension) to be declared in P03 NO DEVIATIONS note; O-P09P02-02 (evidence on main continuity)

New Phase Scope: Workspace Panels — Panel/PanelHeader/PanelActionBar/Collapsible (8 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P03, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P03 APPROVED** (version increment per governance, e.g., 8.73.0) |
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
[ BUILD_ORDER_UI-009-P03 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Panel Frame Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P03 Determination ]
         ↓
[ BUILD_ORDER_UI-009-P04 — Data Tables & Visualization Grids ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Panel renders variants `default/raised/ghost`, slots header/actionBar/children, padding via `var(--ix-space-*)`, `aria-labelledby` | Mandatory | `Panel.test.tsx` + E-12 |
| AC-2 | PanelHeader renders title/subtitle/icon/actions + `headingLevel` `h2`/`h3` + `aria-labelledby` | Mandatory | `PanelHeader.test.tsx` |
| AC-3 | PanelActionBar renders align/wrap + button group flex layout | Mandatory | `PanelActionBar.test.tsx` |
| AC-4 | Collapsible renders collapsed/expanded + `aria-expanded`/`aria-controls` + keyboard `Enter`/`Space` + motion `120ms` → `0ms` reduced | Mandatory | `Collapsible.test.tsx` |
| AC-5 | Panel composed: `Panel` + `PanelHeader` + `PanelActionBar` + `Collapsible` integrated together; applied to ≥3 workspaces | Mandatory | `Panel.integration.test.tsx` + workspace evidence |
| AC-6 | All 4 panel frames consume `var(--ix-*)` — 0 ad-hoc hex in `components/ui/` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-7 | Zero actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-8 | Zero LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-9 | 0 `dangerouslySetInnerHTML` + 0 `eval` in `components/ui/` | Mandatory | E-6/E-7 exit 1 |
| AC-10 | Frontend regression 407 pass (or 407+ with accounting) | Mandatory | E-1 vitest.log |
| AC-11 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-12 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking** — one failure = CORRECT/RESUBMIT. AC-6 inherently re-verifies **O-009-01/O-009-02** remain closed (legacy hex 0 + contrast via P01 tokens).

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P03 implementation only** — no P04–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P03 Design | §5 Phase Breakdown — P03 Workspace Panels & Frame Harmonization |
| Preceding Baseline | D-56: 93 suites / 407 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-56 (93/407) preserved as previous baseline |
| §3 Single Active Phase | **P03 = ACTIVE**, P04–P06 = NOT AUTHORIZED, P01–P02 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P03 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-56 93/407 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + ad-hoc hex check |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no table/modal/audit work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P04 not authorized until P03 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-56 preserved |
| §24 P03 Controls | Applied — panel frames + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P03 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P03**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

