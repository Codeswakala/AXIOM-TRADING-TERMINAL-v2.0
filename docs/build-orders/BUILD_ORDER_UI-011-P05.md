# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P05`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-72 — UI-011-P04 **APPROVED** (144 suites / 587 tests · 414 backend · exit 0) — Observation O-P11P04-01 (evidence logs documentary tier, continuity)
**Phase:** UI-011-P05 — Cross-Workspace Cohesion & Visual Regression Audit
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §5/P05 — Cross-Workspace Cohesion & Visual Regression Audit)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-011-P04 (D-72 APPROVED) — 144 suites / 587 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 144/587 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P05 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P05` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01 — matrix summary, closed) |
| Preceding Milestone | UI-011-P04 (D-72) — 144/587 + 414 |
| Next Milestone | UI-011-P05 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (cross-workspace cohesion — visual integration test harness, no business logic) |

---

## 2. PHASE OBJECTIVE

Verify **cross-workspace visual cohesion and integration** for AXIOM by executing **end-to-end multi-workspace spot-checks and integration test harness** across `/intelligence`, `/charts`, `/governance`, and `/investigate` — proving **seamless visual flow without visual jumps, overlapping panels, or font shifts** — per `12` Part VII §13 (UI-011 Charter — *Cross-Workspace Cohesion & Visual Regression Audit*) and `13` Part V (Design System Rollout).

This phase is **cross-workspace cohesion verification, not typography polish (P04) or whole-surface handover (P06).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Cross-Workspace Cohesion Harness — `crossWorkspaceCohesion.test.tsx`** | Integration test suite rendering 4 workspaces (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `GovernanceEvidencePage.tsx`, `SignalInvestigationPage.tsx`) sequentially via `WorkspaceHost` or `MemoryRouter` + asserting visual consistency: `Panel` header/body padding `var(--ix-space-*)`, typography `var(--ix-font-size-*)`, `tabular-nums` on financial columns, no `overflow: hidden` clipping, no `font-family` shift between workspaces |
| 2 | **Visual Regression Guard — `visualCohesion.test.tsx` (or within same harness)** | Harness proving no visual overlap: `Panel` grid `span-12` layout at 1280px, no overlapping panels (`getBoundingClientRect` checks for non-intersecting panel rects where expected separate), no font shift (`getComputedStyle` `fontFamily` consistent across workspaces) |
| 3 | **Token Consumption Enforcement** | All cohesion tests via `var(--ix-*)` — 0 ad-hoc hex / 0 hardcoded `font-family: Arial` outside `tokens.css` |
| 4 | **Evidence Package** | Logs committed to `docs/evidence/ui011/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Whole-surface Version 1.0 handover & completion checkpoint (final audit, documentation sync to Version 1.0 presentation status) | **UI-011-P06** scope |
| 2 | Optical typography re-verification beyond cohesion (scale `1.5rem`→`0.75rem`, `tabular-nums` already in P04) — reuse, do not rewrite | **P04 already COMPLETE** — reuse |
| 3 | Micro-interaction `120ms` transition re-verification beyond cohesion | **P03 already COMPLETE** — reuse |
| 4 | Panel balance re-verification beyond cohesion | **P02 already COMPLETE** — reuse |
| 5 | Mobile viewports (<768px) | **DEFERRED** per Design Plan §10 — post-1.0 |
| 6 | Route re-architecting or navigation dock re-structure | Not in P05 design — cohesion must use existing `WorkspaceHost`/`NavigationDock` |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P05 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Cross-Workspace Cohesion Architecture (Per Design Plan §5 P05)

