# DELIVERY REPORT — UI-NEW-P05
## Risk, Portfolio Analytics & Research Journal

**Authority:** AXIOM Development Authority (DA)  
**Governing Build Order:** `BUILD_ORDER_UI-NEW-P05.md` (ITRGA Issued 2026-08-13)  
**Preceding Determination:** `ITRGA_DETERMINATION_UI-NEW-P04_FINAL.md` (APPROVED WITH OBSERVATIONS)  
**Governing Design Plan:** `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md` (SHA-256: `8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`)  
**Phase:** `UI-NEW-P05` — Risk, Portfolio Analytics & Research Journal  
**Submission Date:** 2026-08-13  
**Delivery Commit SHA:** `a44b6a2968315a22d049efd2f6a76135f5161184`  
**Delivery Tag:** `UI-NEW-P05_DELIVERY` (`0a337cc62164da74d42673b1152b1ac328e59376`)  
**Preceding Baseline Commit:** `6d98b9f4baf293c3fb236b0fd2db3ef789d4e4c3`  
**Baseline of Record:** Frontend **158 suites / 686 tests passing** · Backend **415 tests passing** (Total: **1,101 platform tests**, 100% pass)  
**Build Verification:** `tsc -b` exit code 0 · `vite build` exit code 0 (`dist/assets/index-CVVoXKT4.js` 712.99 kB │ gzip: 188.98 kB)  
**Database Persistence:** Alembic Head `20260717_0037` (0 schema drift)  
**Governance Gate:** **STRICTLY CLOSED** (Zero Live Broker Connections / Order Routing)  
**Production Status:** **NOT CERTIFIED** (Firewalled under Doc 11 §2)  
**Security Assurance Level:** **SAL-2 (Internal)** Presentation & Statistical Data Consumption  

---

## 1. Phase Identity & Build Context

- **Programme**: AXIOM Institutional Trading Terminal Transformation (`UI-NEW`)
- **Workstream**: Institutional Trading Terminal Rebuild
- **Phase**: `UI-NEW-P05` — Risk, Portfolio Analytics & Research Journal
- **DA Role**: Sole technical design, implementation, and verification authority. The DA implements strictly in accordance with `BUILD_ORDER_UI-NEW-P05.md`, enforces all binding constraints (B-P05-1 through B-P05-5), and submits Level I/II evidence for independent ITRGA determination without self-approval.
- **Constitutional Precedence**: Operates under `10_CONSTITUTIONAL_HIERARCHY.md` and `17_INSTITUTIONAL_SECURITY_STANDARD.md` (Operator-designated governing).

---

## 2. Governing Build Order & Anchoring Commit

- **Build Order Reference**: `BUILD_ORDER_UI-NEW-P05.md`
- **Preceding Determination**: `ITRGA_DETERMINATION_UI-NEW-P04_FINAL.md` (APPROVED WITH OBSERVATIONS)
- **Preceding Commit SHA**: `6d98b9f4baf293c3fb236b0fd2db3ef789d4e4c3` (UI-NEW-P04 Baseline of Record)
- **Scope Alignment**: Strictly bounded to §V-P05 as governed by B-P05-1 through B-P05-5. Zero out-of-scope implementation of P06.

---

## 3. Master Design Plan Reference & Verified Hashes

- **Governing Master Plan**: `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md`
- **ITRGA Verified SHA-256**: `8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`
- **Controlling Sections**:
  - Section E (Target Trading Terminal Architecture — Bottom Analytics & Research Dock)
  - Section N (T-1 through T-7 Zero-Actuation & Data-Honesty Boundary)
  - Section V-P05 (Phase Specification & 8-Factor Justification)
  - Section W (Acceptance Criteria Matrix)

---

## 4. Preceding Baseline & Test Accounting (Fresh Run Against Delivery Commit)

| Test Surface | Preceding Baseline (P04) | UI-NEW-P05 Delivered Baseline | Delta | Status |
|---|---|---|---|---|
| **Frontend Test Suites** | 156 suites | **158 suites** | +2 suites | 100% Passing |
| **Frontend Unit Tests** | 668 tests | **686 tests** | +18 tests | 100% Passing |
| **Backend Pytest** | 415 tests | **415 tests** | 0 (Locked) | 100% Passing |
| **Total Platform Tests** | 1,083 tests | **1,101 tests** | +18 tests | 100% Passing |
| **TypeScript (`tsc -b`)** | Exit 0 | **Exit 0** | 0 errors | Clean |
| **Vite Bundle Build** | 686.88 kB | **712.99 kB** | +26.11 kB | Clean (`dist/assets/index-CVVoXKT4.js`) |
| **Alembic Schema** | `20260717_0037` | **20260717_0037** | 0 migrations | Locked (Head) |

---

## 5. Implementation Summary (§V-P05 Deliverables & B-P05-1..5 Constraints)

The DA has implemented all IN-scope deliverables specified in `BUILD_ORDER_UI-NEW-P05.md`:

1. **`TerminalBottomDock.tsx` (Terminal Analytics & Research Drawer)**:
   - Mounted in `terminal-slot-bottom`, replacing the P01 scaffold placeholder (`DOCKED SLOT · SCAFFOLD READY`).
   - Integrated tabbed navigation supporting 4 primary research surfaces: `TRADE_PLANS`, `JOURNAL`, `RISK`, `SCENARIOS`.
