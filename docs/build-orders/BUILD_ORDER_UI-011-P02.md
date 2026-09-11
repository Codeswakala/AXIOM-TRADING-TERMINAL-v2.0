# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P02`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-69 — UI-011-P01 **APPROVED** (138 suites / 564 tests · 414 backend · exit 0) — Observation O-P11P01-01 (evidence logs documentary tier, continuity — O-011-01 now closed)
**Phase:** UI-011-P02 — Panel Balance & Workspace Frame Harmonization
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §5/P02 — Panel Balance & Workspace Frame Harmonization)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-011-P01 (D-69 APPROVED) — 138 suites / 564 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 138/564 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P02 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P02` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01 — closed D-69 as 5 RETAIN+3 EXTEND+1 DEFER) |
| Preceding Milestone | UI-011-P01 (D-69) — 138/564 + 414 |
| Next Milestone | UI-011-P02 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (panel balance — presentation padding/elevation harmonization, no business logic) |

---

## 2. PHASE OBJECTIVE

Harmonize **panel balance and workspace frame** across all 7 primary workspace surfaces (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/trade-plans`, `/journal`, `/compare-scenarios`) by **standardizing header/body/footer padding and card container elevation/balance** using **P01 hierarchy/spacing tokens** and **P01–P03 Panel primitives** — per `12` Part VI §17 (Balanced Information Density, Uniform Panel Behaviour).

This phase is **panel padding/elevation balance, not information hierarchy redefinition (P01), micro-interaction (P03), typography (P04), or whole-surface audit (P06).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Panel Balance Harmonization — `Panel.css` + `Card.css` + `InstitutionalWorkspaceShell.css`** | Harmonize interior `padding`/`margin`/`gap` of `Panel` header (`var(--ix-space-4)` 16px), body (`var(--ix-space-6)` 24px), action bar (`var(--ix-space-3)` 12px), footer (`var(--ix-space-3)`), and `Card` padding (`var(--ix-space-4)`/`var(--ix-space-6)`) across 7 workspaces — uniform visual balance |
| 2 | **Workspace Frame Harmonization — 7 Workspace Pages** | Apply `Panel` interior balance to `InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `SignalInvestigationPage.tsx`, `GovernanceEvidencePage.tsx`, `TradePlanningPage.tsx`, `ManualJournalPage.tsx`, `ScenarioComparisonPage.tsx` — each page's `Panel`/`Card` containers must show consistent header/body/footer spacing |
| 3 | **Elevation Balance — `--ix-elevation-level-1..4` Application** | Apply elevation tokens `--ix-elevation-level-1` (`0 1px 2px`) → `--ix-elevation-level-4` (`0 8px 24px`) via `var(--ix-elevation-level-*)` to `Panel`/`Card` variants (`default` Level 2, `raised` Level 3, `ghost` Level 1) — consistent shadow hierarchy |
| 4 | **Test Harness — `panelBalance.test.tsx` + invariants** | New suite `panelBalance.test.tsx` (panel padding uniformity, card elevation, header/body/footer spacing) plus security/token invariants — total +4 to +8 tests |
| 5 | **Token Consumption Enforcement** | All panel balance via `var(--ix-*)` / `var(--ix-elevation-level-*)` / `var(--ix-space-*)` — 0 ad-hoc hex / 0 hardcoded spacing outside tokens |
| 6 | **Evidence Package** | Logs committed to `docs/evidence/ui011/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Micro-interaction consistency & motion restraint (`120ms` transitions, hover states, `prefers-reduced-motion` re-verification beyond panel balance) | **UI-011-P03** scope |
| 2 | Optical typography & monospace financial data polish (`0.75rem`/`0.9rem`/`0.85rem`, `tabular-nums` re-verification beyond hierarchy) | P04 scope |
| 3 | Cross-workspace cohesion & visual regression audit | P05 scope |
| 4 | Whole-surface Version 1.0 handover & completion checkpoint | P06 scope |
| 5 | Mobile viewports (<768px) | **DEFERRED** per Design Plan §10 — post-1.0 |
| 6 | Information hierarchy tokens redefinition (`--ix-hierarchy-level-*`) | **P01 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P02 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Panel Balance Architecture (Per Design Plan §5 P02 + 12 Part VI §17 Balanced Information Density / Uniform Panel Behaviour)

