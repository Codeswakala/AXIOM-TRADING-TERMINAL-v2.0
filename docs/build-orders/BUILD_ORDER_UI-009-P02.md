# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-009-P02`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-55 — UI-009-P01 **APPROVED** (84 suites / 381 tests · 414 backend · exit 0) — Observation O-P09P01-01 (continuity tier)
**Phase:** UI-009-P02 — Atomic Component Library
**Governing Design Plan:** `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (Approved per D-54, §5/P02 — Atomic Library) — P02 Phase Title: *Atomic Component Library — Button, Input, Select, Badge, Card, StatusChip, Tooltip, Accordion*
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Carried to UI-009)
**Preceding Milestone:** UI-009-P01 (D-55 APPROVED) — 84 suites / 381 tests · 414 backend · `tsc -b && vite build` exit 0
**Baseline of Record:** Frontend 84/381 · Backend 414 · Build exit 0 · Alembic 20260717_0037
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P02 IMPLEMENTATION** (Only §3.1 scope)

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-009-P02` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Design Plan Determination | D-54 — UI-009 Design Plan APPROVED WITH OBSERVATIONS (O-009-01, O-009-02 — both closed in P01 D-55) |
| Preceding Milestone | UI-009-P01 (D-55) — 84/381 + 414 |
| Next Milestone | UI-009-P02 Delivery Report → ITRGA Determination |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT (carried to UI-009) |
| Risk Level | Low (atomic primitives — reusable, isolated, no business logic) |

---

## 2. PHASE OBJECTIVE

Construct the **reusable atomic component library** for AXIOM in `frontend/src/components/` (or `frontend/src/workstation/design/components/` — DA to declare) using the **5-tier token hierarchy codified in P01** (`--ix-*` in `tokens.css` + `theme.ts` contracts). Primitives must satisfy brand fidelity (16), WCAG 2.1 AA, and style-injection defense (17) and be independently testable for all interaction states.

This phase is **atomic primitives only, not workspace assembly.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Button** | Variants `primary` / `secondary` / `ghost` / `destructive`; states `default` / `hover` / `focus` / `active` / `disabled` / `loading`; sizes `sm`/`md`/`lg`; icon support; `aria-*` |
| 2 | **Input** | Types `text` / `search` / `number`; states `default` / `focus` / `disabled` / `error` / `loading`; label + helper + error message; `aria-invalid`, `aria-describedby` |
| 3 | **Select** | Single-select; states `default` / `open` / `focus` / `disabled` / `error`; keyboard `Tab`/`Enter`/`Space`/`Escape`/`ArrowUp`/`ArrowDown`; `aria-expanded`, `aria-activedescendant`, `listbox`/`option` roles |
| 4 | **Badge** | Variants `neutral` / `info` / `success` / `warning` / `critical` / `accent`; sizes; **never color alone** — text label + semantic token required (08/16) |
| 5 | **Card** | Header / body / footer slots; variants `default` / `raised` / `interactive`; padding via `--ix-space-*` |
| 6 | **StatusChip** | Discrete confidence/status (`HIGH`/`MODERATE`/`LIMITED`/`UNCALIBRATED` pattern) — text + `◆◆◆` + `%` / semantic color — reuse of `UncertaintyBadge` pattern |
| 7 | **Tooltip** | Trigger `hover` / `focus`; placements; `role="tooltip"` + `aria-describedby`; delay; respects `prefers-reduced-motion` |
| 8 | **Accordion** | Sections `collapsed` / `expanded`; `aria-expanded`, `aria-controls`; keyboard `Enter`/`Space`; animated with `--ix-motion-fast:120ms` + reduced-motion fallback |
| 9 | **Comprehensive State Tests** | Per-component suites covering rendering + states + keyboard + ARIA + contrast (via token audit) |
| 10 | **Evidence Package** | Logs committed to `docs/evidence/ui009/` (vitest, tsc/vite, greps, diffs, accessibility) |