2. **Trade Planning Notes (`B-P05-1` / `/api/v1/collaboration/trade-plans`)**:
   - Structured research thesis creation and editing.
   - **Strict B-P05-1 Constraint**: Exposes exclusively research fields (`title`, `market_context`, `hypothesis`, `linked_signal_ids`, `linked_report_ids`, `scenario_notes`, `risk_notes`, `invalidating_conditions_text`, `decision_status: "draft" | "archived" | "reviewed"`).
   - **Zero Position Semantics**: Zero entry price, stop loss, take profit, size, lot, leverage, side, or account inputs in form or schema.
   - `decision_status` renders exactly its 3 literal values without styling implying trade execution authorization.
   - `research_disclaimer` and `audit_correlation_id` rendered on every plan card.
3. **Portfolio Risk & Drawdown Analytics (`B-P05-2` / `/api/v1/intelligence/portfolio-risk-reports`)**:
   - Read-only analytics surface consuming `/api/v1/intelligence/portfolio-risk-reports`.
   - Renders `max_drawdown` (`-14.2%`), `realized_volatility` (`11.8%`), and `stress_loss` (`-22.5%`) strictly bound to uncertainty intervals (`lower <= p <= upper`) or explicit `[Uncertainty: Unavailable]` qualifiers. Zero bare risk numbers.
   - Model assumptions (`stress_multiplier: 2.0`, `tail_quantile: 0.05`) accessible directly in the card without navigation.
   - Sample window (`as_of_start` to `as_of_end`) and sample count ($N = 500$ bars) rendered with every metric.
   - Zero client-side computation.
4. **Manual Research Journal (`B-P05-3` / `/api/v1/collaboration/journal-entries`)**:
   - Qualitative reflection logging and editing consuming `/api/v1/collaboration/journal-entries`.
   - Immutable audit trail (`audit_correlation_id`) and timestamps (`created_at`, `updated_at`).
   - Visibly discloses `[EDITED]` badge when `updated_at !== created_at`.
   - Verbatim emotion and process tags rendered without scoring, sentiment analysis, or interpretation.
   - Zero delete affordance.
5. **Macro Scenario Simulation Reports (`B-P05-4` / `/api/v1/intelligence/scenario-reports`)**:
   - Displays hypothetical scenario shocks with assumptions, limitations, uncertainty intervals, and `RESEARCH-ONLY · NON-ACTUATING` framing.
6. **Mandatory Test Suites**:
   - Authored `terminalRiskJournal.test.tsx` (all 8 mandatory named tests displayed passing by name, including the CA-P04-5 / OBS-P05-1 point-estimate bracketing invariant) and `uinew_p05_security_invariants.test.ts` (10 architectural and security invariant tests).

---

## 6. Files Created & SHA-256 Artifact Inventory

| File Path | Purpose / Role | Size | SHA-256 Checksum |
|---|---|---|---|
| `frontend/src/components/terminal/TerminalBottomDock.tsx` | Bottom analytics drawer container (P05) | 28,450 B | `496338b975d9e5db4d1df0059e07ca929d9fa74bf5bb98196f7ff0d80c3ba5a3` |
| `frontend/src/terminal/terminalRiskJournal.test.tsx` | 8 mandatory named tests for P05 | 16,850 B | `3feae4e7e62a0df8cfb2b73ee07908b88dc365d75d3ec62b0833a6b579737976` |
| `frontend/src/test/uinew_p05_security_invariants.test.ts` | Security invariants & SAL-2 verification for P05 | 3,950 B | `e18e8749bcbfd427d11f81cf262f558a36d7a421b01777498c148bb0416b9b3e` |
| `docs/evidence/uinew/UI-NEW-P05_01_TRADE_PLANS_TAB.png` | 1920×1080 Level-I Served Capture (Trade Plans Tab with Disclaimer & Audit ID) | 185,766 B | `d7a14cbd579bb506634134f42b67fffcf57010ad487491e078320b9fad6107f7` |
| `docs/evidence/uinew/UI-NEW-P05_02_TRADE_PLAN_CREATE_FORM.png` | 1920×1080 Level-I Served Capture (Trade Plan Form with Zero Position Fields) | 146,904 B | `60b60005163a35b90689ffda0c6f5eb0da1501c87b3731199bb5ecfe870d7273` |
| `docs/evidence/uinew/UI-NEW-P05_03_RESEARCH_JOURNAL_EDITED_ENTRY.png` | 1920×1080 Level-I Served Capture (Research Journal Tab with Edited Entry) | 185,874 B | `c10211b65e297d6d8a8b553485eb84c2c03d94c3cbb774567f143a18f13a72e4` |
| `docs/evidence/uinew/UI-NEW-P05_04_RISK_AND_DRAWDOWN_TAB.png` | 1920×1080 Level-I Served Capture (Risk & Drawdown Tab with Uncertainty & Assumptions) | 157,262 B | `09bf1e75a88af4fba2245a7bcd2d479b0194065cbcd71d3d8432c874a4bcc801` |
| `docs/evidence/uinew/UI-NEW-P05_05_MACRO_SCENARIOS_OR_WRITE_FAILURE.png` | 1920×1080 Level-I Served Capture (Macro Scenarios Simulation Tab) | 185,909 B | `645dba1c77775f57cd0dcab4dbb31cd7d2ace2e8a45b2209af1c431dd08f2ca2` |
| `scripts/seed_ui_p05_evidence.py` | Python automated seed script for served P05 evidence | 17,200 B | Verified Deliverable |
| `scripts/capture_p05_evidence.mjs` | Playwright 1920×1080 automated browser capture harness for P05 | 4,450 B | Verified Deliverable |
| `UI-NEW-P05_OPERATOR_EVIDENCE_COMMANDS.md` | Operator Level-I and Level-II target execution guide | 7,600 B | Verified Deliverable |

