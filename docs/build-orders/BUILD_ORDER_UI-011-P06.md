# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P06`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-73 — UI-011-P05 **APPROVED** (146 suites / 595 tests · 414 backend · exit 0) — Observation O-P11P05-01 (evidence logs documentary tier, continuity)
**Phase:** UI-011-P06 — Whole-Surface Version 1.0 Handover & Completion Checkpoint
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §5/P06 — Whole-Surface Version 1.0 Handover & Completion Checkpoint)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-011-P05 (D-73 APPROVED) — 146 suites / 595 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 146/595 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P06 VERIFICATION ONLY** (Only §3.1 scope — no new functional development except verification harness)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P06` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01 — matrix summary, closed) |
| Preceding Milestone | UI-011-P05 (D-73) — 146/595 + 414 |
| Next Milestone | UI-011-P06 Delivery Report → ITRGA Determination → **UI-011 COMPLETE Declaration** (if approved) |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (verification/handover only — no new functional surface except audit harness) |

---

## 2. PHASE OBJECTIVE

Execute the **final whole-surface Version 1.0 handover and completion checkpoint** for `UI-011 — Institutional Refinement & Version 1.0 Presentation`. Perform **whole-surface visual consistency audit** of all P01–P05 refinement surfaces (information hierarchy, panel balance, micro-interaction, typography, cross-workspace cohesion) plus **whole-frontend token consumption audit**, **whole-repository security grep proofs**, **full regression validation**, **documentation synchronization to Version 1.0 presentation status**, and produce the **final handover package** for declaration of **UI-011 COMPLETE**.

This phase is **verification and governance closure, not feature development.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Deliver:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Whole-Surface Visual Consistency Audit** | Audit all 7 workspace surfaces (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/trade-plans`, `/journal`, `/compare-scenarios`) for information hierarchy Levels 1→4, panel balance `var(--ix-space-*)`, micro-interaction `var(--ix-motion-fast)` `120ms`, typography `var(--ix-font-size-*)` + `tabular-nums`, and cross-workspace cohesion — produce `accessibility.log` or `visualAudit.log` whole-surface |
| 2 | **Whole-Frontend Token Consumption Audit** | Whole-frontend scan (`frontend/src` excluding `tokens.css` definition file) proving 0 ad-hoc hex literals (`#[0-9A-Fa-f]{3,6}`) outside `tokens.css` — all colors/spacings/typography via `var(--ix-*)` (extends P01–P05 component-scope proof to whole-frontend) |
| 3 | **Whole-Repository Grep Proofs** | Actuation (`frontend/src`), external LLM (`frontend/`), `dangerouslySetInnerHTML`/`eval` (`frontend/src`), secrets scan — whole-repo, exit-code proof |
| 4 | **Full Regression Suite** | Frontend 146/595 + Backend 414 — captured logs, no test added/removed without accounting (0–2 verification harness tests allowed, must be accounted) |
| 5 | **TypeScript & Vite Build Proof** | `tsc -b` + `vite build` exit 0 — captured logs |
| 6 | **Cross-Workspace Surface Verification (Final)** | Spot-check at least **3 workspaces** (e.g., `/intelligence`, `/charts`, `/governance`) proving hierarchy Levels 1→4 + panel frames + tables + overlays + feedback states + typography + cohesion render via tokens across workspaces — DOM snapshots or integration test evidence |
| 7 | **Whole-Surface Verification Harness — `ui011_p06_wholeSurface.test.tsx` (or `verification.test.tsx`)** | 2–4 tests composing all P01–P06 primitives (hierarchy tokens + panel balance + micro-interaction + typography + cross-workspace cohesion) to prove whole-surface institutional polish still holds |
| 8 | **Branch & Governance Reconciliation (Final)** | Confirm `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L) + `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27) + `16_BRAND_GOVERNANCE_STANDARD.md` fidelity remain on-tree; no divergent `migration` state; `main` contains UI-011 P01→P05 artifacts |
| 9 | **Project-State Final Synchronization** | `PROJECT_STATE.md` final **UI-011 COMPLETE** status (e.g., 8.88.0 `UI-011 — Institutional Refinement & Version 1.0 Presentation COMPLETE`), `CHANGELOG.md`, `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md` — with diff logs (or explicit NO CHANGE) |
| 10 | **Evidence Package (Final)** | `docs/evidence/ui011/` final package — vitest, pytest, tsc/vite, grep logs, accessibility whole-surface, diffs — committed to `main` |
| 11 | **Completion Handover Report** | Delivery Report with 20 sections per Amendment §13 + final **UI-011 COMPLETE** declaration readiness + next workstream recommendation (`11` Production Readiness Certification) |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | New functional components beyond P01–P05 verification harness (0–2 tests) — any other new primitive | P06 is verification only |
| 2 | Redefinition of 5-tier token hierarchy or `theme.ts` contracts | **P01 already COMPLETE** — reuse |
| 3 | Rewrites of panel frames (`Panel`/`PanelHeader`/`PanelActionBar`/`Collapsible`) beyond P06 audit | **P02 already COMPLETE** — reuse |
| 4 | Rewrites of data tables/grids (`DataTable`/`SortableHeader`/`Pagination`/`formatters`) beyond P06 audit | **P04 already COMPLETE** — reuse |
| 5 | Rewrites of modals/overlays (`Dialog`/`Skeleton`/`Toast`/`ErrorBanner`) beyond P06 audit | **P05 already COMPLETE** — reuse (harmonization already in P05) |
| 6 | Rewrites of responsive tokens or panel collapse reflow beyond P06 audit | **UI-010 P02 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P06 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |
| 11 | Mobile <768px companion viewports | **DEFERRED** per Design Plan §10 — post-1.0 |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Verification Boundaries

