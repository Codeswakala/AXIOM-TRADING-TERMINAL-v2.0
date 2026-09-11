# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P01`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-68 — UI-011 Design Plan **APPROVED WITH OBSERVATIONS** (O-011-01 — matrix summary count harmonization, non-blocking)
**Phase:** UI-011-P01 — Information Hierarchy & Spacing Proportion Calibration
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §10 Proposed P01)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-010 COMPLETE (D-67) — 136 suites / 556 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 136/556 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P01 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P01` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01) |
| Preceding Milestone | UI-010 COMPLETE (D-67) — 136/556 + 414 |
| Next Milestone | UI-011-P01 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (hierarchy tokens + spacing rhythm — presentation polish, no business logic) |

---

## 2. PHASE OBJECTIVE

Establish the **4-level information hierarchy tokens** and **4px grid spacing proportion rhythm** for AXIOM by codifying **visual hierarchy tokens** (`--ix-hierarchy-*`, `--ix-elevation-level-*`) and **harmonizing spacing** (`--ix-space-*` 4px through 32px) across **shell Regions A–F and panel/card frames** — per `12` Part VI §17 (Consistent Spacing) and §10 Proposed P01.

This phase is **hierarchy + spacing proportion calibration, not panel balance beyond spacing, micro-interaction, typography, or whole-surface audit.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Hierarchy Tokens — `tokens.css` + `theme.ts`** | Define visual hierarchy tokens: `--ix-hierarchy-level-1` (Mission-Critical Telemetry — e.g., `font-weight: 700`, `elevation: var(--ix-elevation-level-4)`) → `--ix-hierarchy-level-2` (Active Context & Signals) → `--ix-hierarchy-level-3` (Supporting Analytics) → `--ix-hierarchy-level-4` (Administrative & Meta) + `--ix-elevation-level-1..4` (`box-shadow` tokens via `var(--ix-shadow-*)`) — all via `var(--ix-*)` |
| 2 | **Spacing Rhythm Harmonization — `Panel.css`, `Card.css`, `InstitutionalWorkspaceShell.css`** | Harmonize interior paddings/margins/gaps across shell Regions A–F and `Panel`/`Card` frames to **strict 4px/8px/12px/16px/24px/32px scale** via `var(--ix-space-*)` — replace any ad-hoc `margin: 10px` / `padding: 15px` outside scale with nearest token step |
| 3 | **Visual Weight Calibration** | Apply hierarchy tokens to workspace page headers (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `SignalInvestigationPage.tsx` headers) — Level 1 telemetry visually dominant via `--ix-hierarchy-level-1`, Level 4 meta via `--ix-hierarchy-level-4` (subtle, muted) |
| 4 | **Test Harness — `spacingHierarchy.test.tsx` + invariants** | New suite `spacingHierarchy.test.tsx` (hierarchy tokens existence + heading level mapping) + `theme.ts` contracts; plus security/token invariants (`ui011_p01_security_invariants.test.ts`) — total +4 to +8 tests |
| 5 | **Token Consumption Enforcement** | All hierarchy/spacing primitives via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded spacing outside `var(--ix-space-*)` |
| 6 | **Evidence Package** | Logs committed to `docs/evidence/ui011/` (new evidence directory for UI-011) — vitest, tsc/vite, greps, diffs — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Panel balance & workspace frame harmonization beyond spacing (header/body/footer padding uniformity across 7 workspaces) | **UI-011-P02** scope — P01 is hierarchy + spacing rhythm only |
| 2 | Micro-interaction consistency & motion restraint (`120ms` transitions, hover states, `prefers-reduced-motion` re-verification beyond hierarchy) | P03 scope |
| 3 | Optical typography & monospace financial data polish (`0.75rem`/`0.9rem`/`0.85rem` hierarchy, `tabular-nums` re-verification beyond hierarchy) | P04 scope |
| 4 | Cross-workspace cohesion & visual regression audit | P05 scope |
| 5 | Whole-surface Version 1.0 handover & completion checkpoint | P06 scope |
| 6 | Mobile viewports (<768px) | **DEFERRED** per Design Plan §10 — post-1.0 |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P01 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Hierarchy & Spacing Architecture (Per Design Plan §10 + §14 Institutional Polish)

- **Location (Recommended):** `frontend/src/workstation/design/tokens.css` — extend Tier 1 Foundation with hierarchy/elevation tokens; `frontend/src/workstation/design/theme.ts` — typed contracts `HIERARCHY_TOKENS`, `ELEVATION_TOKENS`; DA may alternatively extend `frontend/src/styles/` if reusing existing style file, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **Hierarchy Tokens:** `--ix-hierarchy-level-1: 700 weight + var(--ix-elevation-level-4)` / `--ix-hierarchy-level-2: 600 + var(--ix-elevation-level-3)` / `--ix-hierarchy-level-3: 500 + var(--ix-elevation-level-2)` / `--ix-hierarchy-level-4: 400 + var(--ix-elevation-level-1)` (or DA's equivalent via `font-weight` + `box-shadow`/`opacity` + `font-size` — must be via `var(--ix-*)` tokens, not hardcoded `font-weight: 700` outside tokens). Allow DA to define hierarchy via `font-size` (`1.2rem` → `0.75rem`) + `elevation` if preferred, but must be tokenized.
- **Spacing Rhythm:** `--ix-space-1: 4px`, `--ix-space-2: 8px`, `--ix-space-3: 12px`, `--ix-space-4: 16px`, `--ix-space-6: 24px`, `--ix-space-8: 32px` (already in P01 5-tier, but P01 must **enforce uniform usage** in `Panel.css`/`Card.css`/`InstitutionalWorkspaceShell.css` — replace ad-hoc `margin: 10px` with `margin: var(--ix-space-2)` etc.).
- **Elevation Tokens:** `--ix-elevation-level-1: 0 1px 2px rgba(0,0,0,0.05)` through `--ix-elevation-level-4: 0 8px 24px rgba(0,0,0,0.15)` (or DA's shadow scale via `var(--ix-shadow-*)`).
- **Token Consumption:** Every visual value (hierarchy `font-weight`/`font-size`, spacing `margin`/`padding`/`gap`, elevation `box-shadow`) **must reference P01 tokens** (`var(--ix-*)` or `var(--ix-elevation-level-*)`/`var(--ix-hierarchy-level-*)`). No inline `font-weight: 700` outside `tokens.css`, no hardcoded `margin: 10px` outside `var(--ix-space-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/design/tokens.css` + `components/ui/`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; `EmptyState`/`ErrorBanner` already in UI-010 P03 — P01 spacing refinement not business logic.

### 4.3 Interaction Contracts

| Component / Token | Contract |
|-----------|----------|
| `--ix-hierarchy-level-1..4` | `font-weight` / `font-size` / `elevation` combinations via tokens — Level 1 most prominent, Level 4 most muted |
| `--ix-elevation-level-1..4` | `box-shadow` tokens — Level 1 subtle `0 1px 2px`, Level 4 strong `0 8px 24px` |
| `--ix-space-1..8` | `4px` → `32px` scale — all `margin`/`padding`/`gap` must be `var(--ix-space-*)` |
| `InstitutionalWorkspaceShell.tsx` Regions | Region A header, Region B nav, Region C workspace — spacing via `var(--ix-space-*)` + hierarchy tokens for titles |
| `Panel.css` / `Card.css` | Interior padding `var(--ix-space-4)` / `var(--ix-space-6)` etc. — harmonized across 7 workspaces |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in hierarchy/spacing module | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/design/` — 0 matches |
| 4 | No `eval` / `new Function` in module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/design/` + `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |
| 7 | No credential exposure via hierarchy (no `value` of `<input>` in DOM attributes) | Code review — hierarchy tokens must not log input values |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — hierarchy module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — hierarchy module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/design/ frontend/src/components/ui/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Information Hierarchy Tokens | `--ix-hierarchy-level-1..4` codified and typed in `theme.ts` (font-weight/size/elevation combos) | `12` Part V §5, `16`, Design Plan §11 AC-01 |
| U-2 | Panel Interior Spacing Uniformly Conforms to 4px/8px/12px/16px/24px/32px Scale | DOM snapshot & CSS token audit — `Panel` header `var(--ix-space-4)`, body `var(--ix-space-6)`, footer `var(--ix-space-3)` etc. | `12` Part VI §17 (Consistent Spacing) — AC-02 |
| U-3 | Micro-interaction Transitions Strictly Adhere to `var(--ix-motion-fast)` `120ms` | CSS transition audit — all `transition: var(--ix-motion-fast)` — not yet P03 scope, but hierarchy must not introduce uncurved `transition: 0.5s` | `12` Part VI §17 (Subtle Animations) — AC-03 |
| U-4 | Numerical Data Tables Strictly Render with Monospace `tabular-nums` | Table formatter unit tests — already in P04, but hierarchy must preserve `font-variant-numeric: tabular-nums` on numbers | `08_UI_UX_SPEC.md`, `03` — AC-04 |
| U-5 | Zero Ad-hoc Hex Literals Across `frontend/src/` (outside `tokens.css`) | `grep_ad_hoc_hex.log` exit 1 | `16_BRAND_GOVERNANCE_STANDARD.md` — AC-05 |
| U-6 | Zero Actuation, Zero External LLMs, Zero Dangerous innerHTML/eval | Whole-repo security greps exit 1 | `17_INSTITUTIONAL_SECURITY_STANDARD.md` — AC-06 |
| U-7 | Full Platform Regression Suite Passes with 100% Success (≥556 frontend, 414 backend) | Vitest & Pytest execution logs | Definition of Done — AC-07 |
| U-8 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | `tsc.log` and `vite_build.log` | Definition of Done — AC-08 |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `spacingHierarchy.test.tsx` | Hierarchy tokens `--ix-hierarchy-level-1..4` existence + `theme.ts` `HIERARCHY_TOKENS` contract + `Panel` header/body spacing via `var(--ix-space-*)` |
| T-2 | `panelSpacing.test.tsx` (or within `spacingHierarchy.test.tsx`) | Panel interior spacing uniform `4px`/`8px`/`12px`/`16px`/`24px`/`32px` scale — `Panel` `padding: var(--ix-space-*)` |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **556 tests — 100% pass** (or 556+ with accounting — see §8) — P01 adds hierarchy/spacing tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Hierarchy/spacing refinement is additive — **0 removed / 0 modified** expected for existing tests (136 suites 556 tests from UI-010 COMPLETE). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`spacingHierarchy` with missing `--ix-hierarchy-level-2` → test fails; `Panel` with hardcoded `padding: 10px` (outside scale) → test fails via `grep` or `getComputedStyle` token check; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — new `ui011` evidence directory for UI-011)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **556+ pass** — full log (must show 136 suites/556 baseline + new P01 suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/design/` + `components/ui/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Contrast/hierarchy audit (visual) | Level II | Hierarchy token existence + panel spacing via `spacingHierarchy.test.tsx` or `accessibility.log` | `docs/evidence/ui011/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P01.md` with 20 sections | `DELIVERY_REPORT_UI-011-P01.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `spacingHierarchy.test.tsx` DOM snapshot of hierarchy levels) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **New evidence directory `docs/evidence/ui011/` is required for UI-011 (separate from `ui010` `136/556` baseline).**

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

**Expected:** `VITEST_EXIT:0` with **556+ pass** (P01 will be 136→~138 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

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

DA shall produce `DELIVERY_REPORT_UI-011-P01.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P01 — Information Hierarchy & Spacing Refinement |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P01` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §10 (Proposed P01) |
| 4 | Previous Baseline | UI-010 COMPLETE (D-67): 136 suites / 556 tests · 414 backend · whole-surface harmonization |
| 5 | Implementation Summary | What hierarchy/spacing refinement was built (hierarchy tokens, spacing harmonization, visual weight calibration) + token consumption |
| 6 | Files Created | List with nature (expected hierarchy tokens + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `tokens.css` + `theme.ts` + `Panel.css`/`Card.css`/`InstitutionalWorkspaceShell.css` + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (6 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 136/556 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 136/556 vs current (must be ≥136/556) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Hierarchy visual proof (spacing snapshots, hierarchy token existence) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Hierarchy & spacing complete; panel balance in P02” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-011-P02 Panel Balance & Workspace Frame Harmonization |
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
- Frontend: 136 suites / 556 tests
- Backend: 414 tests

New tests physically added:
- [N tests across spacingHierarchy tests]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [136 or 136+N] suites / [556 or 556+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-67 UI-010 COMPLETE (136/556 + 414) + D-68 Design Plan (1 minor observation O-011-01)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier (with --ix-hierarchy-*), theme.ts, SkipLink, RouteAnnouncer, EmptyState, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, Panel/PanelHeader/PanelActionBar/Collapsible, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 136 suites / 556 frontend + 414 backend (D-67) — plus D-68 design plan (no code)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-011-01 (matrix summary harmonization — documentary)

New Phase Scope: Information Hierarchy — hierarchy tokens + spacing harmonization (6 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P01, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P01 APPROVED** (version increment per governance, e.g., 8.83.0) |
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
[ BUILD_ORDER_UI-011-P01 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Hierarchy/Spacing Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P01 Determination ]
         ↓
[ BUILD_ORDER_UI-011-P02 — Panel Balance & Workspace Frame Harmonization ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Information hierarchy tokens (`--ix-hierarchy-*`) codified and typed in `theme.ts` | Mandatory | `spacingHierarchy.test.tsx` E-10 |
| AC-2 | Panel interior spacing uniformly conforms to 4px/8px/12px/16px/24px/32px scale | Mandatory | DOM snapshot & CSS token audit — `Panel.css` etc. |
| AC-3 | Micro-interaction transitions strictly adhere to `var(--ix-motion-fast)` (120ms) | Mandatory | CSS transition audit |
| AC-4 | Numerical data tables strictly render with monospace `tabular-nums` | Mandatory | Table formatter unit tests |
| AC-5 | Zero ad-hoc hex literals across `frontend/src/` (outside `tokens.css`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-6 | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-7 | Full platform regression suite passes with 100% success (≥556 frontend, 414 backend) | Mandatory | E-1/E-2 vitest/pytest logs |
| AC-8 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | Mandatory | E-3 tsc/vite logs |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**Observation O-011-01 (matrix summary) will be verified as harmonized via P01 delivery `panelBalance.test.tsx` later, but AC-1/AC-2 already prove hierarchy/spacing.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P01 implementation only** — no P02–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P01 Design | §10 Proposed P01 (7-part re-baseline — hierarchy tokens + spacing harmonization) |
| Preceding Baseline | D-67: 136 suites / 556 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-67 (136/556) preserved as previous baseline |
| §3 Single Active Phase | **P01 = ACTIVE**, P02–P06 = NOT AUTHORIZED, UI-010 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §10 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-67 136/556 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no panel balance beyond spacing |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P02 not authorized until P01 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-68 preserved |
| §24 P01 Controls | Applied — hierarchy tokens + spacing rhythm |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P01 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P01**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