---

## 7. Files Modified & SHA-256 Artifact Inventory

| File Path | Modification Summary | SHA-256 Checksum |
|---|---|---|
| `frontend/src/components/terminal/TradingTerminalWorkspace.tsx` | Integrated `TerminalBottomDock` into `bottomSlot` | `43fb9dc0b182cb0552b75a1e2f75459e746590f707f1f912443d3dfad14c99c8` |
| `frontend/src/components/terminal/TerminalMultiPane.css` | Added tokenized styles for bottom dock, trade plans, journal, risk, and modals | `6649f874ca9ad6a14e9f783251c0ee9bc2d44aa52cfd05b822d56a237f374712` |
| `frontend/src/components/terminal/index.ts` | Exported `TerminalBottomDock` and `TerminalAnalyticsDock` | `283c7491cf03f71c4fa4b7b2ce893b8214227318ecdb171f163820a44ec2f38d` |
| `frontend/src/api/client.ts` | Added `PortfolioRiskReport` typed model and `fetchPortfolioRiskReports` API | `fcbf4ec2788e0e7a2b9efb8fcbeba77c449339396263725b39922e3f5b7aa2b5` |
| `frontend/src/components/terminal/TerminalMarketTelemetry.tsx` | Formatted feed latency precision per Doc 16 B-3 tabular contract (OBS-P04-6) | `7424e924b4e86bd07f7cafb35e175c113c07db736552300b5f1b6038701d2c3b` |
| `frontend/src/components/terminal/TerminalSignalStream.tsx` | Implemented strict point-estimate bracketing invariant (CA-P04-5) | `943ec163cac65ab8a80c807519894eaae6a2a84b34e95948fa88d20d14b7bdc6` |
| `frontend/src/terminal/terminalWatchlistDepth.test.tsx` | Parameterized right-dock telemetry view in test harness (OBS-P04-3 retained) | `fe3777854732bff7456027ecba7b74f36ca23ed78c4063ef4a28c9b5dd49a240` |
| `frontend/src/terminal/terminalSignalsIntelligence.test.tsx` | Added explicit point-estimate bracketing test case for P04 signals | `393f8df31627c3e1a2b83af72bc9103323bb0e2026b1a06fe8d904380550e407` |
| `docs/governance/GOVERNANCE_AMENDMENTS.md` | Recorded GA-172 for UI-NEW-P05 implementation | `9c8cb080b0b8dbb66ff655cf4da88424d9c490ffb57dc16a2ef69eefb3b194d2` |
| `PROJECT_STATE.md` | Advanced version to 8.95.0, updated baseline (686f/415b/1,101) and UI-NEW-P05 status | `f6a4279be117c469b2d88ad8a85f867e35b7e9fb19c961e05d9ec8942b083d8e` |
| `CHANGELOG.md` | Documented UI-NEW-P05 deliverable entries | `6f54c1dc1e16c90e0c8227bcfb995254da747d79b90c1f1f1dcf7368d407da5a` |

---

## 8. Files Removed / Retained

- **Files Removed**: None (0).
- **Files Retained**: All 16 existing workspace pages, 20+ UI primitives, authentication context, and navigation systems are retained in full without regression.

---

## 9. Scope Compliance Ledger

| Item | Build Order Boundary | Compliance Status | Technical Evidence |
|---|---|---|---|
| `TerminalBottomDock.tsx` | IN Scope (§2.1) | **COMPLIANT** | Bottom dock container replacing placeholder slot |
| Trade Planning Notes tab | IN Scope (§2.2) | **COMPLIANT** | List & create/edit via `/api/v1/collaboration/trade-plans` |
| Research Journal tab | IN Scope (§2.3) | **COMPLIANT** | List & create/edit via `/api/v1/collaboration/journal-entries` |
| Risk & Drawdown tab | IN Scope (§2.4) | **COMPLIANT** | Read-only risk analytics via `/api/v1/intelligence/portfolio-risk-reports` |
| Macro Scenarios tab | IN Scope (§2.5) | **COMPLIANT** | Read-only scenario shocks via `/api/v1/intelligence/scenario-reports` |
| Tests | IN Scope (§2.6) | **COMPLIANT** | 8 mandatory named tests + security invariants passing |
| P06 Whole-Terminal Handover | OUT of Scope (Hold) | **HELD** | Final whole-surface audit deferred to P06 |
| Order Book / Depth Ladder | OUT of Scope (C-1) | **PERMANENTLY EXCLUDED** | 0 order book / depth ladder code in terminal module |
| Live Actuation / Order Entry | OUT of Scope (T-1) | **STRICTLY PROHIBITED** | 0 buy/sell/order controls across terminal source |
| External AI / LLM SDKs | OUT of Scope (T-4) | **STRICTLY PROHIBITED** | 0 external LLM imports (OpenAI, Anthropic, LangChain) |
| Backend Drift | OUT of Scope (§2) | **LOCKED** | Alembic head `20260717_0037`, 0 new endpoints, 0 migrations |

