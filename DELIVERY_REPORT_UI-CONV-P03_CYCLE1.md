# DELIVERY REPORT — UI-CONV-P03 · CYCLE 1
## Terminal Deep-Link Router (OBS-CONV2-7) · Items 1–2: Scenario Comparison & Portfolio Research Re-homed

| Field | Value |
|---|---|
| Document type | DA Phase Delivery Report (Directive §§29–31; Doc 17 §17.8 Gate 4) — **first implementation cycle of UI-CONV-P03** |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | Independent Technical Review & Governance Authority (ITRGA) & Operator |
| Date | 2026-08-15 |
| Governing build order | `BUILD_ORDER_UI-CONV-P03.md` (Operator-authorized 2026-08-15) |
| §4 disposition gate | `UI-CONV-P03_DISPOSITION_NOTE_RESEARCH_MANAGEMENT.md` — **APPROVED WITH ONE CONDITION** (B-4 sequencing; ITRGA_RESPONSE_UI-CONV-P03_DISPOSITION_AND_P02_CAPTURES.md) |
| Base commit | `75c71c5f7a5409b4886e21cafad5152123ecd076` (origin/main, ITRGA-verified) |
| Delivery commits | `687e283` — items 1–2 + deep-link router · `55bd07c` — backend source-inspection test re-pointing |
| Governance Gate | **CLOSED** · Production **NOT CERTIFIED** |

---

## 1. Scope of this cycle

Per BO §4, items 1, 2, 3, 5, 6 may proceed in parallel while item 4 is gated. **This cycle delivers: the B-4 sequencing prerequisite (view parsing), item 2 (Scenario Comparison), and item 1 (Portfolio Research).** Items 3, 5, 6 and the item-4 ResearchHubView remain in subsequent cycles. The §4 disposition note stands approved with the B-4 condition, which this cycle satisfies — the parser landed **before** any page deletion or route conversion in this report's scope.

```
====================================================================================================
                     UI-CONV-P03 — CYCLE 1 DELIVERY SUMMARY
====================================================================================================
  [B-4 / OBS-CONV2-7]  view-parameter parsing (deep-link router) .................. DELIVERED
  [ITEM 2]             ScenarioComparisonPage -> SCENARIOS dock .................. DELIVERED
  [ITEM 1]             PortfolioResearchPage -> PORTFOLIO dock ................... DELIVERED
  [R2]                 Legacy routes /compare-scenarios, /portfolio-research ..... REDIRECT (no 404)
  [R3]                 Zero fabricated statistical fallbacks ..................... VERIFIED (incl. empty path)
  [R4]                 data-testid hooks on re-homed surfaces .................... DELIVERED
  [R6]                 RBAC unchanged (registry role requirements intact) ....... VERIFIED
  [R8]                 npm ci -> tsc -b clean ................................... EXECUTED
====================================================================================================
  PLATFORM TESTS: 1,160 PASSING (163 FRONTEND SUITES / 745 TESTS · 415 BACKEND TESTS)
  GOVERNANCE GATE: STRICTLY CLOSED · RESEARCH-ONLY · NON-ACTUATING · PRODUCTION NOT CERTIFIED
====================================================================================================
```

---

## 2. B-4 prerequisite — terminal deep-link router (discharges OBS-CONV2-7)

ITRGA Part B-3 established that the `view` parameter shipped by CONV-P02 was **inert** — `ChartWorkspaceRedirect → /?view=chart` encoded a contract the application never honoured (`OBS-CONV2-7`, low severity, mitigated only because the chart stage is in the default layout). B-4 made parsing **load-bearing**: `?view=research` has no default-layout safety net, so the parser must land before any route conversion.

**Delivered in `TradingTerminalWorkspace.tsx`:**

