# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P01`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-54 — UI-009 Design Plan **APPROVED WITH OBSERVATIONS** (O-009-01, O-009-02)
**Phase:** UI-009-P01 — Design System Foundation & Token Architecture
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §10 Proposed P01)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried forward to UI-009; UI-009 shares same governance lineage — *UI-008 GOVERNANCE CONTROL AMENDMENT* remains the active 27-rule instrument for institutional UI work until superseded)
**Preceding Milestone:** UI-008-P06 (D-53 APPROVED WITH OBSERVATIONS) — 83 suites / 376 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 83/376 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P01 IMPLEMENTATION** (Only §3.1 scope)

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P01` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — APPROVED WITH OBSERVATIONS (O-009-01 palette harmonization, O-009-02 contrast 0.75rem @ 4.5:1) |
| Preceding Milestone | UI-008-P06 (D-53) — 83/376 + 414 |
| Next Milestone | UI-009-P01 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (token codification — presentation primitives only) |

---

## 2. PHASE OBJECTIVE

Codify the **comprehensive 5-tier design token hierarchy** for AXIOM in `tokens.css` + `theme.ts` with **Brand Governance Standard (16) fidelity**, establishing the single authoritative token source that enables atomic component construction (P02) and whole-surface harmonization (P03–P06) without regression.

This phase is **token architecture foundation, not workspace rewrite.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Design Tokens — `tokens.css` (5-Tier Hierarchy)** | Tier 1 Foundation (primitive hex, base grid `--ix-space-base: 4px`, fonts) → Tier 2 Semantic (role tokens `--ix-color-accent`, `--ix-color-surface`, `--ix-color-surface-raised`, `--ix-bg-root`, etc.) → Tier 3 Component (e.g., `--ix-button-primary-bg`, `--ix-card-border`) → Tier 4 Workspace (e.g., `--ix-color-charts`, `--ix-color-governance`) → Tier 5 Runtime Theme Overrides (`.theme-light` — adapted values, not new brand) — all with `--ix-*` prefix |
| 2 | **Theme Contracts — `theme.ts`** | TypeScript token contracts / validation helpers mapping semantic roles to primitive values (e.g., `theme.colors.accent === tokens['--ix-color-blue-600']`) |
| 3 | **Brand Palette Harmonization** | Midnight Black `#0B0E14`, Graphite Gray `#1A1F2C`, Electric Blue `#2563EB`, Success Green `#10B981`, Warning Amber `#F59E0B`, Critical Red `#EF4444` — **harmonize legacy `#070A0F` → `#0B0E14`** per O-009-01 (including grep `grep -R "#070A0F" frontend/src` proof) |
| 4 | **Typography Scale** | Display Titles `1.5rem`, Workspace Titles `1.2rem`, Section Headings `1.0rem`, Panel Headings `0.85rem`, Body `0.9rem`, Metadata/Monospace `0.75rem` — as CSS tokens |
| 5 | **Spacing & Elevation Scales** | 4px base grid `--ix-space-1` 4px → `--ix-space-8` 32px; elevation drop shadows; motion `--ix-motion-fast: 120ms` with `@media (prefers-reduced-motion: reduce)` respected |
| 6 | **Token Audit Test Suite — `tokens.test.ts`** | Comprehensive validation: token completeness (all Tier 1–5 present), brand fidelity (6 colors), contrast ratios (see §5.2) |
| 7 | **Style Safety Proofs** | 0 `dangerouslySetInnerHTML`, 0 `eval`/`new Function`, 0 raw `<script>` in design files |
| 8 | **Regression Suite** | All existing 376 frontend + 414 backend tests continue passing |
| 9 | **Evidence Package Preparation** | Logs committed to `docs/evidence/ui009/` (vitest, tsc/vite, greps, diffs, accessibility spot-check) |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Workspace component rewrites (`Button`, `Card`, `Table`, etc.) | **P02 Atomic Library** scope |
| 2 | Panel frames / workspace harmonization | P03 scope |
| 3 | Data tables / visualization grids | P04 scope |
| 4 | Modals, Command Palette styling, dialogs, toasts, skeletons | P05 scope |
| 5 | New backend endpoints, migrations, schema changes | No persistence change |
| 6 | WebSocket / real-time push | Not in P01 design |
| 7 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 8 | External LLM integration (OpenAI/Anthropic/LangChain etc.) | Constitutionally prohibited — 12 Part I §5 |
| 9 | Order / trade / execution / broker controls | Absolutely prohibited — Gate CLOSED |
| 10 | Dynamic theme customizer / user-editable color picker | **DEFERRED** per §10 — post-v1.0 |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Token Hierarchy (Per Design Plan §15, §10)

