# ITRGA REVIEW — UI-CONV-P03 · CYCLE 1 (Re-review on new baseline)

**Reviewing body:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Repository:** `https://github.com/Codeswakala/AXIOM-TRADING-TERMINAL-v1.0.git` — **new clean baseline**
**Baseline of record:** `34f4c62dbef11e685de965415b4b8ab697cef487` · 2026-08-15 20:36:13 +0300 · *"AXIOM Trading Terminal - clean development baseline"*
**Repository shape:** 1 commit · 1 branch (`main`) · 0 tags · 1,475 tracked files · 20 MB
**Supersedes:** the BLOCKED determination on Cycle 1 (transport). **That blocker is resolved — the code is now present and verifiable.**

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**Cycle 1 is verified in source. `OBS-CONV2-7` is DISCHARGED.** Two observations are recorded, one of which repeats a pattern this authority closed in CONV-P02 and must not be allowed to recur.

**Note on repository identity:** this is a *new* repository with no shared history with `AXIOM-TRADING-PLATFORM-v1.0`. SHAs `75c71c5`, `04ded6b`, `5ef6c4e` and the eight delivery tags do not exist here. All prior determinations remain valid as findings-of-record; their commit references are historical only. **`34f4c62` is the sole baseline going forward.**

---

## 2. `OBS-CONV2-7` — DISCHARGED

The finding was that `?view=` was never parsed, making CONV-P02's `ChartWorkspaceRedirect → /?view=chart` inert. Verified corrected:

```
TradingTerminalWorkspace.tsx:56   export function getViewFromSearch(search): StageViewName | null
                            :60   const view = params.get("view")?.toLowerCase();
                            :70   export function getPanelFromSearch(search): BottomDockTab | null
                            :95   const [stageView] = useState(() => getViewFromSearch(searchStr));
                            :103  setRequestedBottomTab(getPanelFromSearch(searchStr));
                            :155  data-stage-view={stageView ?? "default"}
```

The `?? "default"` fallback confirms the reported degradation contract: an unknown or absent view yields the default multi-pane, never a blank stage.

**Test coverage verified — 9 named tests** in `frontend/src/terminal/terminalDeepLinks.test.tsx`, including `..._unknown_view_degrades_to_default_multi_pane`, `..._dock_param_regression_intelligence_still_activates` (P02 deep links unaffected), and both legacy-route redirect tests. The test names match the report's description exactly.

**The B-4 sequencing condition is satisfied.** The parser exists and is test-covered. No page was deleted ahead of it.

---

## 3. ITEMS 1–2 — VERIFIED

### R1 — Capability preservation: **complete, 1:1**

Every heading in each source page is present in its replacement panel.

| Source page | Re-homed panel | Capabilities |
|---|---|---|
| `ScenarioComparisonPage` (281 ln) | `docks/ScenarioComparisonPanel.tsx` (289 ln) | Investigation Context · Existing persisted scenarios · Side-by-side comparison · Hypothetical result · Assumptions · Uncertainty · Provenance · Limitations — **all 8 present** |
| `PortfolioResearchPage` (163 ln) | `docks/PortfolioResearchPanel.tsx` (210 ln) | Investigation Context · Hypothetical Aggregate Figures · Report Builder / Export Preview · Uncertainty & Limitations · Included Scope · metric labels — **all present** |

Both panels grew (+8, +47 lines), consistent with added test hooks and dock chrome rather than capability loss. **`Uncertainty`, `Provenance` and `Limitations` — the constitutional honesty surfaces — all survive.**

### R2 — Redirects: **satisfied**

```
workspaceRegistry.tsx:39  <Navigate to="/?panel=scenarios" replace />
                     :43  <Navigate to="/?panel=portfolio" replace />
```

Both legacy routes remain registered and now resolve to redirect components:

- `compare.scenarios` → `route: "/compare-scenarios"` → `Component: ScenarioComparisonRedirect`
- `review.portfolio_research` → `route: "/portfolio-research"` → `Component: PortfolioResearchRedirect`

Neither 404s. Bookmarks and deep links survive. The P02 `<Navigate replace />` pattern is extended correctly, and the parser (§2) makes these targets live rather than decorative.

### R3 — No fabricated fallbacks: **satisfied**

`grep -E '(\?\?|:)\s*"[0-9]{1,3}\.[0-9]%"'` across both new panels → **0**.

### R4 — Test hooks: **satisfied and exceeded**

`PortfolioResearchPanel` **10** hooks · `ScenarioComparisonPanel` **8** hooks. Both source pages had **zero**. Dedicated panel test files exist for each.

### R6 — RBAC: **unchanged**

16 `protectedWorkspace()` wrappers over 16 route entries — full coverage, no entry bypasses the wrapper. `ALL_AUTHENTICATED_ROLES = ["admin", "operator"]` unchanged at line 122. Zero `unprivileged` grants.

### P02 regression guard: **all four closures intact**

Fabricated literals **0** · palette relabels **3** · orphaned P02 pages **all absent** · `signal_state` verbatim rendering retained.

---

## 4. OBSERVATION — `OBS-CONV3-3`: ORPHANED PAGES, PATTERN REPEAT