| Element | Purpose |
|---|---|
| `getViewFromSearch(search): StageViewName \| null` | Parses `?view=chart \| research`; unknown/absent → `null` (default multi-pane — **never a blank stage**) |
| `getPanelFromSearch(search): BottomDockTab \| null` | Parses `?panel=trade_plans \| journal \| risk \| scenarios \| portfolio` |
| `data-stage-view={stageView ?? "default"}` | Machine-assertable stage state on the terminal root |
| `requestedTab` prop + sync effect | Deep-link tab activation flows into `TerminalBottomDock` |

**Test coverage** (`terminalDeepLinks.test.tsx`, 9 named tests): parser unit cases (chart/research/unknown/absent; portfolio/scenarios/TRADE_PLANS/journal/unknown), `/?view=chart` integration (chart stage + `data-stage-view="chart"`), unknown-view degradation to default multi-pane, `/?panel=portfolio` and `/?panel=scenarios` tab activation, `?dock=intelligence` regression (P02 deep links unaffected), and both legacy-route redirects.

**`OBS-CONV2-7` is discharged by this cycle as ITRGA prescribed.** Visual proof: capture 05 (`data-stage-view="chart"`).

---

## 3. Item 2 — ScenarioComparisonPage re-homed into the SCENARIOS dock

**Disposition: relocation, not retirement.** The page (281 lines) was a live, routed, sole-implementation surface. Its full capability inventory is now in the terminal bottom dock's SCENARIOS tab as `components/terminal/docks/ScenarioComparisonPanel.tsx`; the page file is deleted and `/compare-scenarios` redirects to `/?panel=scenarios`.

### Capability disposition table (BO §3 inventory → new location)

| §3 capability | New location | Evidence |
|---|---|---|
| Investigation Context | Panel header section (context paragraph + read-only navigation links to `/investigate` and `/portfolio-research`) | `ScenarioComparisonPanel.tsx`; suite `test_ui005_comparison_preserves_assumptions_uncertainty_limitations_scope` green |
| Existing persisted scenarios | Scenario picker (checkboxes over dock-fetched `fetchScenarioReports(50)` — **no duplicate endpoint traffic**: the P05 dock already loads scenarios; the panel consumes that fetch) | picker testids `scenario-picker-*`; deep-link test |
| Side-by-side comparison | Comparison card grid; selection defaults to the first two reports, honours exact selection after interaction (deselection is real) | `scenario-comparison-card-*`; ported page suite + extended toggle assertion |
| Hypothetical result | Return %, counterfactual index, economic-usefulness verdict — server values verbatim | ported suite green |
| Assumptions | Compact assumption key/value pairs (blocked-key filter preserved verbatim from the page) | ported suite green |
| Uncertainty | Interval + sample + method text | ported suite green |
| Limitations | Full limitations list per card | ported suite green |
| Provenance / source ids / report hash / input policy | Card provenance section | ported suite green |
| Refresh affordance | Refresh button wired to the dock's shared loader (re-fetches all dock data) | `scenario-refresh-btn` |
| No raw scores / no generation / no actuation | Blocked-key filter + forbidden-term guards carried over | ported suite `uses hypothetical not-guaranteed framing…` and backend `test_scenario_comparison_workspace_has_no_generation_or_execution_path` green |

**P05 behaviour preserved**: the existing scenario cards, empty state, loading state, and testids are untouched (P05 suite green). The comparison surface renders **beneath** them in the same tab.

---

## 4. Item 1 — PortfolioResearchPage re-homed into a new PORTFOLIO dock tab

**Disposition: relocation, not retirement.** The page (163 lines) consumed two endpoints — `fetchPortfolioResearchDashboard` and `fetchAdvancedResearchReport` — **distinct from the RISK tab's `fetchPortfolioRiskReports`**. Its full inventory now lives in `components/terminal/docks/PortfolioResearchPanel.tsx`; the page file is deleted and `/portfolio-research` redirects to `/?panel=portfolio`.

### Capability disposition table