**Implementation Note:** All primitives **must consume P01 tokens** (`var(--ix-*)`) — no ad-hoc hex, no hardcoded spacing, no `dangerouslySetInnerHTML`. Use `.ix-*` namespace scoping.

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Workspace panel harmonization / frame wrappers / headers / action bars | **UI-009-P03** scope |
| 2 | Data tables & visualization grids (sortable headers, monospace alignments, uncertainty formatters, pagination) | P04 scope |
| 3 | Modals, Command Palette styling, dialogs, skeleton loaders, toasts, error banners | P05 scope |
| 4 | Whole-surface audit / workstream completion checkpoint | P06 scope |
| 5 | New backend endpoints, migrations, schema changes | No persistence change |
| 6 | WebSocket / real-time push | Not in P02 design |
| 7 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 8 | External LLM integration (OpenAI/Anthropic/LangChain etc.) | Constitutionally prohibited — 12 Part I §5 |
| 9 | Order / trade / execution / broker controls | Absolutely prohibited — Gate CLOSED |
| 10 | Dynamic theme customizer / user-editable color picker | **DEFERRED** per Design Plan §10 — post-v1.0 |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Atomic Library Architecture (Per Design Plan §5 P02)

- **Location:** `frontend/src/components/` **or** `frontend/src/workstation/design/components/` — DA shall declare chosen path in Delivery Report §6 and use it consistently. No component may live outside the declared library path.
- **Token Consumption:** Every visual value (color, spacing, typography, elevation, motion, radius, border) **must reference P01 tokens** (`var(--ix-*)`). No inline hex (`#…` literal outside `tokens.css`), no hardcoded `px` spacing outside `var(--ix-space-*)`, no ad-hoc `transition` duration outside `var(--ix-motion-fast)`.
- **Prefix:** Component class names **`.ix-*`** (e.g., `.ix-button`, `.ix-input`) — consistent with P01 CSS isolation (§13).
- **No Runtime Style Injection:** No `dangerouslySetInnerHTML` for style/theme injection; no `eval`/`new Function`; no raw `<script>`; tokens are static CSS custom properties.

### 4.2 Architecture Compliance (05 v2.0)

Presentation Layer only (05 §13 single ownership); bounded context `frontend/src/components/` (or design sub-path); no new bounded context; no circular deps; no backend coupling.

### 4.3 Interaction Contracts

