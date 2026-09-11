# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-011-P03`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-70 — UI-011-P02 **APPROVED** (140 suites / 571 tests · 414 backend · exit 0) — Observation O-P11P02-01 (evidence logs documentary tier, continuity)
**Phase:** UI-011-P03 — Micro-Interaction Consistency & Motion Restraint
**Governing Design Plan:** `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (Approved per D-68, §5/P03 — Micro-Interaction Consistency & Motion Restraint)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried UI-008 → UI-009 → UI-010 → UI-011)
**Preceding Milestone:** UI-011-P02 (D-70 APPROVED) — 140 suites / 571 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 140/571 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P03 IMPLEMENTATION** (Only §3.1 scope)
**Cross-Platform Note:** **DA develops on Linux; Operator verifies on Windows** — §8.2 provides **PowerShell (Windows) + Bash (Linux/macOS via Git Bash)** — identical exit codes/logs.

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-011-P03` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-11 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-68 — UI-011 Design Plan APPROVED WITH OBSERVATIONS (O-011-01 — matrix summary, closed) |
| Preceding Milestone | UI-011-P02 (D-70) — 140/571 + 414 |
| Next Milestone | UI-011-P03 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-011) |
| Risk Level | Low (micro-interaction polish — transition timing, hover, reduced-motion, no business logic) |

---

## 2. PHASE OBJECTIVE

Harmonize **micro-interaction consistency and motion restraint** across AXIOM by **standardizing transition timing curves** (`var(--ix-motion-fast)` `120ms`), **hover states**, and **ensuring all motion respects `@media (prefers-reduced-motion: reduce)` → `0ms`** across `Button`, `Select`, `Collapsible`, `Toast`, `Dialog` — per `12` Part VI §17 (Subtle Animations, Stable Transitions).

This phase is **micro-interaction polish, not panel balance (P02), typography (P04), or whole-surface audit (P06).**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Micro-Interaction Transition Harmonization — `Button.css`, `Select.css`, `Collapsible.css`, `Toast.css`, `Dialog.css` + `tokens.css` motion tokens** | Harmonize all interactive transitions to `transition: var(--ix-motion-fast) 120ms` + `cubic-bezier(var(--ix-motion-ease))` (or equivalent `ease` via tokens) — replace any hardcoded `transition: 0.3s` / `transition: all 0.2s` outside tokens with `var(--ix-motion-fast)` |
| 2 | **Hover/Active/Focus-Visible State Consistency** | `Button` `hover` (`filter: brightness(1.05)` or `background: var(--ix-button-hover-bg)`) + `active` (`transform: scale(0.98)` or `filter: brightness(0.95)`) + `focus-visible` (`outline: 2px solid var(--ix-color-focus)`) + `Select`/`Collapsible` hover/active + `Toast` enter/exit `120ms` |
| 3 | **Reduced-Motion Enforcement** | Ensure **every** component with `transition`/`animation` respects `@media (prefers-reduced-motion: reduce) { * { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; } }` via `tokens.css` global override or per-component `prefers-reduced-motion: reduce` → `0ms` |
| 4 | **Test Harness — `interactionPolish.test.tsx` + invariants** | New suite `interactionPolish.test.tsx` (motion `120ms` via `getComputedStyle` `transitionDuration`, hover/active states, `prefers-reduced-motion` query, focus-visible) + security/token invariants |
| 5 | **Token Consumption Enforcement** | All micro-interactions via `var(--ix-*)` (`var(--ix-motion-fast)`, `var(--ix-motion-ease)`, `var(--ix-color-focus)`) — 0 ad-hoc `transition: 0.3s` / `#` hex outside `tokens.css` |
| 6 | **Evidence Package** | Logs committed to `docs/evidence/ui011/` (vitest, tsc/vite, greps, diffs, accessibility) — **both PowerShell + Bash produce same exit codes** |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Optical typography & monospace financial data polish (`0.75rem`/`0.9rem`/`0.85rem`, `tabular-nums` re-verification beyond motion) | **UI-011-P04** scope |
| 2 | Cross-workspace cohesion & visual regression audit | P05 scope |
| 3 | Whole-surface Version 1.0 handover & completion checkpoint | P06 scope |
| 4 | Panel balance & workspace frame harmonization beyond `120ms` transition (header/body/footer padding already harmonized) | **P02 already COMPLETE** — reuse, do not rewrite |
| 5 | Mobile viewports (<768px) | **DEFERRED** per Design Plan §10 — post-1.0 |
| 6 | 5-tier token hierarchy redefinition (`--ix-hierarchy-*`/`--ix-elevation-level-*`) | **P01 already COMPLETE** — reuse |
| 7 | New backend endpoints, migrations, schema changes | No persistence change |
| 8 | WebSocket / real-time push alterations | Not in P03 design |
| 9 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 10 | External LLM integration / Order-trade-execution controls | Constitutionally prohibited — Gate CLOSED |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Micro-Interaction Architecture (Per Design Plan §5 P03)