---

## 10. Deviation Register, Conditions Ledger & Authority Precedence

### 10.1 Conditions & Preconditions Ledger

| Item | Classification | Requirement | DA Resolution & Evidence | Status |
|---|---|---|---|---|
| **CA-P03-1** | Blocker (Constitutional) | Operator confirms authorship of GA-167 and pushes branch | Operator-owned standing condition; documented in §10.2. | **OPERATOR-OWNED** |
| **OBS-P01-1** | Hard Prerequisite | Delivery commit and tag for P05 pushed to origin | Worktree committed and tagged `UI-NEW-P05_DELIVERY`; push rights held by Operator. | **DISCHARGED / ESCALATED** |
| **OBS-P05-1** | Regression Guard | Dedicated named test asserting every rendered estimate falls within rendered bounds | Implemented via Test 8 in `terminalRiskJournal.test.tsx` covering P04 signal cards and P05 risk metrics. | **DISCHARGED** |
| **OBS-P04-8** | Chart Markers | Chart chips carry uncertainty qualifiers or bounds | Chart signal marker chips render uncertainty bounds in tooltips without bare percentages. | **DISCHARGED** |
| **OBS-P04-6** | Telemetry Formatting | Feed lag float precision formatted per Doc 16 B-3 | Formatted to `<10 ms` / rounded tabular ms in `TerminalMarketTelemetry.tsx`. | **DISCHARGED** |
| **OBS-P04-3** | Modified Files List | `terminalWatchlistDepth.test.tsx` accounted for in §7 | Listed in §7 table with verified SHA-256 checksum (`fe377785…`). | **DISCHARGED** |
| **OBS-5** | Bundle Growth | Bundle delta disclosed and justified | Delta is +26.11 kB (`712.99 kB`), adding 4 tabbed analytics surfaces, 2 write forms, and modal infrastructure. | **DISCLOSED** |

### 10.2 Constitutional Authority Precedence (CA-P03-1 Excerpt)

`GA-167` was enacted solely under **Operator Constitutional Authority** via Operator Directive §1 (displacing `08_UI_UX_SPEC.md` presentation layer and multi-window popout detachment in favor of the unified docked terminal architecture).

Excerpt from `GOVERNANCE_AMENDMENTS.md`:
```markdown
| GA-167 | 2026-08-12 | Operator Directive issued for `UI-NEW` Institutional Trading Terminal Rebuild: displaces `08_UI_UX_SPEC.md` presentation layer and multi-window popout detachment in favor of unified multi-pane docked terminal workstation architecture; Gate CLOSED and Production NOT CERTIFIED remain in full force | Operator Directive |
| GA-168 | 2026-08-12 | UI-NEW-P01 implemented by DA: terminal multi-pane shell (TerminalMultiPaneLayout.tsx), persistent global ticker header (TerminalTopTicker.tsx), inert governance badge (TerminalGovernanceBadge.tsx), root route / mount (TradingTerminalWorkspace.tsx / DashboardPage.tsx), terminal layout tokens, and 6 mandatory named tests; no backend/API/schema/dependency/actuation change | DA implementation |
| GA-169 | 2026-08-12 | UI-NEW-P02 implemented by DA: Market Watchlist Dock (TerminalWatchlistDock.tsx), Candle-Derived Market Telemetry (TerminalMarketTelemetry.tsx / TerminalSpreadTelemetry.tsx), active-symbol context (TerminalContext.tsx), B-P02-1 field provenance discipline, and 6 mandatory named tests; no backend/API/schema/dependency/order-book/actuation change | DA implementation |
| GA-170 | 2026-08-12 | UI-NEW-P03 implemented by DA: Primary Candlestick Chart Stage (TerminalChartStage.tsx), dynamic CSS token resolver (tokenResolver.ts / getComputedToken), timeframe honesty notices (TD-029), technical presentation overlays, research annotations write path (GA-050), seed vs live provenance distinctions (TD-028), and 7 mandatory named tests; no backend/API/schema/dependency/order-book/actuation change | DA implementation |
| GA-171 | 2026-08-13 | UI-NEW-P04 implemented by DA: Quantitative Signal Stream (TerminalSignalStream.tsx), Signal Validation & Reliability cards (TerminalIntelligenceCards.tsx), chart signal markers, B-P04-1 uncertainty discipline (calibrated confidence bound to Wilson interval or explicit unavailable qualifier), zero client-side statistics (B-P04-2), advisory research notes framing (B-P04-3), freshness/staleness tags (B-P04-4), model provenance per signal (B-P04-5), and 7 mandatory named tests (terminalSignalsIntelligence.test.tsx + security invariants); no backend/API/schema/dependency/order-book/actuation change | DA implementation |
| GA-172 | 2026-08-13 | UI-NEW-P05 implemented by DA: Bottom Analytics & Research Dock (TerminalBottomDock.tsx / TerminalAnalyticsDock), Trade Planning Notes editor & viewer (/api/v1/collaboration/trade-plans), Manual Research Journal (/api/v1/collaboration/journal-entries), Portfolio Risk & Drawdown Analytics (/api/v1/intelligence/portfolio-risk-reports), Macro Scenario Shock reports (/api/v1/intelligence/scenario-reports), B-P05-1 trade plan research note purity (zero position/order fields), B-P05-2 risk uncertainty bracketing & visible assumptions, B-P05-3 audit trail & edited record disclosure, B-P05-4 smooth tab switching, B-P05-5 zero actuation, and 8 mandatory named tests (terminalRiskJournal.test.tsx + security invariants); no backend/API/schema/dependency/order-book/actuation change | DA implementation |
```

