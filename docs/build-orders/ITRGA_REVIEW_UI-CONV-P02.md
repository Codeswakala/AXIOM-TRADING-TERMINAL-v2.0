# ITRGA REVIEW — UI-CONV-P02

| Field | Value |
|---|---|
| Document type | ITRGA Phase Determination (Directive §§29–31; Doc 17 §17.8 Gate 4) |
| Issued by | Independent Technical Review & Governance Authority |
| Date | 2026-08-13 |
| Submission | `DELIVERY_REPORT_UI-CONV-P02.md` — sha256 `a25f650e3065760fc607198cef9799b9c0fbfb898324f5401ca39c7682e96dcb`, 27,276 B, 293 lines |
| Browser evidence | 6 captures, all **1920×1080**, all digests verified |
| **DETERMINATION** | **CORRECTIVE ACTIONS REQUIRED** |
| Confidence | **HIGH** |
| CONV-P03 authorization | **NOT ISSUED** |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. The core objective is achieved

**B-CONV2-1 — the duplicate statistical paths are gone.** This was the phase's reason for existing, and the DA executed it correctly. §2 confirms `formatConfidence()` in `AdvisorySignalsPage.tsx` and the duplicate `intervalText()` in `PerformanceAnalyticsPage.tsx` are **retired from application code** — deleted, not adapted, as required.

Level-I corroboration across the captures: every rendered confidence carries its bounds or an explicit qualifier, and I checked the arithmetic on each.

| Rendered | Value | Brackets? |
|---|---|---|
| Signal 1 `EMITTED` | `78.4% · Wilson: [72.4% — 84.1%]` | ✅ |
| Signal 2 `WITHHELD` | `48.0% · [Uncertainty: Unavailable]` | ✅ correct withholding |
| Signal 3 `EXPIRED` | `62.5% · [Uncertainty: Unavailable]` | ✅ correct withholding |
| Calibrated Coverage | `78.4% · [72.4% — 84.1%]` | ✅ |
| Clean Advisory Rate | `82.4% · [78.9% — 85.4%]` | ✅ |
| Guardrail Intervention | `17.6% · [14.6% — 21.1%]` | ✅ |

**No bare percentage appears anywhere in the evidence set.** The defect I measured at `AdvisorySignalsPage.tsx:224` is eliminated.

**B-CONV2-2 — absorption verified.** §3 supplies the capability inventory: `ChartWorkspacePage.tsx` (878 lines), `AdvisorySignalsPage.tsx` (328), `PerformanceAnalyticsPage.tsx` (186) retired with each affordance mapped to a new home. Capture 01 shows the signal drill-down now carrying `RESEARCH RATIONALE (VERBATIM)`, `GUARDRAILS & STATE CRITERIA` (operating domain, economic verdict, calibration status, validity window, expires-at) and `MODEL LINEAGE & AUDIT` (artifact, experiment, feature set) — the richer legacy detail view preserved inside the terminal, as §4 required. Capture 03 confirms `/signals` deep-links into the terminal.

**B-CONV2-3 — closed.** `PriceChart.tsx` remediated via `getComputedToken` against `--ix-*`; the seven literals are gone and `TD-005` is closed. The P04/P06 reconciliation discrepancy is resolved.

**Observations closed:** OBS-CONV-2 (capture 06, Playwright `reducedMotion: 'reduce'`), OBS-CONV-4, OBS-CONV-5 (ledger reinstated), OBS-CERT-3.

All six capture digests match §9(f) exactly. I verified each file.

---

## 2. 🔴 CA-CONV2-1 — The palette still offers the retired routes, and shows 6 entries where 16 are claimed

**Classification: Blocker (accuracy + scope). Evidence: Level I, capture 05.**

§9(f)(v) describes capture 05 as *"all 16 registered routes grouped by navigation category on empty query"* and marks **OBS-CONV-3 CLOSED**. I read the capture. It shows **six entries in three groups**:

```
OBSERVE   Open Operations · Open Live Market · Open Chart Workspace
DETECT    Open Advisory Signals
ANALYZE   Open Performance Analytics · Open Institutional Intelligence
```

Two distinct problems.

**(a) The count is wrong.** Six entries, not sixteen. Ten registered routes — `/investigate`, `/compare-scenarios`, `/trade-plans`, `/execution-research`, `/portfolio-research`, `/journal`, `/research-management`, `/governance`, `/workspace`, `/chart` — do not appear. The panel is not scrolled; it terminates after `Open Institutional Intelligence` with clear space below. **OBS-CONV-3 is not closed**, and marking it closed against this capture is the specific defect pattern I have now flagged four times: a description drafted from intent rather than from the delivered artifact.