| Component | Contract |
|-----------|----------|
| Button | `variant` prop + `size` + `disabled`/`loading` + `onClick`; `type="button"` default; `aria-busy` when loading |
| Input | `label` + `id` + `value`/`defaultValue` + `error` + `helperText` + `disabled`; `aria-invalid` + `aria-describedby` linking error/helper |
| Select | `options[]` + `value` + `onChange` + `placeholder` + `disabled`/`error`; `aria-expanded` + `aria-controls` + `role="combobox"`/`listbox`/`option` |
| Badge | `variant` + `label` (required text) + optional `icon`; `aria-label` if icon-only (discouraged) |
| Card | `header`/`footer` slots + `variant` + `padding` via tokens |
| StatusChip | `level` (`HIGH`/`MODERATE`/`LIMITED`/`UNCALIBRATED`) + `value` (e.g., `%`) + `symbol` (`◆◆◆`) |
| Tooltip | `content` + `placement` + `delay` + `trigger` child; `aria-describedby` on trigger |
| Accordion | `items[]` (`title` + `content` + `defaultExpanded`) + `onToggle`; each trigger `aria-expanded` + `aria-controls` |

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | Whole-repo grep `frontend/src` — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | Whole-repo grep `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in atomic library | Grep `dangerouslySetInnerHTML` in `frontend/src/components/` (or chosen path) — 0 matches |
| 4 | No `eval` / `new Function` in library | Grep `eval\(|new Function` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan — 0 real secrets |
| 6 | No ad-hoc hex outside `tokens.css` (style-injection hygiene) | Grep `#[0-9A-Fa-f]{3,6}` in `frontend/src/components/` — 0 matches (all colors via `var(--ix-*)`) — or explicit allowlist with justification |

### Required Security Proofs

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 |
| S-3 | Sandbox safety (design/components) | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Ad-hoc hex hygiene | `grep -R -E "#[0-9A-Fa-f]{3,6}" frontend/src/components/` → exit 1 (0 matches) |
| S-5 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |

---

## 6. UI/UX REQUIREMENTS

| # | Requirement | Specification | Governing Clause |
|---|-------------|---------------|------------------|
| U-1 | Brand Fidelity | All 6 palette colors via tokens (`--ix-color-accent`, `--ix-color-success`, etc.) — no inline hex | 16 Part VI, Design Plan §10 AC-02 |
| U-2 | Contrast | Text/background >4.5:1 (body, input, badge, chip, tooltip); large headings >3:1; **`0.75rem` metadata also >4.5:1** (inherited from P01) | 08 WCAG, P01 AC-03 |
| U-3 | No Color-Alone Encoding | Badge/StatusChip: semantic color + **text label + symbol** required (never color alone) | 02 §Design, 08, AC-04 |
| U-4 | Focus Visibility | Focus rings `var(--ix-color-focus)` `#8CC2FF` on all interactive primitives (Button, Input, Select, Accordion trigger, Tooltip trigger) | WCAG 2.4.7 |
| U-5 | Motion Restraint | Transitions via `var(--ix-motion-fast)` `120ms`; respects `@media (prefers-reduced-motion: reduce)` → `0ms` | 08 motion |
| U-6 | Keyboard Navigation | `Tab`/`Shift+Tab` traverses all primitives; `Enter`/`Space` activates Button/Select/Accordion; `Escape` closes Select/Tooltip; Arrow keys navigate Select options | 08 keyboard |
| U-7 | ARIA | Button `aria-busy` when loading; Input `aria-invalid`/`aria-describedby`; Select `aria-expanded`/`aria-controls`/`aria-activedescendant`; Badge/StatusChip not icon-only; Card not interactive unless `variant=interactive` + `role="button"` + tabIndex; Tooltip `role="tooltip"` + `aria-describedby`; Accordion `aria-expanded`/`aria-controls`/`aria-labelledby` | WCAG / 08 |
| U-8 | Dark-First | Primitives render correctly on `--ix-bg-root` `#0B0E14` + `--ix-bg-surface` `#111822` + `.theme-light` override | 08 dark-first |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | `Button.test.tsx` | Variants (primary/secondary/ghost/destructive) + states (default/hover/focus/active/disabled/loading) + sizes + icon + `aria-busy` |
| T-2 | `Input.test.tsx` | Types + states (default/focus/disabled/error/loading) + label/helper/error + `aria-invalid`/`aria-describedby` |
| T-3 | `Select.test.tsx` | Single-select + states (default/open/focus/disabled/error) + keyboard (Tab/Enter/Space/Escape/Arrow) + `aria-expanded`/`listbox`/`option` |
| T-4 | `Badge.test.tsx` | Variants (neutral/info/success/warning/critical/accent) + text label + not icon-only |
| T-5 | `Card.test.tsx` | Variants (default/raised/interactive) + header/body/footer slots + padding via tokens |
| T-6 | `StatusChip.test.tsx` | Levels (`HIGH`/`MODERATE`/`LIMITED`/`UNCALIBRATED`) + text+`◆◆◆`+% + semantic color |
| T-7 | `Tooltip.test.tsx` | Trigger hover/focus + placements + `role="tooltip"` + `aria-describedby` + delay + reduced-motion |
| T-8 | `Accordion.test.tsx` | Collapsed/expanded + `aria-expanded`/`aria-controls` + keyboard Enter/Space + motion `120ms` |
| T-9 | `tokens` integration | Each primitive consumes `var(--ix-*)` — no ad-hoc hex (grep S-4 proves) |

### 7.2 Regression — Mandatory

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **381 tests — 100% pass** (or 381+ with accounting — see §8) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript + Vite build | `tsc -b` exit 0 **and** `vite build` exit 0 |

*Primitives are additive — **0 removed / 0 modified** expected for existing tests. Category counts descriptive; baseline delta authoritative per Amendment §8.*

### 7.3 Negative Tests

Input `error` → `aria-invalid` true + error message visible; Select `disabled` → not focusable / not openable; Button `disabled` → not clickable + `aria-disabled` semantics; Tooltip `Escape` → closes.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II Committed to `docs/evidence/ui009/` on `main`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **381+ pass** — full log (must show 84 suites/381 baseline + new primitive suites) | `docs/evidence/ui009/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui009/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui009/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — whole `frontend/src` | Level II | 0 functional matches — transcript + exit 1 | `docs/evidence/ui009/grep_actuation.log` |
| E-5 | Grep LLM — whole `frontend/` | Level II | 0 | `docs/evidence/ui009/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` in `components/` | Level II | 0 | `docs/evidence/ui009/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval\|new Function` in `components/` | Level II | 0 | `docs/evidence/ui009/grep_eval.log` |
| E-8 | Grep ad-hoc hex — `#[0-9A-F]{3,6}` in `components/` | Level II | 0 (proves token consumption) | `docs/evidence/ui009/grep_ad_hoc_hex.log` |
| E-9 | Grep secrets scan | Level II | 0 real secrets | `docs/evidence/ui009/grep_secrets.log` |
| E-10 | Accessibility spot-check | Level II | WCAG 2.1 AA — contrast >4.5:1 + focus + ARIA + keyboard (axe or `tokens.test.ts` excerpt + new primitive checks) | `docs/evidence/ui009/accessibility.log` |
| E-11 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` / `CHANGELOG.md` (or explicit NO CHANGE) | `docs/evidence/ui009/project_state_diff.log` |
| E-12 | Delivery Report | Level III | `DELIVERY_REPORT_UI-009-P02.md` with 20 sections | `DELIVERY_REPORT_UI-009-P02.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — snapshots if applicable, e.g., Storybook or DOM snapshots for primitives) > Level II (Automated) > Level III (Documentary). Declarations without logs are EVF-4.

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
grep -R -n "dangerouslySetInnerHTML" --include="*.ts" --include="*.tsx" frontend/src/components/ frontend/src/workstation/design/components/ 2>&1 | tee docs/evidence/ui009/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"
grep -R -n "eval\(|new Function" --include="*.ts" --include="*.tsx" frontend/src/components/ frontend/src/workstation/design/components/ 2>&1 | tee docs/evidence/ui009/grep_eval.log; echo "EVAL_GREP_EXIT:$?"
grep -R -n -E "#[0-9A-Fa-f]{3,6}" --include="*.ts" --include="*.tsx" --include="*.css" frontend/src/components/ frontend/src/workstation/design/components/ 2>&1 | tee docs/evidence/ui009/grep_ad_hoc_hex.log; echo "AD_HOC_HEX_EXIT:$?"
grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 | tee docs/evidence/ui009/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"