| Field | Content |
|---|---|
| **Finding ID** | `OBS-CONV3-3` |
| **Requirement** | BO §3 / turn-56 reframe — absorbed surfaces must not persist as unrouted orphan page files. This is the identical requirement as `OBS-CONV2-4`. |
| **Evidence** | `pages/ScenarioComparisonPage.tsx` (281 ln) and `pages/PortfolioResearchPage.tsx` (163 ln) remain in the tree. Their registry entries now point at redirect components, so **nothing routes to them**. Live-import check: zero imports outside their own test files. |
| **Failure** | Two unrouted, duplicate implementations persist alongside their replacements. `ScenarioComparisonWorkspace` and `PortfolioResearchWorkspace` are each now exported from two locations. This is precisely the duplicate-implementation hazard the turn-56 reframe forbids and that `OBS-CONV2-4` was raised to eliminate. |
| **Aggravating** | Their test files — `pages/ScenarioComparisonPage.test.tsx` (5,626 B) and `pages/PortfolioResearchPage.test.tsx` (4,540 B) — are still in `pages/` and still import from the orphaned pages. **The delivery report stated these were moved:** `pages/PortfolioResearchPage.test.tsx → docks/PortfolioResearchPanel.test.tsx`, "moved + import-path updates". They were **copied, not moved.** The dock test files exist; the originals were never removed. |
| **Mitigating** | No capability is lost and no user-facing defect results — every route resolves correctly. Severity is **low**; this is hygiene and report accuracy, not function. |
| **Required Correction** | Delete `pages/ScenarioComparisonPage.tsx`, `pages/PortfolioResearchPage.tsx` and their two `pages/*.test.tsx` files. Confirm the suite stays green. Fold into the next cycle — **no separate cycle**. |
| **Closure Evidence** | Fresh clone: four files absent; single export for each workspace component; suite green. |
| **Owner** | DA |

**This is the third occurrence of the same class.** `ChartWorkspacePage` was relocated-not-deleted in P02 (legitimate — a consumer remained). Three pages were re-added by a stale-baseline patch in `5ef6c4e` (a transport artifact). Here, two pages were superseded but left behind. Each had a different cause; the common thread is that **"re-homed" is being treated as complete when the new surface works, before the old one is removed.** Re-homing is complete when exactly one implementation exists.

**A discrepancy between "moved" and "copied" in a delivery report is the specific kind of wording defect `OBS-CONV2-2` was raised for.** It is minor here and I do not doubt the intent — but a report that says *moved* when files were *copied* is the same failure mode that let three orphan pages survive P02 unnoticed. State dispositions exactly.

---

## 5. OBSERVATION — `OBS-CONV3-1` CARRIED FORWARD (capture fold)

Captures 01 and 04 terminate at the "Hypothetical research only" banner; the Portfolio panel body is below the fold. The report's claim that capture 04 shows "4 aggregate cards, report preview, scope" is **not visually evidenced**.

**Downgraded in significance, not withdrawn.** Source verification now confirms all five capability groups exist in `PortfolioResearchPanel.tsx`, so the *capability* claim is proven by code. What remains unevidenced is the *rendering*. Re-capture scrolled to the panel body in the next cycle.

`OBS-CONV3-2` (capture cannot prove a DOM attribute) is **closed** — `data-stage-view` is verified in source at line 155 and asserted by named test, which is the correct evidence type for an attribute.

---

## 6. STILL ASSERTED, NOT VERIFIED

| Claim | Status |
|---|---|
| 1,160 tests passing (163 suites / 745 frontend + 415 backend) | **NOT VERIFIED.** 165 frontend test files counted at `34f4c62` — consistent with the claim, but a file count is not an execution result. No transcript supplied. |
| `npm ci` → `tsc -b` clean | **NOT VERIFIED.** No transcript. `OBS-CONV2-6` remains open. |
| `vite build` succeeds; bundle +1.82 kB | **NOT VERIFIED.** No transcript. |

**A summary line is not execution evidence.** Earlier cycles supplied raw console output; supply it again. This does not block Cycle 1 — the corrections are string-verifiable and the risk is low — but it must not become the norm.

---

## 7. TRANSPORT — `CA-CONV2-3` RESOLVED IN EFFECT

The new repository contains the Cycle-1 code. The six-failure transport deadlock is **broken**.

Recorded for continuity: the mechanism that finally worked was the Operator publishing a clean repository containing the DA's work. The PAT + working-branch arrangement in the transport directive remains the durable fix for the remaining phases — **11 phases remain** (P03 items 3/5/6/4, SURF ×3, DATA ×2, CHART ×4, POLISH ×2). Without a push path for the DA, every cycle depends on an Operator-mediated republish.

`CA-CONV3-1` (Cycle-1 code not transmitted) is **CLOSED** — superseded by this baseline.

---

## 8. STATUS

| Item | State |
|---|---|
| UI-CONV-P03 Cycle 1 | **APPROVED WITH OBSERVATIONS** |
| `OBS-CONV2-7` `?view=` inert | **DISCHARGED** |
| `CA-CONV3-1` transport | **CLOSED** — superseded by new baseline |
| `OBS-CONV3-2` evidence mapping | **CLOSED** |
| `OBS-CONV3-3` orphaned pages + report wording | **NEW** — fold into next cycle |
| `OBS-CONV3-1` capture fold | **CARRIED** — re-capture scrolled |
| `OBS-CONV2-6` `tsc -b` transcript | Open |
| `OBS-CONV2-2` relocation wording | Open — recurs as `OBS-CONV3-3` |
| `OBS-CONV2-5` / `TD-...-SCEN002` fixtures | Open — deviation register |
| `OBS-PROV-2` `docs/evidence/` | Open |
| `OBS-5` bundle delta | Open |
| `F-BRAND-1` | Open — GA-173 |
| P02 closures ×4 | **Verified intact at `34f4c62`** |

**Remaining P03 items:** 3 (`WorkspaceCustomizationPage`), 5 (`GovernanceEvidencePage`, RBAC-sensitive), 6 (`SignalInvestigationPage`), then 4 (`ResearchManagementPage` — disposition note approved, B-4 satisfied, **cleared to proceed**).

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not authorization** for the next phase.
**No implementation** beyond `BUILD_ORDER_UI-CONV-P03` scope.

**We don't guess. We prove.**