- **Location (Recommended):** `frontend/src/components/ui/Button.css`, `Select.css`, `Collapsible.css`, `Toast.css`, `Dialog.css` — harmonize `transition` properties; `frontend/src/workstation/design/tokens.css` — `var(--ix-motion-fast): 120ms; var(--ix-motion-ease): cubic-bezier(0.4, 0, 0.2, 1);` (or DA's equivalent ease token) — DA shall declare chosen paths in Delivery Report §6 and use them consistently. Presentation Layer only.
- **Transition Harmonization:** Every interactive `transition` (e.g., `Button: hover background`, `Select: dropdown open`, `Collapsible: height`, `Toast: slide-in`, `Dialog: backdrop/content fade`) **must be** `transition: all var(--ix-motion-fast) var(--ix-motion-ease)` or `transition: background var(--ix-motion-fast), transform var(--ix-motion-fast)` with `120ms` via token, not `transition: all 0.3s` or `transition: 0.2s` hardcoded.
- **Reduced-Motion:** `tokens.css` must include `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; scroll-behavior: auto !important; } }` (or DA's equivalent global `0ms` override) — ensures all motion zeroes under reduced preference.
- **Focus-Visible Consistency:** `Button` `:focus-visible` → `outline: 2px solid var(--ix-color-focus)` `#8CC2FF` + `outline-offset: 2px` (already in P02 atomic, but re-verify for P03 motion polish — no `outline: none` without `:focus-visible` alternative).

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership — `components/ui/` + `workstation/design/tokens.css`); bounded context isolated; no new backend bounded context; no circular deps; no backend coupling; micro-interaction is presentation polish, not business logic.

### 4.3 Interaction Contracts

| Component / Token | Contract |
|-----------|----------|
| `var(--ix-motion-fast)` | `120ms` — all `transition` durations via this token |
| `var(--ix-motion-ease)` | `cubic-bezier(0.4, 0, 0.2, 1)` (or DA's `ease` token) — all `transition-timing-function` via this token |
| `@media (prefers-reduced-motion: reduce)` | `* { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }` |
| `Button` | `transition: background var(--ix-motion-fast) var(--ix-motion-ease), transform var(--ix-motion-fast)` — `hover`/`active` states via `filter` or `background` token, not inline style |
| `Collapsible` | `transition: height var(--ix-motion-fast) var(--ix-motion-ease)` — smooth height via `max-height` or `height` tokenized |
| `Dialog` / `Toast` | Backdrop/content fade + slide-in via `var(--ix-motion-fast)` — respects `prefers-reduced-motion` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in micro-interaction module | Grep `dangerouslySetInnerHTML` in `frontend/src/components/ui/` — 0 matches |
| 4 | No `eval` / `new Function` in module | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/components/ui/` — 0 matches outside `tokens.css` (all colors via `var(--ix-*)`) |
| 7 | No ad-hoc `transition: 0.3s` outside tokens | Grep `transition.*0\.3s` / `transition: all.*0\.2s` in `components/ui/` — 0 matches (all via `var(--ix-motion-fast)`) — or `transition` audit in `interactionPolish.test.tsx` |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/components/ui/ 2>&1` → exit 1 (0 matches outside `tokens.css`) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Motion Consistency | All interactive transitions via `var(--ix-motion-fast)` `120ms` + `var(--ix-motion-ease)` `cubic-bezier(0.4,0,0.2,1)` — `Button` hover/active, `Select` dropdown, `Collapsible` height, `Toast` enter/exit, `Dialog` backdrop fade | `12` Part VI §17 (Subtle Animations, Stable Transitions) |
| U-2 | Reduced-Motion | `@media (prefers-reduced-motion: reduce)` → `transition-duration: 0.01ms !important` + `animation-duration: 0.01ms !important` for all motion components | WCAG 2.3.3 Animation from Interactions, 08 |
| U-3 | Focus Consistency | `Button` `focus-visible` `outline: 2px solid var(--ix-color-focus)` `#8CC2FF` + `outline-offset` — same as `Input`/`Select`/`Collapsible` already in P02 atomic | WCAG 2.4.7 |
| U-4 | Visual Consistency | No `transition: 0.3s` outside tokens; no ad-hoc `ease` outside `var(--ix-motion-ease)` — all via tokens | 16 Brand Governance |
| U-5 | Dark-First | Motion/harmonized components render correctly on `var(--ix-bg-root)` `#0B0E14` and `var(--ix-bg-surface)` `#111822` via tokens | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `interactionPolish.test.tsx` | Motion `var(--ix-motion-fast)` `120ms` via `getComputedStyle` `transitionDuration` on `Button`/`Select`/`Collapsible`/`Toast`/`Dialog` + `var(--ix-motion-ease)` |
| T-2 | `prefersReducedMotion.test.tsx` (or within `interactionPolish.test.tsx`) | `@media (prefers-reduced-motion: reduce)` → `0ms` via computed style with `matchMedia` mock `prefers-reduced-motion: reduce` |
| T-3 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/ad-hoc hex — via `grep_*.log` transcripts |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **571 tests — 100% pass** (or 571+ with accounting — see §8) — P03 adds micro-interaction tests |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Micro-interaction harmonization is additive — **0 removed / 0 modified** expected for existing tests (140 suites 571 tests from UI-011-P02). Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

`Button` with hardcoded `transition: all 0.3s` → test fails via `grep` or `getComputedStyle` token check; `Collapsible` with `transition-duration: 0.5s` outside token → fails; `grep` with no matches → exit 1 (CLEAN) — existing tests already cover.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui011/` on `main` — continue `ui011` evidence directory for UI-011)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **571+ pass** — full log (must show 140 suites/571 baseline + new P03 suites) | `docs/evidence/ui011/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui011/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui011/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui011/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui011/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/ui/` | Level II | 0 | `docs/evidence/ui011/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/ui/` | Level II | 0 | `docs/evidence/ui011/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `components/ui/` (outside `tokens.css`) | Level II | 0 (proves token consumption) | `docs/evidence/ui011/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui011/grep_secrets.log` |
| E-10 | Interaction polish evidence | Level II | `interactionPolish.test.tsx` motion `120ms` + `prefers-reduced-motion` 0ms + `Button` hover/active via `var(--ix-*)` | `docs/evidence/ui011/accessibility.log` or `vitest.log` excerpt |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui011/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-011-P03.md` with 20 sections | `DELIVERY_REPORT_UI-011-P03.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — `interactionPolish.test.tsx` DOM snapshot of `Button` `transitionDuration` `120ms`) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4. **Continue evidence directory `docs/evidence/ui011/` is required for UI-011 (separate from `ui010` 136/556 baseline).**

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

**Expected:** `VITEST_EXIT:0` with **571+ pass** (P03 will be 140→~142 suites), `PYTEST_EXIT:0` **414**, `TSC_EXIT:0` + `BUILD_EXIT:0`.

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

DA shall produce `DELIVERY_REPORT_UI-011-P03.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-011-P03 — Micro-Interaction Consistency & Motion Restraint |
| 2 | Governing Build Order | `BUILD_ORDER_UI-011-P03` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` §5 P03 + §10 P01 hierarchy |
| 4 | Previous Baseline | UI-011-P02 D-70: 140 suites / 571 tests · 414 backend · panel balance |
| 5 | Implementation Summary | What micro-interaction harmonization was built (transition `120ms`, hover/active, motion restraint) + token consumption |
| 6 | Files Created | List with nature (expected `interactionPolish.test.tsx` + maybe component CSS harmonization + evidence logs) |
| 7 | Files Modified | List with nature (likely `Button.css`/`Select.css`/`Collapsible.css`/`Toast.css`/`Dialog.css` + `PROJECT_STATE.md`/`CHANGELOG.md`) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (6 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 140/571 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 140/571 vs current (must be ≥140/571) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo/component proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Interaction polish visual proof (motion snapshots) |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Micro-interaction complete; typography in P04” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-011-P04 Optical Typography & Monospace Financial Data Polish |
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
- Frontend: 140 suites / 571 tests
- Backend: 414 tests

New tests physically added:
- [N tests across interactionPolish tests]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [140 or 140+N] suites / [571 or 571+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-70 UI-011-P02 (140/571 + 414)
- Commit: [current HEAD]

Inherited Components: hierarchy tokens (--ix-hierarchy-*, --ix-elevation-level-*), 5-tier tokens, Panel/PanelHeader/PanelActionBar/Collapsible, DataTable/SortableHeader/Pagination/formatters, Dialog/Skeleton/Toast/ErrorBanner, tokens.css 5-tier, theme.ts, Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 140 suites / 571 frontend + 414 backend (D-70)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P11P02-01 (evidence on main continuity)

New Phase Scope: Micro-Interaction — transition 120ms + hover/active + reduced-motion (6 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P03, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-011-P03 APPROVED** (version increment per governance, e.g., 8.85.0) |
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
[ BUILD_ORDER_UI-011-P03 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Micro-Interaction Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P03 Determination ]
         ↓
[ BUILD_ORDER_UI-011-P04 — Optical Typography & Monospace Financial Data Polish ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Micro-interaction transitions `var(--ix-motion-fast)` `120ms` via `var(--ix-motion-fast)` + `var(--ix-motion-ease)` on `Button`/`Select`/`Collapsible`/`Toast`/`Dialog` | Mandatory | `interactionPolish.test.tsx` DOM snapshot |
| AC-2 | Hover/active/focus-visible states harmonized via tokens (hover `filter: brightness` or `var(--ix-button-hover-bg)` + active `scale` + focus `var(--ix-color-focus)`) | Mandatory | `interactionPolish.test.tsx` |
| AC-3 | Reduced-motion enforcement — `@media (prefers-reduced-motion: reduce)` → `0ms` (`transition-duration: 0.01ms !important`) | Mandatory | CSS + `prefersReducedMotion.test.tsx` or within `interactionPolish.test.tsx` |
| AC-4 | Zero ad-hoc hex literals across `frontend/src/components/ui/` (outside `tokens.css`) — all colors via `var(--ix-*)` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-5 | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Mandatory | E-4/E-5/E-6/E-7 exit 1 |
| AC-6 | Full platform regression suite passes with 100% success (≥571 frontend, 414 backend) | Mandatory | E-1/E-2 vitest/pytest logs |
| AC-7 | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | Mandatory | E-3 tsc/vite logs |
| AC-8 | Delivery Report 20 sections + Governance Declaration per §25 | Mandatory | Document |

All 8 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**O-011-01 (matrix summary) will be re-verified as harmonized via P03 panelBalance.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P03 implementation only** — no P04–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L, D-68 APPROVED WITH OBSERVATIONS) |
| P03 Design | §5 Phase Specifications — P03 Micro-Interaction Consistency & Motion Restraint |
| Preceding Baseline | D-70: 140 suites / 571 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-70 (140/571) preserved as previous baseline |
| §3 Single Active Phase | **P03 = ACTIVE**, P04–P06 = NOT AUTHORIZED, UI-011-P01→P02 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P03 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-70 140/571 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no typography beyond micro-interaction |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P04 not authorized until P03 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui011/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-70 preserved |
| §24 P03 Controls | Applied — micro-interaction + motion restraint |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P03 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-011-P03**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