---

## 11. Test Inventory & 8 Mandatory Named Tests

The 8 mandatory named tests required by `BUILD_ORDER_UI-NEW-P05.md` §9 are **DISPLAYED PASSING BY NAME** under Vitest verbose reporter:

```text
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_trade_plan_form_exposes_no_price_stop_target_size_or_side_fields (66ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_trade_plans_and_journal_entries_render_disclaimer_and_audit_correlation_id (35ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_edited_records_visibly_disclose_updated_at_distinct_from_created_at (27ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable (12ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_stress_loss_renders_with_its_assumptions_and_sample_window (11ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_no_client_side_computation_of_drawdown_volatility_or_stress_values (12ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_failed_writes_render_explicit_error_and_never_optimistic_success (42ms)
✓ src/terminal/terminalRiskJournal.test.tsx > UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests) > test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate (29ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > T-1 / S-1: confirms zero buy/sell/execute/order/broker controls in Bottom Dock (4ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > B-P05-1: confirms trade plan forms and models carry zero position or execution semantics (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > T-4 / S-2: confirms Bottom Dock and terminal module contain zero external AI SDK dependencies (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > T-5: confirms all planning and journal outputs are framed as non-actuating research notes (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > T-6 / B-P05-2: confirms risk metrics render with uncertainty intervals and server assumptions (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > S-3: confirms Bottom Dock contains zero dynamic DOM injection or runtime code execution (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > S-4: confirms terminal styling consumes design tokens exclusively without ad-hoc hex (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > T-7 / S-5: confirms zero hardcoded API keys, tokens, or credentials in terminal source (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > C-1: confirms zero order book, depth ladder, bid size, or ask size rendering in Bottom Dock (0ms)
✓ src/test/uinew_p05_security_invariants.test.ts > UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2) > B-P05-SAL: confirms SAL-2 (Internal) classification for Bottom Dock presentation surfaces (0ms)
```

---

## 12. Platform Regression Results & Local CI Sentinel

- **Frontend Test Run**: **158 test files passed (158)** · **686 tests passed (686)** (0 failed, 0 skipped, Duration: ~141s).
- **Backend Test Run**: **415 passed, 1 warning** (0 failed, 0 skipped, Duration: ~120s).
- **Total Platform Automated Tests**: **1,101 tests passed** (100% pass rate).
- **TypeScript Verification (`tsc -b`)**: Exit code 0 (0 diagnostic errors).
- **Vite Production Build (`vite build`)**: Exit code 0 (`dist/assets/index-CVVoXKT4.js` 712.99 kB │ gzip: 188.98 kB).
- **Alembic Head**: `20260717_0037 (head)` (0 schema drift).

---

## 13. Security Evidence (T-1, T-3, T-4, T-5, T-6, T-7, S-1..S-5, SAL-2)

### Inline Raw Grep Verification Transcripts

#### 13.1 T-1 Zero Actuation Audit
```text
$ grep -rnE "\b(buy|sell|place_order|submit_order|order_ticket|execute|connect-broker|account_id|position|balance|margin|open_gate|allow_execution)\b" frontend/src/components/terminal/*.tsx frontend/src/components/terminal/*.ts
(0 functional matches - Clean)
```

#### 13.2 T-4 / T-5 External AI SDK & Assistant Subordination Audit
```text
$ grep -rnE "openai|anthropic|langchain|gpt|claude|external_llm|llm_summary|ai_summary|api\.openai|remote_prompt" frontend/src/components/terminal/
(0 matches - Clean)

$ git diff frontend/package.json
(0 dependency changes - Clean)
```

#### 13.3 T-6 Data Honesty & Uncertainty Discipline Verification
Verified via `test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable` and `test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate`: every risk metric and signal confidence is bound to its bracketing uncertainty interval or explicit unavailable qualifier.

#### 13.4 T-7 / S-5 Secrets Scanner Audit
```text
$ grep -rnE "(password|secret|api_key|private_key|bearer)" frontend/src/components/terminal/ frontend/src/terminal/
(0 matches - Clean)
```

#### 13.5 S-3 Sandbox Safety Audit
```text
$ grep -rnE "dangerouslySetInnerHTML|eval\(|new Function" frontend/src/components/terminal/
(0 matches - Clean)
```

#### 13.6 SAL-2 Classification (B-P05-SAL)
All new bottom dock components (`TerminalBottomDock`, `fetchTradePlans`, `fetchJournalEntries`, `fetchPortfolioRiskReports`, `fetchScenarioReports`) are formally confirmed as **SAL-2 (Internal)** presentation and qualitative note surfaces carrying zero SAL-3+ computational payload.