| Boundary | Requirement |
|----------|-------------|
| Functional surfaces | All P01 hierarchy (`--ix-hierarchy-*`/`--ix-elevation-level-*`) → P02 panel balance (header `var(--ix-space-4)`, body `var(--ix-space-6)`) → P03 micro-interaction `var(--ix-motion-fast)` `120ms` → P04 typography `var(--ix-font-size-*)` + `tabular-nums` → P05 cross-workspace cohesion → P06 whole-surface audit — **read-only verification only**, no new primitives except 0–2 harness tests |
| Token audit | Whole-frontend `frontend/src` excluding `tokens.css` definition file — **not just `components/ui/`** — proves harmonization beyond library (all 7 workspace pages now via tokens) |
| Data | No mutation of persisted data — presentation-only verification |
| Branch | `main` must be single authoritative worktree after P05; `main` already contains UI-009/010 COMPLETE artifacts via prior reconciliation — confirm no divergent state |

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `workstation/design/tokens.css` + `components/ui/` + `InstitutionalWorkspaceShell.tsx`); verification respects layered architecture; no new bounded context; no circular deps; no backend coupling. Whole-surface audit via harness is test, not business logic.

### 4.3 State

No new UI states beyond P01–P05 (hierarchy levels, panel collapsed/expanded, `DataTable` sorted/paginated, `Dialog` open/closed focus trap, `Toast` `polite`/`assertive`, `EmptyState` `role="status"`, typography hierarchy). Verification confirms existing states still render via harness.

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
| 6 | No ad-hoc hex outside `tokens.css` — whole-frontend | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/` (excluding `tokens.css` itself) — 0 matches (all colors/spacings/typography via `var(--ix-*)`) |
| 7 | No new actuation/LLM via overlay `action` Button (Dialog `footer`/`ErrorBanner` `action`) — `Button` must be presentation `onClick` only, not order routing | Code review — `Button` `onClick` in `Dialog`/`ErrorBanner` must not call `placeOrder`/`executeTrade` |

### Required Security Proofs (Whole-Frontend for P06 Completion)

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety — whole `frontend/src/` | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex — **whole `frontend/src`*** | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src --exclude="tokens.css"` → exit 1 (0 matches) — *stricter than P02–P05 component-scope* |
| S-5 | Secrets scan — whole `frontend/` | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