- **Location (Recommended):** `frontend/src/components/ui/Panel.css` — interior `padding` harmonization for `.ix-panel__header { padding: var(--ix-space-4); }`, `.ix-panel__body { padding: var(--ix-space-6); }`, `.ix-panel__action-bar { gap: var(--ix-space-3); }`, `.ix-panel__footer { padding: var(--ix-space-3); }`; `frontend/src/components/ui/Card.css` — `.ix-card { padding: var(--ix-space-4); }` / `.ix-card--raised { box-shadow: var(--ix-elevation-level-3); }`; `frontend/src/workstation/design/tokens.css` — elevation tokens already in P01, reuse. DA may alternatively harmonize via `frontend/src/styles/` if reusing existing style file, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only.
- **Harmonization Rule:** Every `Panel` across 7 workspaces must have **identical interior spacing scale** — header `16px` (`--ix-space-4`), body `24px` (`--ix-space-6`), footer/action bar `12px` (`--ix-space-3`) — via tokens, not ad-hoc `padding: 10px`. `Card` elevation `default` → Level 2, `raised` → Level 3 via `var(--ix-elevation-level-*)`.
- **Workspace Pages:** `InstitutionalIntelligencePage.tsx` (ReportSection/ReportCard), `ChartWorkspacePage.tsx` (ProfessionalMarketOverview), `SignalInvestigationPage.tsx` (InvestigationPlanningFrame), `GovernanceEvidencePage.tsx` (AuditExplorerPanel), `TradePlanningPage.tsx`, `ManualJournalPage.tsx`, `ScenarioComparisonPage.tsx` — each page's `Panel`/`Card` must show harmonized padding/elevation — no page-specific hardcoded `margin: 10px`.
- **Token Consumption:** Every visual value (padding `var(--ix-space-*)`, elevation `var(--ix-elevation-level-*)`, background `var(--ix-bg-surface)` / `var(--ix-bg-surface-raised)`) **must reference P01 5-tier tokens** (`var(--ix-*)`). No inline `padding: 10px` outside `var(--ix-space-*)`, no inline `box-shadow` outside `var(--ix-elevation-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `components/ui/Panel.css` + `workstation/design/tokens.css`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; panel balance is presentation spacing/elevation, not business logic.

### 4.3 Interaction Contracts

| Component / Token | Contract |
|-----------|----------|
| `Panel` | `header`/`body`/`actionBar`/`footer` slots — body `padding: var(--ix-space-6)` — header `padding: var(--ix-space-4)` — elevation via `var(--ix-elevation-level-*)` |
| `Card` | `padding: var(--ix-space-4)` (`default`) / `box-shadow: var(--ix-elevation-level-3)` (`raised`) — via tokens |
| `--ix-elevation-level-1..4` | `0 1px 2px` → `0 8px 24px` shadows — Level 1 subtle, Level 4 strong — via `var(--ix-elevation-level-*)` |
| `--ix-space-1..8` | `4px` → `32px` scale — all `margin`/`padding`/`gap` must be `var(--ix-space-*)` |
| Workspace Pages | Each `Panel`/`Card` interior spacing harmonized — visual balance via tokens |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in panel balance module | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` — 0 matches |
| 4 | No `eval` / `new Function` in module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — panel balance module | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — panel balance module | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/components/ui/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Panel Balance | `Panel` header `var(--ix-space-4)` 16px, body `var(--ix-space-6)` 24px, footer/action bar `var(--ix-space-3)` 12px — uniform across 7 workspaces | `12` Part VI §17 (Balanced Information Density, Uniform Panel Behaviour) |
| U-2 | Card Balance | `Card` padding `var(--ix-space-4)` 16px / `var(--ix-space-6)` 24px via tokens — uniform | `12` Part VI §17 |
| U-3 | Elevation Balance | `Panel`/`Card` `default` Level 2 → `raised` Level 3 via `var(--ix-elevation-level-*)` (`0 1px 2px` → `0 4px 12px` → `0 8px 24px`) — consistent shadow hierarchy | `12` Part VI §17 (Uniform Panel Behaviour) |
| U-4 | Visual Consistency | No workspace-specific hardcoded padding — all via `var(--ix-space-*)` / `var(--ix-elevation-level-*)` | 16 Brand Governance |
| U-5 | Dark-First | Panel/card balance renders correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |
| U-6 | No Color-Alone | Panel balance is spacing/elevation, not color-alone — status already text+`◆◆◆`+`%` per P02 atomic | 02 §Design, 08 |
| U-7 | Workspace Polish | Panel balance harmonization ensures visual breathing room between dense financial tables and summary cards (12 Part VI §17) | 12 Part VI §17 |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `panelBalance.test.tsx` | Panel `Panel.css` header `var(--ix-space-4)`, body `var(--ix-space-6)`, action bar/footer `var(--ix-space-3)` + `Card` padding + elevation `var(--ix-elevation-level-*)` via `var(--ix-*)` |
| T-2 | `workspaceFrameHarmonization.test.tsx` (or within `panelBalance.test.tsx`) | 7 workspace pages (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `SignalInvestigationPage.tsx`, etc.) `Panel` interior margins uniform — no hardcoded `padding: 10px` outside scale |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **564 tests — 100% pass** (or 564+ with accounting — see §8) — P02 adds panel balance tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Panel balance harmonization is additive — **0 removed / 0 modified** expected for existing tests (138 suites 564 tests from UI-011-P01). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`Panel` with hardcoded `padding: 10px` (outside scale) → test fails via `grep` or `getComputedStyle` token check; `Panel` `raised` without `var(--ix-elevation-level-*)` → fails; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — continue `ui011` evidence directory for UI-011)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **564+ pass** — full log (must show 138 suites/564 baseline + new P02 suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `components/ui/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Panel balance visual proof | Level II | `panelBalance.test.tsx` DOM snapshot of header/body/footer spacing via `var(--ix-space-*)` + elevation `var(--ix-elevation-level-*)` | `docs/evidence/ui011/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P02.md` with 20 sections | `DELIVERY_REPORT_UI-011-P02.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `panelBalance.test.tsx` DOM snapshot of header/body/footer spacing) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **Continue evidence directory `docs/evidence/ui011/` is required for UI-011 (separate from `ui010` 136/556 baseline).**

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