```
Tier 1 Foundation:  --ix-color-blue-600: #2563EB; --ix-space-base: 4px; fonts, base grid
       ↓
Tier 2 Semantic:    --ix-color-accent: var(--ix-color-blue-600); --ix-color-surface: #111822; etc.
       ↓
Tier 3 Component:   --ix-button-primary-bg: var(--ix-color-accent); --ix-card-border: var(--ix-border-subtle);
       ↓
Tier 4 Workspace:   --ix-color-charts: #4CC9F0; --ix-color-governance: #10B981;
       ↓
Tier 5 Runtime Theme Override: .theme-light { --ix-bg-root: #F8FAFC; ... }
```

- Bounded context: `frontend/src/workstation/design/` (per Design Plan §12)
- Prefix: **All tokens `--ix-*`** — disorganized/conflicting token names superseded (one-line diff per supersede)
- No runtime string interpolation for theme injection — static CSS custom properties only

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); no new bounded context; no circular deps; no broker logic outside External Integration.

### 4.3 State

No new UI states beyond existing P03-P05 states; P01 adds token completeness + contrast states for `tokens.test.ts` validation.

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in design files | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/design/` — 0 matches |
| 4 | No `eval` / `new Function` in design files | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials in tokens | Whole-repo secrets scan — 0 real secrets (fixtures `REPLACE_ME` acceptable) |
| 6 | Token files = visual only (color/spacing/font) — no JWT secrets / API keys | Manual review + secrets grep |
| 7 | Style-injection defense: tokens as static CSS custom properties, scoped `.ix-*` namespace | Code review — no runtime interpolation |

### Required Security Proofs (Per Design Plan AC-05…AC-07)

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 (CLEAN) |
| S-3 | Sandbox safety | `dangerouslySetInnerHTML` → exit 1 (=0 matches); `eval\(|new Function` → exit 1 |
| S-4 | Palette harmonization grep | `grep -R "#070A0F" frontend/src` → exit 1 (proves legacy hex removed per O-009-01) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | 5-Tier Token Architecture | All Tier 1–5 present with `--ix-*` prefixes in `tokens.css` | 12 Part V §1, Design Plan §11 AC-01 |
| U-2 | Brand Palette Fidelity | `#0B0E14` / `#1A1F2C` / `#2563EB` / `#10B981` / `#F59E0B` / `#EF4444` present (harmonized per O-009-01) | 16 Part VI, AC-02 |
| U-3 | Contrast Compliance | **All** text/background combos >4.5:1; large headings >3:1; **smallest `0.75rem` metadata = >4.5:1** on both `--ix-bg-root` and `--ix-color-surface` (per O-009-02) | 08 §Accessibility, AC-03 |
| U-4 | No Color-Alone Encoding | Statuses/confidence include text label + symbol (e.g., `UncertaintyBadge` pattern) — retain, not supersede | 02 §Design, 08 no-color-alone, AC-04 |
| U-5 | Motion Restraint | `--ix-motion-fast: 120ms` + `@media (prefers-reduced-motion: reduce)` respected | 08 motion, 12 Part VI |
| U-6 | Focus Visibility | `--ix-color-focus: #8CC2FF` explicit focus rings on interactive controls | WCAG 2.1 AA |
| U-7 | Dark-First | Base `#0B0E14`, panels `#1A1F2C`, accent `#2563EB` — institutional workstation | 08 dark-first, 12 Part V |
| A-1…A-4 | Accessibility | Keyboard Tab/Enter/Space/Escape, ARIA, contrast, screen-reader — validated via `tokens.test.ts` + axe spot-check | 08/11 §7 WCAG 2.1 AA |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `tokens.test.ts` — token completeness | All Tier 1–5 tokens present (`--ix-*`) |
| T-2 | `tokens.test.ts` — brand fidelity | 6 brand colors present |
| T-3 | `tokens.test.ts` — contrast ratios | All combos >4.5:1 (and >3:1 large) — **including `0.75rem` on both backgrounds per O-009-02** |
| T-4 | `tokens.test.ts` — no color-alone | Verifies status tokens include text/symbol backup |
| T-5 | Grep-invariant tests (S-1…S-5) | Zero actuation/LLM/sandbox/secrets/legacy hex |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **376 tests — 100% pass** (no new tests beyond T-1…T-5; if DA adds more, must be 376+ and accounted) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Note: Baseline is 83/376 (P06 D-53). P01 is additive token architecture — **0 modified / 0 removed** expected. Category counts are descriptive; baseline delta counts are authoritative per Amendment §8.*

### 7.3 Negative Tests

Palette harmonization negative: `grep "#070A0F"` must be 0 (proves O-009-01 closure).

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **376 pass** (or 376+ with accounting) — full log | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` | Level II | 0 in `frontend/src/workstation/design/` | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | Grep legacy hex — `#070A0F` | Level II | 0 (proves O-009-01) | `docs/evidence/ui009/grep_legacy_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Contrast/accessibility proof | Level II | `tokens.test.ts` contrast checks + axe spot-check | `docs/evidence/ui009/accessibility.log` (or `tokens.test.ts` log excerpt) |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P01.md` with 20 sections | `DELIVERY_REPORT_UI-009-P01.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — snapshots if applicable) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4.

### 8.2 Commands to Generate Evidence (Run on `main`)

```bash
# 1. Frontend + Backend + Build (from repo root)
npm ci
npm run test -- --run 2>&1 | tee docs/evidence/ui009/vitest.log; echo "VITEST_EXIT:$?"
pytest -q 2>&1 | tee docs/evidence/ui009/pytest.log; echo "PYTEST_EXIT:$?"
npx tsc -b 2>&1 | tee docs/evidence/ui009/tsc.log; echo "TSC_EXIT:$?"
npm run build 2>&1 | tee docs/evidence/ui009/vite_build.log; echo "BUILD_EXIT:$?"

# 2. Security greps
grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 | tee docs/evidence/ui009/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"
grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 | tee docs/evidence/ui009/grep_llm.log; echo "LLM_GREP_EXIT:$?"
grep -R -n "dangerouslySetInnerHTML" --include="*.css" --include="*.ts" --include="*.tsx" frontend/src/workstation/design/ 2>&1 | tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"
grep -R -n "eval\(|new Function" --include="*.ts" --include="*.tsx" frontend/src/workstation/design/ 2>&1 | tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"
grep -R -n "#070A0F" --include="*.css" --include="*.ts" --include="*.tsx" frontend/src 2>&1 | tee docs/evidence/ui009/grep_legacy_hex.log; echo "LEGACY_HEX_EXIT:$?"
grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 | tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"

# 3. Documentation diffs
git diff HEAD -- PROJECT_STATE.md 2>&1 | tee docs/evidence/ui009/project_state_diff.log
git diff HEAD -- CHANGELOG.md 2>&1 | tee docs/evidence/ui009/changelog_diff.log
```

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-009-P01.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P01 — Design System Foundation & Token Architecture |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P01` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §10 (Proposed P01) |
| 4 | Previous Baseline | P06 D-53: 83 suites / 376 tests · 414 backend (and inherited 83/376 components/debt) |
| 5 | Implementation Summary | What was codified (5-tier hierarchy, 6 brand colors, typography/spacing/elevation) |
| 6 | Files Created | List with nature (expected `tokens.css` extended, `theme.ts` extended, `tokens.test.ts` NEW, evidence logs) |
| 7 | Files Modified | List with nature |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (9 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 83/376 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 83/376 vs current (must be ≥83/376, 0 removed/modified unless accounted) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo proofs (O-009-01 closure included) |
| 14 | UI/UX Evidence | Contrast >4.5:1 (including `0.75rem`) + focus + motion + axe spot-check |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely none for P01 (or deferred items) |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-009-P02 Atomic Component Library |
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
- Frontend: 83 suites / 376 tests
- Backend: 414 tests

New tests physically added:
- [N tests in tokens.test.ts]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [83 or 83+N] suites / [376 or 376+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-53 UI-008-P06 (83/376 + 414)
- Commit: [current HEAD]

Inherited Components: InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets, tokens.css baseline, theme.ts

Inherited Tests: 83 suites / 376 frontend + 414 backend (D-53)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-009-01, O-009-02 (to be closed in this phase)

New Phase Scope: Design System Foundation — 5-tier token hierarchy (9 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P01, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P01 APPROVED** (version increment per governance, e.g., 8.71.0) |
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
[ BUILD_ORDER_UI-009-P01 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Token Codification & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P01 Determination ]
         ↓
[ BUILD_ORDER_UI-009-P02 — Atomic Component Library ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | 5-tier token hierarchy codified in `tokens.css` with `--ix-*` prefix (Tier 1→5) | Mandatory | Code inspection + E-12 |
| AC-2 | Brand palette fidelity: `#0B0E14` / `#1A1F2C` / `#2563EB` / `#10B981` / `#F59E0B` / `#EF4444` present (O-009-01 harmonized, 0 `#070A0F`) | Mandatory | Code + E-8 legacy hex exit 1 |
| AC-3 | Contrast >4.5:1 body, >3:1 large headings, **0.75rem metadata also >4.5:1** on both backgrounds (O-009-02) | Mandatory | `tokens.test.ts` (T-3) + E-10 accessibility.log |
| AC-4 | No color-alone encoding — statuses include text+symbol backup | Mandatory | `tokens.test.ts` (T-4) |
| AC-5 | Zero actuation grep (whole `frontend/src`) — 0 functional matches | Mandatory | E-4 exit 1 |
| AC-6 | Zero external LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-7 | Style-injection safety: 0 `dangerouslySetInnerHTML` + 0 `eval` in design files | Mandatory | E-6/E-7 exit 1 |
| AC-8 | Legacy `#070A0F` grep 0 (proves O-009-01) | Mandatory | E-8 exit 1 |
| AC-9 | Secrets scan 0 real secrets | Mandatory | E-9 |
| AC-10 | Frontend regression 376 pass (or 376+ with accounting) | Mandatory | E-1 vitest.log |
| AC-11 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-12 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-13 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 13 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**Observations O-009-01 and O-009-02 will be verified as closed via AC-2/AC-3/AC-8 in the P01 evidence package.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P01 implementation only** — no P02–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P01 Design | §10 Proposed P01 (7-part re-baseline) |
| Preceding Baseline | D-53: 83 suites / 376 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried to UI-009) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-53 (83/376) preserved as previous baseline |
| §3 Single Active Phase | **P01 = ACTIVE**, P02–P06 = NOT AUTHORIZED, UI-008 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §10 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-53 83/376 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no workspace rewrites |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P02 not authorized until P01 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-53 preserved |
| §24 P01 Controls | Applied — token audit + contrast + palette harmonization |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P01 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P01**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