*`*` For S-4 whole-frontend, **exclude `frontend/src/workstation/design/tokens.css` itself** (it is the *definition* of hex primitives — the source of truth). All other files must be 0 ad-hoc hex. Document the exclusion in `grep_ad_hoc_hex.log` header.*

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Whole-Surface Visual Consistency | Hierarchy Levels 1→4 via `var(--ix-hierarchy-*)` + `var(--ix-elevation-level-*)` + spacing `var(--ix-space-*)` 4px grid + panel balance + micro-interaction `120ms` + typography `var(--ix-font-size-*)` + cross-workspace cohesion — all via `var(--ix-*)` — whole-frontend 0 ad-hoc hex | 12 Part VI §17 (Institutional Polish — 8-point criteria) |
| U-2 | Brand Fidelity (Whole-Surface) | All workspaces/primitives via tokens (`--ix-bg-surface-raised`, `--ix-border-subtle`, `--ix-space-*`, `--ix-font-size-*)` — verified via whole-frontend ad-hoc hex 0 (excluding `tokens.css`) | 16 Part VI, Design Plan §10 AC-02 |
| U-3 | Information Hierarchy | Level 1 mission-critical → Level 4 administrative visual priority via `var(--ix-hierarchy-*)` + `var(--ix-elevation-level-*)` — consistent across 7 workspaces | 12 Part V §5 (Information Hierarchy) |
| U-4 | Panel Balance | Header `var(--ix-space-4)` 16px + body `var(--ix-space-6)` 24px consistently applied, elevation via `var(--ix-elevation-level-*)` | 12 Part VI §17 |
| U-5 | Micro-Interaction Consistency | All interactive transitions `var(--ix-motion-fast)` `120ms` + `var(--ix-motion-ease)` — `Button` hover/active, `Collapsible` height, `Toast` slide-in, `Dialog` fade — respect `prefers-reduced-motion` 0ms | 12 Part VI §17 |
| U-6 | Typography | Display `1.5rem` → Metadata `0.75rem` via `var(--ix-font-size-*)` + `tabular-nums` for financial columns | 08 typography |
| U-7 | Cross-Workspace Cohesion | No visual jumps between workspaces, no overlapping panels, no `font-family` shift — `InstitutionalWorkspaceShell` header height consistent | 12 Part VII §13 |
| U-8 | Dark-First + WCAG | Whole-surface contrast >4.5:1 + focus `#8CC2FF` + ARIA + keyboard + `aria-live` + `prefers-contrast` + `prefers-reduced-motion` across whole-surface | WCAG 2.1 AA/AAA + 08 |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `ui011_p06_wholeSurface.test.tsx` (or `verification.test.tsx`) | Whole-surface regression: at least one assertion per P01–P05 deliverable class (hierarchy tokens existence, `Panel` header/body spacing via `var(--ix-space-*)`, `DataTable` `tabular-nums`, `Dialog` `aria-modal` focus trap, `RouteAnnouncer` `aria-live`, panel frames `aria-labelledby`, micro-interaction `120ms`, typography `var(--ix-font-size-*)`, cross-workspace cohesion) — proves harmonization still holds; may be minimal 3–5 tests |
| T-2 | `ui011_p06_security_invariants.test.ts` | S-1 whole-repo actuation + S-2 LLM + S-3 whole-frontend sandbox + S-4 whole-frontend ad-hoc hex (`frontend/src` excluding `tokens.css`) + S-5 secrets — via `grep_*.log` transcripts (or `expect` grep exit 1 in test harness) |

**Note:** P06 is a **verification checkpoint**, not a feature phase. DA may add **0–5** verification-only tests (T-1…T-2) if needed; must account for them per Amendment §8. Zero new functional tests is acceptable if existing 146/595 already cover whole-surface via integration snapshots.

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **595 tests — 100% pass** (or 595+ with accounting — see §8) — P06 verification must show **no regression** from D-73 (P05) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*P06 is additive verification — **0 removed / 0 modified** expected for existing tests (146 suites 595 tests from P05). Category counts descriptive; baseline delta authoritative per Amendment §8.*

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — continue `ui011` directory)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **595+ pass** — full log (must show 146 suites/595 baseline + any new P06 verification suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` **whole `frontend/src`** | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` **whole `frontend/src`** | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | **Grep ad-hoc hex — WHOLE `frontend/src` (excluding `tokens.css`)** | Level II | 0 (proves **whole-surface** token consumption — strictly stronger than P02–P05 component-scope) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Accessibility audit — whole-surface | Level II | WCAG 2.1 AA — hierarchy + panel balance + micro-interaction + typography + cross-workspace cohesion (axe or `crossWorkspaceCohesion.test.tsx`) | `docs/evidence/ui011/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` / `RISK_REGISTER.md` / `TECHNICAL_DEBT_REGISTER.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Branch / governance reconciliation | Level II | `git log --oneline --all --graph` + `git diff main..HEAD` showing `main` contains UI-011 P01→P05 artifacts + `docs/plans/` + `docs/governance/` | `docs/evidence/ui011/branch_reconciliation.log` (optional — already on-tree per P05, but re-verify for COMPLETE) |
| E-13 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P06.md` with 20 sections | `DELIVERY_REPORT_UI-011-P06.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — DOM snapshots for whole-surface spot-checks) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **P06 upgrades S-3/S-4 from component-scope (P02–P05) to whole-frontend scope (excluding `tokens.css` definition file).**

### 8.2 Commands to Generate Evidence — CROSS-PLATFORM (Windows PowerShell vs Linux/macOS Bash)

> **Operator (Windows) vs DA (Linux):** All verification is **platform-independent**. PowerShell commands produce **identical exit codes and log files** as Bash. Run **either** column on your machine; ITRGA will accept either platform's logs. **For reliable cross-platform `grep` on Windows, use *Git Bash* (bundled with Git for Windows) — it runs identical Bash commands as DA's Linux.**

#### 1. Frontend + Backend + Build

| Step | Windows (PowerShell) | Linux / macOS (Bash) |
|------|----------------------|----------------------|
| Install | `npm ci` | `npm ci` |
| Create evidence dir (if needed) | `New-Item -ItemType Directory -Force -Path docs/evidence/ui011` | `mkdir -p docs/evidence/ui011` |
| Frontend tests | `npm run test -- --run 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npm run test -- --run 2>&1 \| tee docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$?"` |
| Alt frontend | `npx vitest run 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$LASTEXITCODE"` | `npx vitest run 2>&1 \| tee docs/evidence/ui011/vitest.log; echo "VITEST_EXIT:$?"` |
| Backend tests | `pytest -q 2>&1 | Tee-Object -FilePath docs/evidence/ui011/pytest.log; echo "PYTEST_EXIT:$LASTEXITCODE"` | `pytest -q 2>&1 \| tee docs/evidence/ui011/pytest.log; echo "PYTEST_EXIT:$?"` |
| TypeScript | `npx tsc -b 2>&1 | Tee-Object -FilePath docs/evidence/ui011/tsc.log; echo "TSC_EXIT:$LASTEXITCODE"` | `npx tsc -b 2>&1 \| tee docs/evidence/ui011/tsc.log; echo "TSC_EXIT:$?"` |
| Vite build | `npm run build 2>&1 | Tee-Object -FilePath docs/evidence/ui011/vite_build.log; echo "BUILD_EXIT:$LASTEXITCODE"` | `npm run build 2>&1 \| tee docs/evidence/ui011/vite_build.log; echo "BUILD_EXIT:$?"` |

**Expected:** `VITEST_EXIT:0` with **595+ pass** (P06 will be 146→~148 suites if +2 verification harness), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

#### 2. Security Greps

| Grep | Windows (PowerShell via Git Bash Recommended) | Linux / macOS (Bash) |
|------|-----------------------------------------------|----------------------|
| Actuation (S-1) whole `frontend/src` | **Git Bash:** `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` | `grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"` |
| LLM (S-2) whole `frontend/` | **Git Bash:** `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` | `grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_llm.log; echo "LLM_GREP_EXIT:$?"` |
| Sandbox `dangerouslySetInnerHTML` (S-3a) **whole `frontend/src`** | **Git Bash:** `grep -R -n "dangerouslySetInnerHTML" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` | `grep -R -n "dangerouslySetInnerHTML" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"` |
| Eval (S-3b) whole `frontend/src` | **Git Bash:** `grep -R -n "eval\(|new Function" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` | `grep -R -n "eval\(|new Function" frontend/src 2>&1 \| tee docs/evidence/ui011/grep_eval.log; echo "EVAL_GREP_EXIT:$?"` |
| **Ad-hoc hex (S-4) WHOLE `frontend/src` excluding `tokens.css`** | **Git Bash:** `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src --exclude="tokens.css" 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` | `grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src --exclude="tokens.css" 2>&1 \| tee docs/evidence/ui011/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"` |
| Secrets (S-5) | **Git Bash:** `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` | `grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 \| tee docs/evidence/ui011/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"` |

**Exit code contract (both platforms, identical):** **exit 1 = CLEAN (0 matches), exit 0 = matches found (BLOCKER unless matches are only in explicit `*test.ts` security assertion fixtures, documented).** For S-4 whole-frontend in P06, **exclude `tokens.css` itself** (it is the *definition* of hex primitives — the source of truth). All other files must be 0 ad-hoc hex. Document the exclusion in `grep_ad_hoc_hex.log` header.

#### 3. Documentation Diffs & Accessibility

| Windows (PowerShell) | Linux / macOS (Bash) |
|----------------------|----------------------|
| `git diff HEAD -- PROJECT_STATE.md 2>&1 | Tee-Object -FilePath docs/evidence/ui011/project_state_diff.log` | `git diff HEAD -- PROJECT_STATE.md 2>&1 \| tee docs/evidence/ui011/project_state_diff.log` |
| `git diff HEAD -- CHANGELOG.md 2>&1 | Tee-Object -FilePath docs/evidence/ui011/changelog_diff.log` | `git diff HEAD -- CHANGELOG.md 2>&1 \| tee docs/evidence/ui011/changelog_diff.log` |
| *(Optional axe)* `npx axe --help 2>&1 | Tee-Object -FilePath docs/evidence/ui011/accessibility.log` | `npx axe --help 2>&1 \| tee docs/evidence/ui011/accessibility.log` |

**All logs must be committed to `docs/evidence/ui011/` on `main`.** ITRGA will accept **either** PowerShell-generated or Bash-generated logs — both deterministic. **Git Bash on Windows gives identical `grep` exit codes as DA's Linux** — strongly recommended.

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-011-P06.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P06 — Whole-Surface Version 1.0 Handover & Completion Checkpoint |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P06` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §5 P06 (and §10 P01 hierarchy) |
| 4 | Previous Baseline | P05 D-73: 146 suites / 595 tests · 414 backend · cross-workspace cohesion |
| 5 | Implementation Summary | What whole-surface verification was performed (whole-frontend token audit, whole-repo greps, WCAG whole-surface audit, cross-workspace spot-checks) — no new functional development beyond 0–1 verification harness |
| 6 | Files Created | List with nature (expected 0–1 verification harness + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe accessibility refinements) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (11 deliverables §3.1) / Out-of-scope (11 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 146/595 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 146/595 vs current (must be ≥146/595) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo proofs (whole-frontend ad-hoc hex 0 excluding `tokens.css`) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + whole-surface WCAG audit + cross-workspace snapshots |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “None — UI-011 verification complete; whole-surface harmonized” or remaining observation |
| 18 | Evidence Index | Complete list E-1…E-13 |
| 19 | Next Phase Recommendation | **UI-011 COMPLETE** declaration (or next workstream UI-011+ / 11 Production Readiness) |
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
- Frontend: 146 suites / 595 tests
- Backend: 414 tests

New tests physically added:
- [N tests in ui011_p06 verification harness — or 0]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [146 or 146+N] suites / [595 or 595+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-73 UI-011-P05 (146/595 + 414)
- Commit: [current HEAD]

Inherited Components: hierarchy tokens (--ix-hierarchy-*, --ix-elevation-level-*), 5-tier tokens, Panel/PanelHeader/PanelActionBar/Collapsible, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 146 suites / 595 frontend + 414 backend (D-73)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P11P05-01 (evidence on main continuity)

New Phase Scope: Whole-Surface Version 1.0 Handover — whole-frontend token audit + whole-repo greps + WCAG whole-surface + cross-workspace spot-checks (11 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P06, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P06 APPROVED** and **UI-011 — Institutional Refinement & Version 1.0 Presentation COMPLETE** (e.g., 8.88.0 `UI-011 COMPLETE`) |
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
[ BUILD_ORDER_UI-011-P06 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Whole-Surface Verification & Evidence Capture ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P06 Determination → UI-011 COMPLETE (if APPROVED) ]
         ↓
[ UI-011 COMPLETE Declaration → Next Workstream UI-011+ or Production Readiness Certification (11) — Separate Governance ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Whole-surface token audit — 0 ad-hoc hex in `frontend/src` **excluding `tokens.css`** (all colors/spacings/typography via `var(--ix-*)`) | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-2 | Whole-repo actuation grep (whole `frontend/src`) — 0 functional | Mandatory | E-4 exit 1 |
| AC-3 | Whole-repo LLM grep (whole `frontend/`) — 0 functional | Mandatory | E-5 exit 1 |
| AC-4 | Sandbox safety — **whole `frontend/src`** 0 `dangerouslySetInnerHTML` + 0 `eval`/`new Function` | Mandatory | E-6/E-7 exit 1 |
| AC-5 | Secrets scan — 0 real secrets | Mandatory | E-9 exit 1 |
| AC-6 | Cross-workspace spot-check — at least 3 workspaces (`/intelligence`, `/charts`, `/governance` or equivalent) prove panel frames + tables + overlays + feedback states render via tokens | Mandatory | Level I DOM snapshots or integration test evidence |
| AC-7 | WCAG 2.1 AA whole-surface audit — contrast >4.5:1 + focus + ARIA + keyboard + `aria-live` `polite`/`assertive` + `prefers-contrast` + `prefers-reduced-motion` across whole-surface | Mandatory | E-10 `accessibility.log` |
| AC-8 | Frontend regression 595 pass (or 595+ with accounting) | Mandatory | E-1 `vitest.log` |
| AC-9 | Backend regression 414 pass | Mandatory | E-2 `pytest.log` |
| AC-10 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-11 | Project-state docs synchronized — `PROJECT_STATE.md` final `UI-011 COMPLETE` + `CHANGELOG.md` + diff logs | Mandatory | E-11 |
| AC-12 | No new functional development beyond 0–1 verification harness — 0 deviations beyond verification | Mandatory | §10 `NO DEVIATIONS` |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking** — one failure = CORRECT/RESUBMIT. Upgrading S-3/S-4 from component-scope (P02–P05) to whole-frontend scope is the key P06 hardening for UI-011 COMPLETE.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P06 verification only** — no new functional development beyond 0–1 verification harness per §3.1.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P06 Design | §5 Phase Specifications — P06 Whole-Surface Version 1.0 Handover & Completion Checkpoint |
| Preceding Baseline | D-73: 146 suites / 595 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-73 (146/595) preserved as previous baseline |
| §3 Single Active Phase | **P06 = ACTIVE**, UI-012+ = NOT YET AUTHORIZED, P01–P05 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P06 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-73 146/595 as baseline |
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
| §21 No Premature Next-Phase | Enforced — UI-011 COMPLETE only after P06 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-73 preserved |
| §24 P06 Controls | Applied — whole-surface harmonization + WCAG audit + token audit |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P06 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P06**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