**Expected:** `VITEST_EXIT:0` with **564+ pass** (P02 will be 138→~140 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) `components/ui/` | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| Ad-hoc hex (S-4) `components/ui/` | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ui/ 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
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

DA shall produce `DELIVERY_REPORT_UI-011-P02.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P02 — Panel Balance & Workspace Frame Harmonization |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P02` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §5 P02 + §10 P01 hierarchy |
| 4 | Previous Baseline | UI-011-P01 D-69: 138 suites / 564 tests · 414 backend · hierarchy tokens + spacing rhythm |
| 5 | Implementation Summary | What panel balance was built (header/body/footer spacing, card elevation, workspace frame harmonization) + token consumption |
| 6 | Files Created | List with nature (expected `panelBalance.test.tsx` + maybe workspace page harmonization + evidence logs) |
| 7 | Files Modified | List with nature (likely `Panel.css`/`Card.css`/`InstitutionalWorkspaceShell.css` + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (6 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 138/564 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 138/564 vs current (must be ≥138/564) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Panel balance visual proof (spacing snapshots) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Panel balance complete; micro-interaction in P03” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-011-P03 Micro-Interaction Consistency & Motion Restraint |
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
- Frontend: 138 suites / 564 tests
- Backend: 414 tests

New tests physically added:
- [N tests across panelBalance tests]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [138 or 138+N] suites / [564 or 564+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-69 UI-011-P01 (138/564 + 414)
- Commit: [current HEAD]

Inherited Components: hierarchy tokens (--ix-hierarchy-*, --ix-elevation-level-*), 5-tier tokens, Panel/PanelHeader/PanelActionBar/Collapsible, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 138 suites / 564 frontend + 414 backend (D-69)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P11P01-01 (evidence on main continuity)

New Phase Scope: Panel Balance — header/body/footer spacing + card elevation + workspace frame harmonization (6 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P02, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P02 APPROVED** (version increment per governance, e.g., 8.84.0) |
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
[ BUILD_ORDER_UI-011-P02 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Panel Balance Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P02 Determination ]
         ↓
[ BUILD_ORDER_UI-011-P03 — Micro-Interaction Consistency & Motion Restraint ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Panel `Panel.css` header `var(--ix-space-4)` 16px, body `var(--ix-space-6)` 24px, action bar/footer `var(--ix-space-3)` 12px — uniform across 7 workspaces (`/charts`, `/intelligence`, `/investigate` etc.) | Mandatory | `panelBalance.test.tsx` DOM snapshot |
| AC-2 | Card `Card.css` padding `var(--ix-space-4)` 16px / `var(--ix-space-6)` 24px + elevation `var(--ix-elevation-level-*)` via tokens | Mandatory | `panelBalance.test.tsx` |
| AC-3 | Elevation balance — `Panel`/`Card` `default` Level 2 → `raised` Level 3 via `var(--ix-elevation-level-*)` (`0 1px 2px` → `0 4px 12px`) — consistent shadow hierarchy | Mandatory | `panelBalance.test.tsx` |
| AC-4 | Zero ad-hoc hex literals across `frontend/src/components/ui/` (outside `tokens.css`) — all colors via `var(--ix-*)` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-5 | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-6 | Full platform regression suite passes with 100% success (≥564 frontend, 414 backend) | Mandatory | E-1/E-2 vitest/pytest logs |
| AC-7 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | Mandatory | E-3 tsc/vite logs |
| AC-8 | Delivery Report 20 sections + Governance Declaration per §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**O-011-01 (matrix summary) is now closed in P01 and will be re-verified as harmonized via P02 panelBalance.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P02 implementation only** — no P03–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P02 Design | §5 Phase Specifications — P02 Panel Balance & Workspace Frame Harmonization |
| Preceding Baseline | D-69: 138 suites / 564 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-69 (138/564) preserved as previous baseline |
| §3 Single Active Phase | **P02 = ACTIVE**, P03–P06 = NOT AUTHORIZED, UI-011-P01 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P02 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-69 138/564 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no micro-interaction beyond panel balance |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P03 not authorized until P02 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-69 preserved |
| §24 P02 Controls | Applied — panel balance + spacing rhythm |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P02 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P02**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