# 3. Documentation diffs
git diff HEAD -- PROJECT_STATE.md 2>&1 | tee docs/evidence/ui009/project_state_diff.log
git diff HEAD -- CHANGELOG.md 2>&1 | tee docs/evidence/ui009/changelog_diff.log
```

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-009-P02.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-009-P02 — Atomic Component Library |
| 2 | Governing Build Order | `BUILD_ORDER_UI-009-P02` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` §5 P02 (and §10–§15 token foundation) |
| 4 | Previous Baseline | P01 D-55: 84 suites / 381 tests · 414 backend · tokens.css 5-tier `+` O-009-01/O-009-02 closed |
| 5 | Implementation Summary | What primitives were built (Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion) + token consumption |
| 6 | Files Created | List with nature (expected 8+ component files + test files + evidence logs) |
| 7 | Files Modified | List with nature (likely `PROJECT_STATE.md`/`CHANGELOG.md` + maybe `tokens.css` if extended) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (10 deliverables §3.1) / Out-of-scope (10 exclusions §3.2) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 84/381 baseline → current (0 or +N suites/tests) |
| 12 | Regression Results | Per §10 — previous 84/381 vs current (must be ≥84/381) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo proofs (ad-hoc hex 0) |
| 14 | UI/UX Evidence | Contrast/focus/motion/ARIA + primitive snapshots |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “Atomic primitives complete; workspace assembly in P03” |
| 18 | Evidence Index | Complete list E-1…E-12 |
| 19 | Next Phase Recommendation | UI-009-P03 Workspace Panels & Frame Harmonization |
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
- Frontend: 84 suites / 381 tests
- Backend: 414 tests