**(b) The palette advertises surfaces this phase retired.** `Open Chart Workspace`, `Open Advisory Signals` and `Open Performance Analytics` are the three pages CONV-P02 deleted. Their presence is not necessarily wrong — a redirect target is a legitimate destination — but the labels are, because they name workspaces that no longer exist. An operator selecting *"Open Chart Workspace"* now lands on the terminal chart stage. The label promises a page; the product delivers a dock.

This bears directly on B-CONV2-2. The capability survived; **the navigational vocabulary did not follow it.** Retiring a surface means retiring its name from the navigation, or relabelling to the destination — `Open Chart Stage`, `Open Signals Dock`, `Open Intelligence Dock`.

**Required correction:**
1. Palette on empty query enumerates **every** registered route, grouped, scrollable if needed — and the capture must show it (scroll evidence acceptable).
2. Retired-surface entries relabelled to their actual destinations.
3. Reconcile the route count explicitly. P06 §B-P06-4 established **17** (16 protected + `/login`); with `/charts`, `/chart`, `/signals`, `/analytics` now redirects, state the post-absorption number and what the palette should contain.
4. `test_uiconv_p02_...` claiming full route coverage must assert the **count**, not merely that the palette opens. The current test passes while the palette shows six.

## 3. 🔴 CA-P03-1 — GA-167 (16th cycle) — Operator-owned

Unchanged: origin head `GA-166`, `grep -c "GA-167"` = 0, delivery commit absent from origin. Binds delivery approval per Build Order §1.1. The DA again correctly declined to transcribe it.

---

## 4. Observations

- **OBS-CONV2-1 (new)** — capture 01's drill-down panel is **clipped at the right edge**: `Wilson: [72.4% — 84.1%` and `Feat: feat.m1.v2` are cut off, and `Calibration Report:` is truncated at the panel bottom. The dock cannot accommodate the absorbed detail view at this width. Since B-CONV2-2 moved *richer* content into a *narrower* container, this needs a scroll affordance, a wider dock, or a detail overlay. **A truncated uncertainty bound is a data-honesty concern, not merely cosmetic** — an operator must never see a partial interval.
- **OBS-CONV2-2 (new)** — captures 01/02 show the chart stage empty (`No Candle Data`) while capture 04 shows it seeded from the same session. Consistent with capture sequencing; noted only so it is not misread as regression.
- **OBS-CONV2-3 (new)** — the signal state badge differs across captures for the same signal: `EXPIRED` in CONV-P01 capture 03, `WITHHELD` here. If the fixture changed, say so; if state is being derived rather than read from `signal_state`, that is a defect. Clarify in the next report.
- **OBS-5** — I expected a bundle **decrease** given 1,392 lines retired. Confirm the delta explicitly; an increase requires justification.
- **F-BRAND-1** — AX Monogram correctly retained; compass+Epsilon still blocked pending **GA-173**.
- **OBS-CERT-2** — corpus not at origin.

---

## 5. Determination

**CORRECTIVE ACTIONS REQUIRED.**

The hard part of this phase is done and done well. Three duplicate surfaces are deleted, 1,392 lines removed, the triple statistical code path collapsed to one, the richer signal detail preserved rather than lost in the merge, and `PriceChart.tsx` finally reconciled. Six statistics render with correctly bracketing intervals and two correctly withhold. That is the outcome CONV-P02 existed to produce.

What fails is the navigation layer around it. The palette shows six routes where sixteen were claimed, and three of those six invite the operator to open workspaces that no longer exist.

```
CA-CONV2-1  Blocker · accuracy + scope
  Req  BO §9(f)(v) — palette enumerates all registered routes; OBS-CONV-3 closure
  Ev   Capture 05 shows 6 entries in 3 groups; 10 routes absent; panel not scrolled;
       entries name Chart Workspace / Advisory Signals / Performance Analytics — all retired
  Fix  Enumerate all routes; relabel retired-surface entries to destinations;
       reconcile the post-absorption count; assert count in the named test
  Own  DA

CA-P03-1    Blocker · constitutional · 16th cycle · OWNER: OPERATOR
  Req  GA-167 recorded under Operator authority and readable at origin
  Ev   grep = 0; head GA-166; delivery commit absent
  Fix  Record or confirm authorship; push
  Own  Operator
```

**On closure I will issue APPROVED WITH OBSERVATIONS and authorise CONV-P03.** CA-CONV2-1 is a palette registration fix and one re-capture.

## 6. CONV-P03 authorization

**`BUILD_ORDER_UI-CONV-P03` IS NOT ISSUED.**

CONV-P03 re-homes the remaining surfaces — investigate, compare-scenarios, portfolio-research, research-management, governance, workspace. Note the dependency this phase just exposed: `/investigate` shares the signal drill-down built here, so **OBS-CONV2-1's width problem must be solved before CONV-P03 builds on it.**

---

This determination applies only to UI-CONV-P02 and its supporting evidence. It does not constitute production certification.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**. Handover remains **WITHHELD**. No CONV-P03 implementation may begin before its Build Order is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