- **Location (Recommended):** `frontend/src/workstation/design/crossWorkspaceCohesion.test.tsx` — integration harness; DA may alternatively place in `frontend/src/test/crossWorkspaceCohesion.test.tsx` if reusing existing test directory, but **must declare chosen path in Delivery Report §6** and use it consistently. Presentation Layer only. Harness renders `InstitutionalWorkspaceShell.tsx` Regions A–F + 4 workspace pages via `MemoryRouter` (or `WorkspaceHost` directly) with `vitest` + `jsdom`.
- **Cohesion Checks:** For each of the 4 workspaces (`/intelligence`, `/charts`, `/governance`, `/investigate`): (a) `Panel` header `getComputedStyle` `padding` → `var(--ix-space-4)` `16px` (consistent), (b) `Panel` body `padding` `var(--ix-space-6)` `24px` (consistent), (c) financial columns `fontVariantNumeric: tabular-nums` (consistent), (d) no `Panel` rect overlap where panels are side-by-side (compare `getBoundingClientRect` `left`/`right` not intersecting), (e) `fontFamily` consistent (`var(--ix-font-sans)`/`var(--ix-font-mono)`) across workspaces.
- **Visual Regression Guard:** No visual jumps between workspaces — `InstitutionalWorkspaceShell` header `height` consistent across routes; no `font-family` shift between workspaces (`getComputedStyle` `fontFamily` equal across pages); no `overflow: hidden` clipping causing hidden content at 1280/1024 reflow.
- **Token Consumption:** Every visual value (spacing `var(--ix-space-*)`, typography `var(--ix-font-size-*)`, elevation `var(--ix-elevation-level-*)`) **must reference P05 tokens** (`var(--ix-*)`). No inline `padding: 10px` outside `var(--ix-space-*)`.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/design/` + `components/ui/` + `InstitutionalWorkspaceShell`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; cross-workspace cohesion is presentation integration test, not business logic.

### 4.3 Interaction Contracts

| Component / Test | Contract |
|-----------|----------|
| `crossWorkspaceCohesion.test.tsx` | Renders `InstitutionalWorkspaceShell` + `InstitutionalIntelligencePage` + `ChartWorkspacePage` + `GovernanceEvidencePage` + `SignalInvestigationPage` sequentially via `MemoryRouter` — asserts panel padding `var(--ix-space-*)`, typography `var(--ix-font-size-*)`, tabular-nums, no overlap, no font shift |
| `Panel` header/body | `padding: var(--ix-space-4)` (header) + `var(--ix-space-6)` (body) — consistent across workspaces |
| `DataTable` numeric column | `fontVariantNumeric: tabular-nums` via `var(--ix-font-mono)` — consistent across workspaces |
| Workspace shell header heights | `getBoundingClientRect` `height` consistent across routes (±2px tolerance for rounding) |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in cohesion harness | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/design/` — 0 matches |
| 4 | No `eval` / `new Function` in harness | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/workstation/design/` + `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — cohesion harness | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene — cohesion harness | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/workstation/design/ frontend/src/components/ui/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Cross-Workspace Cohesion | No visual jumps between workspaces — `InstitutionalWorkspaceShell` header height consistent ±2px, no `font-family` shift (`var(--ix-font-sans)`/`var(--ix-font-mono)`) across `/intelligence`/`/charts`/`/governance`/`/investigate` | `12` Part VII §13 (UI-011 Charter — Cross-Workspace Cohesion) |
| U-2 | No Overlapping Panels | No `Panel` rect overlap where panels are side-by-side (`getBoundingClientRect` left/right not intersecting) — correct `span-12` grid at 1280px | `12` Part VI §17 (Uniform Panel Behaviour) |
| U-3 | No Font Shift | `fontFamily` consistent across workspaces (`var(--ix-font-sans)` for body, `var(--ix-font-mono)` for numeric) — `getComputedStyle` `fontFamily` equal across pages | `08_UI_UX_SPEC.md` typography |
| U-4 | Token Consumption | All cohesion checks via `var(--ix-*)` — header `var(--ix-space-4)`, body `var(--ix-space-6)`, elevation `var(--ix-elevation-level-*)` | 16 Brand Governance |
| U-5 | Dark-First | Cohesion harness renders correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `crossWorkspaceCohesion.test.tsx` | Rendering + panel padding `var(--ix-space-*)` + `Card` padding + typography `var(--ix-font-size-*)` + tabular-nums across 4 workspaces (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `GovernanceEvidencePage.tsx`, `SignalInvestigationPage.tsx`) + no `overflow: hidden` clipping + no font shift |
| T-2 | Visual regression (within `crossWorkspaceCohesion.test.tsx` or separate) | No overlapping panels (`getBoundingClientRect` non-intersection) + no visual jumps (shell header height consistent ±2px across routes) + no `fontFamily` shift |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **587 tests — 100% pass** (or 587+ with accounting — see §8) — P05 adds cohesion tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Cohesion verification is additive — **0 removed / 0 modified** expected for existing tests (144 suites 587 tests from UI-011-P04). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`crossWorkspaceCohesion` with missing workspace route → test fails (must cover 4 workspaces); `Panel` with hardcoded `padding: 10px` outside scale → fails; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — continue `ui011` evidence directory for UI-011)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **587+ pass** — full log (must show 144 suites/587 baseline + new P05 suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `workstation/design/` | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `workstation/design/` + `components/ui/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Cohesion audit evidence | Level II | `crossWorkspaceCohesion.test.tsx` visual regression + panel padding + typography + no overlap + no font shift | `docs/evidence/ui011/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P05.md` with 20 sections | `DELIVERY_REPORT_UI-011-P05.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `crossWorkspaceCohesion.test.tsx` DOM snapshots of panel padding + typography + no overlap) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **Continue evidence directory `docs/evidence/ui011/` is required for UI-011 (separate from `ui010` 136/556 baseline).**

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