New tests physically added:
- [N tests across Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [84 or 84+N] suites / [381 or 381+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- ITRGA: D-55 UI-009-P01 (84/381 + 414)
- Commit: [current HEAD]

Inherited Components: tokens.css 5-tier, theme.ts, InstitutionalWorkspaceShell.tsx, NavigationDock.tsx, all UI-003→UI-008 surfaces, branding assets

Inherited Tests: 84 suites / 381 frontend + 414 backend (D-55)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-P09P01-01 (continuity tier — documentary, to be closed when evidence on main)

New Phase Scope: Atomic Component Library — 8 primitives (10 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P02, DA shall commit (with diff logs):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-009-P02 APPROVED** (version increment per governance, e.g., 8.72.0) |
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
[ BUILD_ORDER_UI-009-P02 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Atomic Component Implementation & Verification ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P02 Determination ]
         ↓
[ BUILD_ORDER_UI-009-P03 — Workspace Panels & Frame Harmonization ] (Next)
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Button renders variants/sizes/states + `aria-busy` when loading | Mandatory | `Button.test.tsx` + E-12 |
| AC-2 | Input renders states + `aria-invalid`/`aria-describedby` linking error/helper | Mandatory | `Input.test.tsx` |
| AC-3 | Select renders states + keyboard Tab/Enter/Space/Escape/Arrow + `aria-expanded`/`listbox`/`option` | Mandatory | `Select.test.tsx` |
| AC-4 | Badge variants + text label (never color alone) | Mandatory | `Badge.test.tsx` |
| AC-5 | Card variants + header/body/footer slots | Mandatory | `Card.test.tsx` |
| AC-6 | StatusChip levels text+`◆◆◆`+% + semantic color | Mandatory | `StatusChip.test.tsx` |
| AC-7 | Tooltip `role="tooltip"` + `aria-describedby` + delay + reduced-motion | Mandatory | `Tooltip.test.tsx` |
| AC-8 | Accordion `aria-expanded`/`aria-controls` + Enter/Space + `120ms` + reduced-motion `0ms` | Mandatory | `Accordion.test.tsx` |
| AC-9 | All 8 primitives consume `var(--ix-*)` — 0 ad-hoc hex in `components/` | Mandatory | E-8 `grep_ad_hoc_hex.log` exit 1 |
| AC-10 | Zero actuation grep (whole `frontend/src`) — 0 | Mandatory | E-4 exit 1 |
| AC-11 | Zero LLM grep (whole `frontend/`) — 0 | Mandatory | E-5 exit 1 |
| AC-12 | 0 `dangerouslySetInnerHTML` + 0 `eval` in `components/` | Mandatory | E-6/E-7 exit 1 |
| AC-13 | Frontend regression 381 pass (or 381+ with accounting) | Mandatory | E-1 vitest.log |
| AC-14 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-15 | `tsc -b` + `vite build` exit 0 | Mandatory | E-3 |
| AC-16 | Delivery Report 20 sections + Governance Declaration §25 | Mandatory | Document |

All 16 criteria are **blocking.** One failure = CORRECT/RESUBMIT.

**Observations O-009-01/O-009-02 will be re-verified as closed via AC-9/AC-10–12 + regression invariance in P02 evidence package. O-P09P01-01 (evidence on `main` continuity) will be closed when `docs/evidence/ui009/` logs are on `main`.**

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P02 implementation only** — no P03–P06 work is authorized.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L, D-54 APPROVED WITH OBSERVATIONS) |
| P02 Design | §5 Phase Breakdown — P02 Atomic Component Library |
| Preceding Baseline | D-55: 84 suites / 381 tests · 414 backend · 05 v2.0 · 16 Brand |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules, carried) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Presentation Layer §13 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewalled |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES (Carried Forward)

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | D-55 (84/381) preserved as previous baseline |
| §3 Single Active Phase | **P02 = ACTIVE**, P03–P06 = NOT AUTHORIZED, UI-009-P01 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §5 P02 |
| §7 API/Architecture Changes | 0 expected — must be documented if any |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | D-55 84/381 as baseline |
| §11 Evidence Hierarchy | Level I/II/III per §8 |
| §12 ITRGA Independence | Maintained — DA implements, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM + ad-hoc hex check |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no workspace/table/modal work |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — P03 not authorized until P02 APPROVED |
| §22 Chat Continuity | Applied — `docs/evidence/ui009/` + diff logs required |
| §23 Continuity Confirmation | Confirmed — D-50→D-55 preserved |
| §24 P02 Controls | Applied — atomic primitives + state tests + token consumption |
| §25 Delivery Declaration | Required per §20 |
| §26 ITRGA Declaration | Included in P02 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-009-P02**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