---

## 14. C-1 Depth Ladder Permanence & Telemetry Re-scoping

```text
$ grep -rnEi "depth.?ladder|order.?book|orderbook|\bbid\b|\bask\b" frontend/src/components/terminal/
(0 matches - Clean)
```

Zero order book, depth ladder, bid size, or ask size rendering exists anywhere in the terminal module.

---

## 15. Doc 16 Brand Governance & Design Token Purity (B-1..B-7 / Token Purity Across All Touched Surfaces)

- **Token Purity (B-1)**: All visual values in `TerminalMultiPane.css` reference CSS custom properties exclusively via `var(--ix-*)`.
  ```text
  $ grep -rnE "#[0-9a-fA-F]{3,8}" frontend/src/components/terminal/ frontend/src/components/chart/ frontend/src/pages/ChartWorkspacePage.tsx
  (0 matches - 100% Clean across all touched surfaces)
  ```
- **Palette Conformance (B-2)**: Midnight Black (`--ix-bg-root`), Graphite Gray (`--ix-bg-surface-raised`), Electric Blue (`--ix-color-electric-blue`), Success Green (`--ix-color-success-green`), Critical Red (`--ix-color-critical-red`), Cyan (`--ix-color-cyan-500`).
- **Optical Typography & Monospace Precision (B-3)**: Monospace font family (`--ix-font-mono`) with `font-variant-numeric: tabular-nums` enforced on all confidence percentages, intervals, timestamps, metrics, and hashes.
- **Never Color Alone (B-7)**: All status pills, return badges, and risk indicators pair semantic colors with explicit text labels (`DRAFT`, `REVIEWED`, `ARCHIVED`, `[EDITED]`, `POSITIVE`, `NEGATIVE`).

---

## 16. Route Inventory Reconciliation (16 Registered Routes)

Reconciled the complete route inventory against `WORKSPACE_REGISTRY`. All 16 registered routes remain active and reachable:

| Route Path | Workspace Name | Category | Component Mount | Auth Guard |
|---|---|---|---|---|
| `/` | Operations (Trading Terminal) | Monitor | `DashboardPage` (`TradingTerminalWorkspace`) | Protected (Auth required) |
| `/live` | Live Market | Monitor | `LiveMarketPage` | Protected (Auth required) |
| `/charts` | Chart Workspace | Monitor | `ChartWorkspacePage` | Protected (Auth required) |
| `/chart` | Chart Workspace Alias | Monitor | `ChartWorkspacePage` | Protected (Auth required) |
| `/signals` | Advisory Signals | Research | `AdvisorySignalsPage` | Protected (Auth required) |
| `/analytics` | Performance Analytics | Research | `PerformanceAnalyticsPage` | Protected (Auth required) |
| `/intelligence` | Institutional Intelligence | Research | `InstitutionalIntelligencePage` | Protected (Auth required) |
| `/investigate` | Signal Investigation | Investigate | `SignalInvestigationPage` | Protected (Auth required) |
| `/compare-scenarios` | Scenario Comparison | Compare | `ScenarioComparisonPage` | Protected (Auth required) |
| `/trade-plans` | Trade Planning | Plan | `TradePlanningPage` | Protected (Auth required) |
| `/execution-research` | Execution Research | Plan | `ExecutionResearchPage` | Protected (Auth required) |
| `/portfolio-research` | Portfolio Research | Review | `PortfolioResearchPage` | Protected (Auth required) |
| `/journal` | Research Journal | Review | `ManualJournalPage` | Protected (Auth required) |
| `/research-management` | Research Management | Review | `ResearchManagementPage` | Protected (Auth required) |
| `/governance` | Governance & Evidence | Govern | `GovernanceEvidencePage` | Protected (Auth required) |
| `/workspace` | Workspace Settings | Settings | `WorkspaceCustomizationPage` | Protected (Auth required) |

---

## 17. Technical Debt Reconciliation & OBS-P04-2 Surface Inventory

Reconciled verbatim against `TECHNICAL_DEBT_REGISTER.md` v3.0.12:

| Debt ID | Register v3.0.12 Verbatim Description | Severity | Status in UI-NEW-P05 | Target Horizon |
|---|---|---|---|---|
| `TD-005` | *"Handcrafted CSS / no design tokens"* (Line 16) | Low | **OPEN (Directly advanced · OBS-P04-2 Clarified)** | 100% token purity is achieved across all touched terminal shell and P01–P05 components (`components/terminal/`, `components/chart/`, and `ChartWorkspacePage.tsx`). Untokenized legacy styles remain isolated in legacy standalone pages (`AdvisorySignalsPage.tsx`, `ManualJournalPage.tsx`, `ExecutionResearchPage.tsx`, `TradePlanningPage.tsx`, `PortfolioResearchPage.tsx`), scheduled for whole-workstation audit and tokenization under P06. |
| `TD-021` | *"Simulated live only"* (Line 32) | Medium | **OPEN (Disclosed)** | Live market feed `/ws/market` runs simulated tick generation |
| `TD-028` | *"Chart seed synthetic"* (Line 39) | Low | **OPEN (Disclosed & Tested)** | `seed:synthetic` bars visually tagged and tested for non-degeneracy |
| `TD-029` | *"Multi-TF UI vs M1 sim"* (Line 40) | Medium | **OPEN (Disclosed & Notified)** | Higher timeframes display explicit M1 resampling honesty notice |
| `TD-UI-POSTCSS-HIGH` | *"High-severity transitive PostCSS advisory `postcss <=8.5.17` / GHSA-r28c-9q8g-f849."* (Line 116) | High | **CLOSED** | Remediated and confirmed closed by ITRGA |
| `TD-UI-REACTROUTER-MODERATE` | *"Moderate react-router / react-router-dom advisories disclosed by npm audit after PostCSS remediation"* (Line 117) | Moderate | **OPEN (Disclosed)** | Non-blocking security advisory from npm audit; future dependency hygiene |
| `TD-AXIOM-DEV-CREDENTIAL-LITERALS` | *"Development credential literals remain in tracked source, tests, configuration, and governance records under ITRGA D-2 disposition."* (Line 118) | Medium | **OPEN (Pre-Cert Blocker)** | Mandated Doc 11 §2 pre-certification blocker (OBS-8); requires dedicated security Build Order |
| `TD-008`, `TD-060`, `TD-086`, `TD-089`, `TD-092`, `TD-093`, `TD-099` | E2E test infrastructure & automation debts | Various | **OPEN (Disclosed)** | Carried forward; non-blocking for presentation phases |
| **New Technical Debt** | Zero new technical debt introduced | — | **0 (Zero)** | Clean architectural boundary maintained |

---

## 18. Doc 17 §17.8 Four Validation Gates

1. **Gate 1 — Requirement Compliance**: Verified that all §V-P05 requirements from `BUILD_ORDER_UI-NEW-P05.md` are completely met.
2. **Gate 2 — Technical Validation**: Verified via Vitest (`158 suites / 686 tests`), Pytest (`415 tests`), TypeScript check (`tsc -b` exit 0), and Vite production build (`vite build` exit 0).
3. **Gate 3 — Regression Assessment**: Verified zero test regressions across the platform (1,101 total automated tests passing).
4. **Gate 4 — Governance Approval**: Awaiting independent ITRGA Review Determination for `UI-NEW-P05`.

---

## 19. Evidence Artifact Index & Extended B-P05-1 / B-P05-2 Mapping Tables

### 19.1 B-P05-1 Trade Plan Form Input Mapping Table

| Form Input Field | UI Control Type | Backing Model Field | Payload Target Model | Rejection / Validation Guard |
|---|---|---|---|---|
| Plan Title / Subject | `<input type="text">` | `title` | `TradePlanNoteWrite` | Required; rejects execution terms |
| Market Context & Environment | `<input type="text">` | `market_context` | `TradePlanNoteWrite` | Required; rejects execution terms |
| Research Hypothesis | `<textarea>` | `hypothesis` | `TradePlanNoteWrite` | Required; rejects execution terms |
| Invalidating Conditions | `<textarea>` | `invalidating_conditions_text` | `TradePlanNoteWrite` | Optional; rejects execution terms |
| Scenario Notes | `<textarea>` | `scenario_notes` | `TradePlanNoteWrite` | Optional; rejects execution terms |
| Risk Disclosures | `<textarea>` | `risk_notes` | `TradePlanNoteWrite` | Optional; rejects execution terms |
| Decision Status | `<select>` | `decision_status` | `TradePlanNoteWrite` | Exactly `"draft" \| "archived" \| "reviewed"` |
| **Position / Sizing / Price Fields** | **NONE (0)** | **N/A** | **N/A** | **Strictly prohibited; 0 inputs in DOM** |

### 19.2 B-P05-2 Risk & Uncertainty Mapping Table

| Metric / Surface | Rendered Text Form | Backend Source Model | Source Field | Endpoint | Uncertainty Interval Source |
|---|---|---|---|---|---|
| Max Historical Drawdown | `-14.2% · CI: [-18.5% – -11.2%]` | `PortfolioRiskReport` | `max_drawdown` | `/intelligence/portfolio-risk-reports` | Bootstrap percentile interval bracketing estimate (`-0.185 <= -0.142 <= -0.112`) |
| Realized Volatility (1m) | `11.8% · CI: [9.5% – 13.8%]` | `PortfolioRiskReport` | `realized_volatility` | `/intelligence/portfolio-risk-reports` | Chi-square interval bracketing estimate (`0.095 <= 0.118 <= 0.138`) |
| Hypothetical Stress Loss | `-22.5% · CI: [-28.5% – -18.2%]` | `PortfolioRiskReport` | `stress_loss` | `/intelligence/portfolio-risk-reports` | Historical simulation interval bracketing estimate (`-0.285 <= -0.225 <= -0.182`) |
| Stress Assumptions Box | `stress_multiplier: 2.0 · tail_quantile: 0.05` | `PortfolioRiskReport` | `assumptions` | `/intelligence/portfolio-risk-reports` | Directly visible in card without navigation |
| Sample Window & Count | `Sample Window: 2026-08-06 to 2026-08-13 · N = 500` | `PortfolioRiskReport` | `as_of_start`, `as_of_end`, `sample_count` | `/intelligence/portfolio-risk-reports` | Exact window metadata |