**Expected:** `VITEST_EXIT:0` with **587+ pass** (P05 will be 144→~146 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

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

DA shall produce `DELIVERY_REPORT_UI-011-P05.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P05 — Cross-Workspace Cohesion & Visual Regression Audit |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P05` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §5 P05 + §10 P01 hierarchy |
| 4 | Previous Baseline | UI-011-P04 D-72: 144 suites / 587 tests · 414 backend · typography polish |
| 5 | Implementation Summary | What cross-workspace cohesion was built (integration harness across 4 workspaces + visual regression guard) + token consumption |
| 6 | Files Created | List with nature (expected `crossWorkspaceCohesion.test.tsx` + maybe visual regression harness + evidence logs) |
| 7 | Files Modified | List with nature (likely `InstitutionalWorkspaceShell.tsx` if needed for cohesion, but ideally none beyond harness + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (4 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 144/587 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 144/587 vs current (must be ≥144/587) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Cohesion visual proof (panel padding + typography + no overlap + no font shift) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Cohesion verified across 4 workspaces; whole-surface handover in P06” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-011-P06 Whole-Surface Version 1.0 Handover & Completion Checkpoint |
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
- Frontend: 144 suites / 587 tests
- Backend: 414 tests

New tests physically added:
- [N tests across crossWorkspaceCohesion tests]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [144 or 144+N] suites / [587 or 587+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-72 UI-011-P04 (144/587 + 414)
- Commit: [current HEAD]

Inherited Components: hierarchy tokens (--ix-hierarchy-*, --ix-elevation-level-*), 5-tier tokens, Panel/PanelHeader/PanelActionBar/Collapsible, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 144 suites / 587 frontend + 414 backend (D-72)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P11P04-01 (evidence on main continuity)

New Phase Scope: Cross-Workspace Cohesion — integration harness across 4 workspaces (4 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P05, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P05 APPROVED** (version increment per governance, e.g., 8.87.0) |
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
[ BUILD_ORDER_UI-011-P05 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Cohesion Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P05 Determination ]
         ↓
[ BUILD_ORDER_UI-011-P06 — Whole-Surface Version 1.0 Handover & Completion Checkpoint ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Cross-workspace cohesion harness `crossWorkspaceCohesion.test.tsx` renders 4 workspaces (`InstitutionalIntelligencePage.tsx`, `ChartWorkspacePage.tsx`, `GovernanceEvidencePage.tsx`, `SignalInvestigationPage.tsx`) sequentially via `MemoryRouter` without visual jumps | Mandatory | `crossWorkspaceCohesion.test.tsx` |
| AC-2 | No overlapping panels — `getBoundingClientRect` non-intersection for side-by-side panels + no `font-family` shift (`var(--ix-font-sans)`/`var(--ix-font-mono)`) across workspaces | Mandatory | `crossWorkspaceCohesion.test.tsx` |
| AC-3 | Typography consistency — `var(--ix-font-size-*)` + `var(--ix-font-weight-*)` + `var(--ix-typography-*)` consistent across workspaces | Mandatory | `crossWorkspaceCohesion.test.tsx` |
| AC-4 | Zero ad-hoc hex literals across `frontend/src/workstation/design/` + `frontend/src/components/ui/` (outside `tokens.css`) — all colors via `var(--ix-*)` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-5 | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-6 | Full platform regression suite passes with 100% success (≥587 frontend, 414 backend) | Mandatory | E-1/E-2 vitest/pytest logs |
| AC-7 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | Mandatory | E-3 tsc/vite logs |
| AC-8 | Delivery Report 20 sections + Governance Declaration per §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P05 implementation only** — no P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P05 Design | §5 Phase Specifications — P05 Cross-Workspace Cohesion & Visual Regression Audit |
| Preceding Baseline | D-72: 144 suites / 587 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-72 (144/587) preserved as previous baseline |
| §3 Single Active Phase | **P05 = ACTIVE**, P06 = NOT AUTHORIZED, UI-011-P01→P04 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P05 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-72 144/587 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no whole-surface handover beyond cohesion |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P06 not authorized until P05 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-72 preserved |
| §24 P05 Controls | Applied — cross-workspace cohesion + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P05 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P05**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

