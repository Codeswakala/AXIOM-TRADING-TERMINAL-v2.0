# ITRGA REVIEW — UI-NEW-P01 (ATTEMPT 3 · CA-P01-4 EVIDENCE)

| Field | Value |
|---|---|
| Document type | ITRGA Phase Determination — corrective evidence pass |
| Issued by | Independent Technical Review & Governance Authority |
| Date | 2026-08-12 |
| Evidence received | `Screenshot 2026-08-12 185327.png` — sha256 `8746cfee81d9adf041d9dcf30953d648629179b438b2841fa411decf172fb238`, 1364×682 |
| Prior evidence | `Screenshot 2026-08-12 181045.png` — sha256 `31266457…`, 1365×681 |
| **DETERMINATION** | **APPROVED WITH OBSERVATIONS** — subject to §6 closure conditions |
| Confidence | **HIGH** |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. CA-P01-4 — DISCHARGED

The DA has answered the full-bleed finding by implementation rather than argument, and the two captures — 43 minutes apart, same session, same server — form a controlled before/after pair.

| Attribute | 15:10:36 UTC | 15:53:22 UTC |
|---|---|---|
| Right `WORKSPACE CONTEXT` panel (~265px) | Present | **Removed** |
| Bottom `ACTIVITY TELEMETRY` / `WORKSTATION ACTIVITY` | Present | **Removed** |
| Left navigation | ~220px labelled dock | **~40px icon rail** |
| Terminal width | ~55% viewport | **~96%** |
| Terminal height | ~60% viewport | **~85%** |
| `Terminal Analytics Dock` (P05 slot) | **Clipped** at shell boundary | **Fully visible** |

The competing chrome is gone. All five docked slots now render completely: `Market Watchlist [P02]`, `Primary Candlestick Chart Stage [P03]`, `Signals & Spread Telemetry [P02/P04]`, and `Terminal Analytics Dock [P05]`, beneath the persistent ticker.

**This resolves the P02 compounding risk I flagged.** The 220px labelled navigation column that would have sat beside a P02 watchlist dock — producing two parallel vertical navigation columns — is now a 40px icon rail. P02 can dock its watchlist without colliding.

The delivered result corresponds to disposition **(b)** from my §4 menu: terminal renders effectively full-bleed at `/` with shell chrome suppressed, while the icon rail preserves reachability of the other 15 routes. That is a sound engineering answer — it satisfies Directive §2 without severing navigation, and it does not require the other routes to be rebuilt.

**Residual, recorded as an observation rather than a finding.** The page header `Operations` with breadcrumb `AXIOM · Observe · Operations` persists above the ticker. Strictly, a terminal titled "Operations" retains a trace of the administrative framing Directive §2 warns against, and Plan §D classified `DashboardPage.tsx` as REPLACE. It costs roughly 40px and does not impair the terminal. I raise it as **OBS-P01-6** for P06 cleanup, not as a blocker — the substance of CA-P01-4 is discharged.

## 2. T-6 and T-1 — sustained across both captures

The honest-state behaviour did not regress under the layout change. At 15:53:22 the ticker still reads `Empty Feed`, `SPREAD: --`, `VOL: --`, `H: -- L: --`, `WS: IDLE [○]`, `LIVE:SIMULATED`, with a live clock. Two independent observations 43 minutes apart, across a structural refactor, both honest. That is stronger evidence than either capture alone.

Control inventory at 15:53:22 remains free of any execution affordance: `Workspace switcher`, `Global search`, `Command palette Ctrl K`, `Light theme`, `admin`, `Sign out`, icon rail. **No buy, sell, order, or broker control.** `GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING` remains prominent in the ticker.

---

## 3. Determination

**APPROVED WITH OBSERVATIONS.**

UI-NEW-P01 — Terminal Foundation & Multi-Pane Shell Architecture — satisfies its Build Order acceptance criteria. Basis:

| Requirement | Status |
|---|---|
| §W acceptance — ticker persistent, grid mounts without DOM collisions | ✅ Level I |
| T-1 zero actuation | ✅ Level I (both captures) + named test #3 |
| T-6 data honesty | ✅ Level I (both captures) + named test #4 |
| C-1 order-book permanence | ✅ Level II grep, 0 matches |
| Six mandatory named tests | ✅ Displayed passing by name |
| Regression 150f/617t · 414 backend · 1,031 | ✅ Arithmetic reconciles from both directions |
| Scope compliance — P02–P05 held | ✅ Placeholder slots, no future scope |
| Doc 17 SAL-2 + §17.8 Gates 1–3 | ✅ Gate 4 = this determination |
| CA-P01-4 full-bleed | ✅ Discharged |

I record the quality of the T-6 implementation once more, because it is the point of the exercise: shown a wireframe specifying `EUR/USD 1.08450 · SPREAD: 0.8 · VOL: 14.2M`, the DA built a terminal that renders dashes when it has no feed. The honest path was chosen deliberately, and it held through a structural refactor.

## 4. Observations carried to P02

| ID | Observation |
|---|---|
| **OBS-P01-6** | `Operations` page header + breadcrumb persist above the ticker; retire at P06 |
| **OBS-P01-5** | Captures at 1364×682 vs specified 1920×1080; use full resolution for P02 chart/watchlist density |
| **OBS-P01-1** | Provenance: commit `ad5fd877` / tag `UI-NEW-P01_DELIVERY` not resolvable in origin; `git rev-parse --verify` output not supplied. **Must discharge before P06 handover** |
| **OBS-P01-2** | 13 evidence logs referenced by filename; supply raw grep output inline from P02 |
| **OBS-P01-3** | Doc 16 B-7 unaddressed in §15 |
| **OBS-P01-4** | Root still mounts `DashboardPage.tsx`; rename at P06 (Plan §D said REPLACE) |
| **OBS-5** | Bundle 648.22 → 650.02 kB (+1.80 kB); proportionate, disclosed |

## 5. Findings remaining open

```
CA-P01-1 (iii) — logged-out / capture showing redirect to /login          Owner: Operator
CA-P01-2       — TD-005, TD-021, TD-029, TD-UI-REACTROUTER-MODERATE
                 descriptions restated verbatim from register v3.0.12      Owner: DA
CA-P01-3       — GA-167 confirmed recorded under OPERATOR authority
                 (origin register still GA-166; Tier-5 amendment)          Owner: Operator
```

## 6. Closure conditions and P02 authorization

This approval is issued **subject to closure of CA-P01-1(iii), CA-P01-2 and CA-P01-3.** None is architectural; all three are administrative and none affects what P02 must build.

**`BUILD_ORDER_UI-NEW-P02` — I am prepared to issue it on your instruction.**

My recommendation, offered as a recommendation and not a requirement: issue P02 now, with the three residuals bound as conditions of the P02 delivery rather than gates on it. CA-P01-3 (GA-167) is the one I would not let run past P02 delivery — it is a Tier-5 amendment, and P02 is the phase that first exercises the displaced panel architecture in earnest.

**P02 scope, when authorized**, is bounded to Plan §V-P02 as re-scoped by C-1: `TerminalWatchlistDock.tsx` and `TerminalSpreadTelemetry.tsx` — candle-derived spread, tick frequency, session volume. **No order book. No depth ladder. No bid/ask rendering.** That exclusion is permanent while the Gate is closed.

---

This determination applies only to UI-NEW-P01 and its supporting evidence. It does not constitute production certification or authorization to execute any successor phase.

Historical UI-001…UI-011 records remain historical unless separately superseded.

No implementation of P02 may begin before `BUILD_ORDER_UI-NEW-P02` is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