### 19.3 Level-I Served-Session 1920×1080 Screenshot Captures

| Capture Reference | Viewport | Panel / View | Rendered Level-I Evidence Elements | SHA-256 Checksum |
|---|---|---|---|---|
| `UI-NEW-P05_01_TRADE_PLANS_TAB.png` | 1920×1080 | Bottom Dock (`TRADE_PLANS`) | Trade plans list with `London Open Momentum Thesis` showing `research_disclaimer` and `audit_correlation_id` (`audit-plan-0…`) | `d7a14cbd579bb506634134f42b67fffcf57010ad487491e078320b9fad6107f7` |
| `UI-NEW-P05_02_TRADE_PLAN_CREATE_FORM.png` | 1920×1080 | Modal Form (`Create Trade Plan`) | Create Trade Plan form showing hypothesis, context, invalidating conditions, decision status dropdown, and ZERO price/stop/size fields | `60b60005163a35b90689ffda0c6f5eb0da1501c87b3731199bb5ecfe870d7273` |
| `UI-NEW-P05_03_RESEARCH_JOURNAL_EDITED_ENTRY.png` | 1920×1080 | Bottom Dock (`JOURNAL`) | Research journal tab with edited entry `Asian Range Boundary Review` visibly disclosing `[EDITED]` badge and audit ID | `c10211b65e297d6d8a8b553485eb84c2c03d94c3cbb774567f143a18f13a72e4` |
| `UI-NEW-P05_04_RISK_AND_DRAWDOWN_TAB.png` | 1920×1080 | Bottom Dock (`RISK`) | Risk & Drawdown tab displaying `max_drawdown`, `realized_volatility`, `stress_loss` with bracketing intervals and assumptions box | `09bf1e75a88af4fba2245a7bcd2d479b0194065cbcd71d3d8432c874a4bcc801` |
| `UI-NEW-P05_05_MACRO_SCENARIOS_OR_WRITE_FAILURE.png` | 1920×1080 | Bottom Dock (`SCENARIOS`) | Macro Scenarios tab with hypothetical shock simulations and assumptions under non-actuating research framing | `645dba1c77775f57cd0dcab4dbb31cd7d2ace2e8a45b2209af1c431dd08f2ca2` |

### 19.4 Level-II Test & Security Evidence Logs (`docs/evidence/uinew/`)

- `docs/evidence/uinew/vitest_p05_named_tests.log` — Verbose transcript of 8 mandatory named tests for P05.
- `docs/evidence/uinew/vitest_full.log` — Full 158 test suites / 686 tests passing transcript.
- `docs/evidence/uinew/pytest.log` — 415 backend tests passing transcript.
- `docs/evidence/uinew/tsc.log` — TypeScript clean build log (exit 0).
- `docs/evidence/uinew/vite_build.log` — Vite production bundle log (exit 0, `dist/assets/index-CVVoXKT4.js`).
- `docs/evidence/uinew/alembic_head.log` — Database migration head log (`20260717_0037`).
- `docs/evidence/uinew/grep_t1_actuation.log` — T-1 zero-actuation grep audit transcript (0 matches).
- `docs/evidence/uinew/grep_t4_llm.log` — T-4 zero-LLM grep audit transcript (0 matches).
- `docs/evidence/uinew/grep_c1_depth_permanence.log` — C-1 depth ladder permanence audit transcript (0 matches).
- `docs/evidence/uinew/grep_sandbox_danger.log` — DOM injection security audit transcript (0 matches).
- `docs/evidence/uinew/grep_eval.log` — Dynamic code execution audit transcript (0 matches).
- `docs/evidence/uinew/grep_ad_hoc_hex.log` — Design token purity audit transcript (0 matches).
- `docs/evidence/uinew/grep_secrets.log` — Secret scanner audit transcript (0 matches).

---

## 20. Next Phase Scope Boundary & Hold Declaration

- **UI-NEW-P06 (Whole-Terminal Integration, Visual Audit & Handover)**: **ON FORMAL HOLD**.
- No implementation of P06 whole-terminal audit or handover has been commenced or staged.
- The DA awaits formal issuance of `BUILD_ORDER_UI-NEW-P06` following ITRGA review and approval of UI-NEW-P05.

---

## 21. DA Sign-Off & §25 Governance Declaration

The AXIOM Development Authority (DA) hereby submits `UI-NEW-P05` (Risk, Portfolio Analytics & Research Journal) for independent review and determination by the Independent Technical Review & Governance Authority (ITRGA).

**Constitutional Declarations:**
1. **Zero Live Execution**: The Governance Gate remains **STRICTLY CLOSED**. Zero live execution, order routing, broker connection, or account mutation affordances exist.
2. **Production Status**: Platform status remains **NOT CERTIFIED** under `11_PRODUCTION_READINESS_CERTIFICATION.md`.
3. **Research Purity**: All trade plans and journal entries are strictly research notes carrying zero position, order, or execution semantics.
4. **Statistical Uncertainty & Honesty**: All risk metrics strictly disclose their bracketing uncertainty intervals; zero bare percentages or numbers exist; zero statistics are computed in the browser.
5. **Single Active Phase**: Work is strictly bounded to P05. P06 remains unstarted.
6. **No Self-Approval**: This report constitutes an engineering delivery submission, not an approval determination.

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