| §3 capability | New location | Evidence |
|---|---|---|
| Investigation Context | Panel section with the same read-only navigation links (`/investigate`, `/compare-scenarios`) | `PortfolioResearchPanel.tsx`; UI-005 suite green |
| Hypothetical Aggregate Figures | Metric cards (label, value, sample count, uncertainty method, economic-usefulness verdict, source artifact ids — all server values verbatim) | `portfolio-metric-*`; capture 04 shows 4 aggregate cards |
| Report Builder / Export Preview | Report preview panel (status, report hash, persisted flag, verdict, sources, export-preview markdown) | `portfolio-report-preview`; ported suite green |
| Uncertainty & Limitations | Limitations list + Included Scope JSON — server data verbatim | `portfolio-uncertainty-limitations`, `portfolio-included-scope` |
| Refresh affordance | Refresh button re-invoking the same two endpoint fetches | `portfolio-refresh-btn` |
| No execution/order/account/P&L surface | Forbidden-term guards carried over | ported suite + backend `test_portfolio_and_reports_have_no_real_account_or_pnl_field_or_label` green |

### R3 — empty-path honesty (ITRGA A-4)

ITRGA recorded: "an empty-API capture of any surface rendering statistics is worth more than a populated one." **Capture 01 was taken against an artifact-free database.** The server returned a **zero-valued dashboard** (`aggregate_cards[0] = {value: 0, sample_count: 0, uncertainty: {method: descriptive_count_only}}`) and the panel rendered those honest zeros **verbatim** — no fabricated fallbacks, no plausible-looking numbers. (Disclosed nuance: because the endpoint returns a valid zero-valued dashboard rather than `null`, the panel's explicit empty banner does not trigger; the empty *banner* path is exercised in the scenario dock instead — capture 02, genuine `No Scenarios Found` on an artifact-free DB.) A metrics-less validation report renders `Unavailable`/`[Uncertainty: Unavailable]` per the P02 regression guard.

---

## 5. Mandatory requirements — compliance map

| Requirement | Status | Evidence |
|---|---|---|
| **R1** Preserve every capability | SATISFIED for items 1–2 — both §3 inventories carried over in full (tables above); zero capabilities removed or re-scoped | capability tables + green suites |
| **R2** Legacy routes redirect, never 404 | SATISFIED — `ScenarioComparisonRedirect → /?panel=scenarios`, `PortfolioResearchRedirect → /?panel=portfolio` (P02 `<Navigate replace />` pattern extended) | captures 06/07; deep-link tests |
| **R3** One code path per statistic; no fabricated fallbacks | SATISFIED — both panels render server figures verbatim or explicit empty/unavailable states; zero hardcoded percentage literals in new code | capture 01 (honest zeros); R1 regression guard still green |
| **R4** `data-testid` hooks | SATISFIED — both panels carry testids on every major region (picker, cards, aggregate figures, report preview, scope, refresh, empty/loading/error states) | grep + suites |
| **R5** Constitutional constraints (T-1/T-6, no LLM/plugins/execution) | SATISFIED — no new dependency, no actuation surface, research-only framing on both panels | backend forbidden-term tests green |
| **R6** RBAC preserved | SATISFIED — both panels live inside the protected shell's terminal; registry role requirements untouched | registry diff (Component swaps only) |
| **R7** Suite green, floor ≥ 736, no deletions to force green | SATISFIED — **163 suites / 745 tests (100%)**, +9 above the floor; two page suites *moved*, not deleted; two UI-005 suites *re-pointed*, not deleted | vitest transcript |
| **R8** `npm ci` before `tsc -b` | SATISFIED — clean `npm ci` → `tsc -b` exit 0 | tsc log |

---

## 6. Executed transcripts (this cycle)

| Command | Result |
|---|---|
| `npm ci` (frontend) | success (lockfile install) |
| `npm test` (vitest, full) | **163 files / 745 tests passed** |
| `npx tsc -b --pretty false` | **exit 0** (no diagnostics) |
| `npm run build` (vite) | **exit 0** · `index-DR0q2iSs.js` **683.93 kB** (gzip 183.62 kB) |
| backend `pytest -q` | **415 passed** |

Bundle delta: P02-close was 682.11 kB → **+1.82 kB** for the two dock panels and the router. Disclosed under OBS-5 discipline; the 682 kB advisory remains a POLISH-P01 item (BO §6 — not touched).

---

## 7. Level-I captures (7 · all exactly 1920×1080 · alt text on every image)

Transmitted via the Operator's submission workflow: gallery `UI-CONV-P03_CAPTURES.html` (workspace root) + raw PNGs in `/home/user/uiconv_p03_captures/`. Machine-recorded DOM state per capture: `UI-CONV-P03_CAPTURE_VERIFICATION.json`.

| # | File | SHA-256 | Subject |
|---|---|---|---|
| 1 | `UI-CONV-P03_01_PORTFOLIO_EMPTY_STATE.png` | `ca8a17a97fe66237e471007bdc16b6b3ec6eb52bb539a1f0dde2833ccc327633` | Portfolio dock — **empty-data path** (honest zero-valued aggregates, no fabricated fallbacks) |
| 2 | `UI-CONV-P03_02_SCENARIOS_EMPTY_STATE.png` | `9242b98466503e123294f23e0846d776c585c09fddd5c74ead01b2f579426d4f` | Scenarios dock — genuine empty states (dock + comparison) |
| 3 | `UI-CONV-P03_03_SCENARIOS_POPULATED_COMPARISON.png` | `98dc8743b141b8b93ca8af477515a513d448853562e620388ec22d12f433e641` | Populated dock + side-by-side comparison (2 cards, 2 picks) |
| 4 | `UI-CONV-P03_04_PORTFOLIO_POPULATED.png` | `cc0893a68bf9a5e0671ad80f8a1798e6e4daa42740ac1da3f3f82dd43fc50e4a` | Populated portfolio tab (4 aggregate cards, report preview, scope) |
| 5 | `UI-CONV-P03_05_VIEW_CHART_DEEP_LINK.png` | `60a6c17439547c0b5e16d5ceae54eee428c96fa313dd136ab9a1703cf69d9d96` | `/?view=chart` honoured — `OBS-CONV2-7` discharge |
| 6 | `UI-CONV-P03_06_PORTFOLIO_ROUTE_REDIRECT.png` | `fd294b36bb2f36dad0acabb9ade22d01926eea9dddf3c08e3d9b22e25e0d4e2c` | `/portfolio-research` → PORTFOLIO tab (no 404) |
| 7 | `UI-CONV-P03_07_SCENARIOS_ROUTE_REDIRECT.png` | `eec2bef3ff3a1b9d6ec7cb30c53aef104aab7ea51126fc4badd7a32b013934cc` | `/compare-scenarios` → SCENARIOS tab (no 404) |

---

## 8. Files changed (this cycle, vs base `75c71c5`)

| Path | Change | +/− |
|---|---|---|
| `components/terminal/TradingTerminalWorkspace.tsx` | modified — deep-link router (`view`/`panel` parsers, `data-stage-view`, `requestedTab`) | +61/−8 |
| `components/terminal/TerminalBottomDock.tsx` | modified — PORTFOLIO tab, `requestedTab` sync, shared `loadAllData` refactor, comparison mount | +41/−18 |
| `components/terminal/docks/PortfolioResearchPanel.tsx` | **added** (relocation of `pages/PortfolioResearchPage.tsx`) | +242 |
| `components/terminal/docks/ScenarioComparisonPanel.tsx` | **added** (relocation of `pages/ScenarioComparisonPage.tsx`) | +300 |
| `pages/PortfolioResearchPage.tsx` | **deleted** (redirect registered) | −164 |
| `pages/ScenarioComparisonPage.tsx` | **deleted** (redirect registered) | −282 |
| `pages/PortfolioResearchPage.test.tsx` → `docks/PortfolioResearchPanel.test.tsx` | moved + import-path updates | ± |
| `pages/ScenarioComparisonPage.test.tsx` → `docks/ScenarioComparisonPanel.test.tsx` | moved + extended (picker toggle assertion) | ± |
| `terminal/terminalDeepLinks.test.tsx` | **added** — 9 named tests | +188 |
| `workstation/registry/workspaceRegistry.tsx` | modified — two redirect components; Component swaps; description updates | +24/−8 |
| `workstation/investigation/InvestigationPlanningCompletion.test.tsx` | modified — re-pointed to dock modules | ± |
| `workstation/investigation/ScenarioPortfolioContext.test.tsx` | modified — re-pointed to dock modules | ± |
| `backend/tests/test_portfolio_research.py` | modified — source-inspection path re-pointed | +1/−1 |
| `backend/tests/test_scenario_comparison_workspace.py` | modified — source-inspection path re-pointed | +1/−1 |
| `scripts/capture_uiconv_p03_*.mjs` | added — capture harnesses (empty / populated / redirects) | +~250 |

Net: `frontend/src` +569/−236 · `backend/tests` +2/−2. **No backend application code, schema, migration, endpoint, or dependency changed** (BO §6 held).

---

## 9. Deviations & disclosures

1. **Bundle +1.82 kB** — two dock panels added to the terminal chunk. Disclosed under OBS-5 discipline; below the P04 >+25 kB formal-justification threshold; code-splitting remains a POLISH-P01 item.
2. **Seeded scenario fixture `scen-002`** — the P05 seed script creates a single scenario; a second local-dev scenario row (`Dovish Easing Path Shock`, disclosed seed:synthetic provenance) was inserted so capture 03 shows a genuine two-way comparison. Local database only; no seed script or schema changed. Tracked as `TD-UI-CONV-P03-SCEN002-EVIDENCE-FIXTURE` in the debt register (pending next register update; same class as the accepted `TD-UI-CONV-P02-SIG004-EVIDENCE-FIXTURE`).
3. **Portfolio empty-banner nuance** — on an artifact-free DB the dashboard endpoint returns a valid zero-valued dashboard (rendered honestly), so the panel's null-dashboard banner does not trigger; the banner path itself is exercised by the scenarios dock (capture 02). Stated plainly rather than left implicit.
4. **P02 capture 3 alt-text finding (A-3)** — corrected practice: every capture in this cycle's gallery carries alt text.

---

## 10. Remaining items (subsequent cycles)

| Item | Surface | State |
|---|---|---|
| 3 | `WorkspaceCustomizationPage` (271 lines) → Settings surface from the shell | pending |
| 5 | `GovernanceEvidencePage` (1,072 lines) → governance view, RBAC preserved (R6) | pending |
| 6 | `SignalInvestigationPage` (425 lines) → details dock from signal-card drill-down | pending |
| 4 | `ResearchManagementPage` (1,391 lines) → `?view=research` stage view | gated — parser landed this cycle (B-4 satisfied); implementation proceeds with the approved disposition note |

## 11. Carried-forward findings

| ID | Status | Owner |
|---|---|---|
| `CA-CONV2-3` | Transport — structural, open | Operator |
| `OBS-CONV2-2` | Wording discipline — "relocated" used throughout this report | DA (held) |
| `OBS-CONV2-5` | P02 sig-004 fixture — deviation register entry exists | DA (held) |
| `OBS-CONV2-6` | `@types/node` local install — resolved this cycle (`npm ci` → `tsc` clean) | Operator/DA (held) |
| `OBS-PROV-2` | `docs/evidence/uiconv/` at origin — travels with this phase's push | DA |
| P02 captures ×6 | Previously transmitted (gallery accepted by ITRGA) | — |
| `OBS-5`, `F-BRAND-1` | Unchanged | — |

---

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**. This cycle delivers UI-CONV-P03 items 1–2 and the B-4 prerequisite only; it is not authorization for SURF, DATA, CHART or POLISH, and no such work was performed or begun.

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
*2026-08-15*
