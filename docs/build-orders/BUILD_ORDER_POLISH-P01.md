# BUILD ORDER — POLISH-P01

**Issued by:** Independent Technical Review & Governance Authority (authorized by Operator)
**Date:** 2026-08-18
**Phase:** POLISH-P01 — final phase: open observations, simulator realism, evidence confluence
**Base of record:** 15-element chain (through `chart_p03.patch.txt`)
**Operator scope decisions (this turn):** fix `OBS-DATA2-1` · build Confluence as **evidence-only**

**This is the last phase in the programme.** Its purpose is to discharge what has accumulated, not to open new ground.

---

## 1. VERIFIED STATE

Confirmed against the current tree, not recalled:

| | Count |
|---|---|
| RBAC routes | **16** |
| Registered indicators | **29** |
| Backend test files | **69** |
| Frontend test files | **174** |
| Tests | **473 BE + 853 FE = 1,326** |
| Bundle | **748.05 kB** |

---

## 2. MANDATORY REQUIREMENTS (M1–M7)

### M1 — 🔴 `OBS-DATA2-1`: remove the directional drift

All three walks carry a **positive mean**:

```python
crypto : rng.gauss(0.0004, 0.0083)
JPY    : rng.gauss(0.004,  0.015)
forex  : rng.gauss(0.00004, 0.00015)
```

Measured consequence: EURUSD drifts `+0.0576` in one day (`+5.2%`) and `+0.3456` over six days (**`+31.4%`**). No FX pair trends one direction for six days at 31%.

**Required:** a zero-mean or mean-reverting walk, so long windows no longer trend. State the chosen model.

**This reopens the DATA-P01 generators, which are otherwise closed.** The authorization is narrow: **the mean/reversion term only.** Do not alter per-symbol seeding (`symbol_seed`), class factor streams, betas, the `_base_price` table, the market-class branch, or the provenance markers. Those took three correction cycles to stabilise and are not in scope.

**Consequences you must handle, and which I have already checked:**
- **No test hardcodes a seeded price.** The DATA-P01 determinism test compares run-to-run equality, so it must be **re-run, not rewritten.**
- CHART-P01/P02/P03 hand-computed tests use their own fixtures and are unaffected. **If you find yourself editing an expected value in a CHART test, stop — something else has broken.**
- Captures showing price levels become stale; re-capture what you cite.

### M2 — 🔴 `OBS-5`: the bundle is one monolithic chunk

748.05 kB with **zero code splitting**: no `manualChunks`, no `React.lazy`, no dynamic `import()`, and 16 route components eagerly imported into a single chunk. The heaviest sources are `ResearchHubView` (64 kB), `TerminalChartStage` (52 kB), `InstitutionalIntelligencePage` (52 kB), `TerminalBottomDock` (50 kB).

**Required:** route-level code splitting so the initial load carries the terminal, not all sixteen workspaces. Report initial-chunk size before and after.

**Constraint:** splitting must not break RBAC. A lazily-loaded route must still be gated by `protectedWorkspace()` **before** its chunk is requested — a chunk fetched for an unauthorized route is an information leak even if the render is blocked. **Prove this**, do not assert it.

### M3 — `OBS-DATA-P01-WATCHLIST-CLIP`
`grid-template-columns: var(--ix-terminal-watchlist-width, 240px)` with `overflow: hidden`. BTC's widest strings left under one pixel of margin. Give the column enough room, or let it size to content within a bound. **Do not solve it by truncating values.**

### M4 — `OBS-CHART-1`: remove the orphaned placeholder
`frontend/src/pages/ChartPlaceholderPage.tsx` says *"Reserved for TradingView Lightweight Charts integration"* and *"Not Initialized"*. That integration shipped three phases ago. Referenced nowhere — not the registry, not a component, not a test. Delete it.

### M5 — Confluence engine, **evidence-only** (Operator decision)

Build as **evidence aggregation**: count how many active indicators align in the same direction, presented as a **score with an uncertainty band** and the `NON-ACTUATING` label, following the Advisory Signals precedent exactly.

**🔴 Explicitly NOT authorized — do not build:**
- **`Trade Eligibility`** — a go/no-go verdict. Requires a formal constitutional amendment that has not been made.
- **`Risk/Reward`** — requires an implied entry, stop and target: actionable trade parameters.
- **`Setup Quality`** as a recommendation. A neutral descriptive score is acceptable; a "quality" judgement that implies tradeability is not.

The distinction is not cosmetic. *"7 of 9 active indicators are directionally aligned; uncertainty ±2"* is a description of the operator's own indicator set. *"Setup quality: high, eligible"* is advice. **The first is authorized; the second is not.**

Confluence must state that it aggregates **the operator's currently active indicators over simulated data** — it is not a market opinion.

### M6 — `F-BRAND-1` / `GA-173`: login and logo
Operator directive (turn 57), still outstanding: the login page must be presentable, 3D-like, welcoming, attractive and trading-related; the logo must be **a drawing compass with an epsilon symbol beside it**. Neither exists — `LoginPage.tsx` has no 3D/gradient/perspective treatment and no compass or epsilon asset is present.

**Note:** this is the one item in the programme originating in an explicit Operator design instruction rather than a review finding. Build it to that description.

### M7 — T-1 guard extended for confluence
Keep the anchor pinned. Extend the forbidden list with the vocabulary M5 excludes: `eligible`, `eligibility`, `risk/reward`, `r:r`, `setup quality`, `take the trade`, `high probability setup`, plus the standing actuation and institutional-claim terms.

**Confluence is the single most likely surface in this programme to drift into advice.** Guard it accordingly.

---

## 3. CONSTRAINTS (R1–R6)

- **R1** — Generators are opened **only** for M1's mean/reversion term. Everything else in DATA-P01 stays closed. DATA-P02 aggregation and all 29 indicator formulae stay closed.
- **R2** — RBAC unchanged: **16 routes**, `protectedWorkspace()`. M2 makes this a live risk — verify independently and prove chunk-level gating.
- **R3** — Constitutional: no automated execution, external LLMs, dynamic plugins, live trading. **No recommendations, eligibility verdicts, or entry/stop/target output.**
- **R4** — Provenance vocabulary unchanged: `seed:synthetic`, `live:simulated`.
- **R5** — No new dependencies without justification. Code splitting is a bundler configuration, not a library.
- **R6** — Report bundle **initial chunk** and **total** against 748.05 kB. This is the phase where `OBS-5` is discharged, so the number is the deliverable.

---

## 4. EVIDENCE REQUIRED

**The image is primary; instruments corroborate and must measure rendered extent.**

### Captures
1. **Drift fixed** — a six-day `1D` chart showing a non-trending series. Compare against the CHART-P02 capture where EURUSD climbed 1.24→1.44.
2. **Watchlist clip resolved** — BTC's widest row fully visible.
3. **Confluence** — the evidence score with its uncertainty band and `NON-ACTUATING` label.
4. **Login page** — the M6 redesign.
5. **Logo** — compass with epsilon, legible at rendered size.
6. **Route splitting** — a network trace showing the initial chunk and a route chunk loading on navigation.
7. **RBAC under splitting** — an unauthorized route: **chunk not fetched**, access denied.

### Named tests — each must fail against current code
- `test_polish_p01_walk_has_no_directional_drift_over_long_windows` — assert a property (mean return ≈ 0 over N bars within tolerance), **not** a golden value.
- `test_polish_p01_chart_seed_determinism_still_holds` — the DATA-P01 test **re-run**, unmodified.
- `test_polish_p01_lazy_route_chunk_not_fetched_when_unauthorized`
- `test_polish_p01_confluence_emits_score_with_uncertainty_not_verdict`
- `test_polish_p01_no_eligibility_or_risk_reward_language` (M7)

### Executed evidence
Full `pytest`, `vitest`, `tsc -b`, `npm run build`. Distinguish executed from asserted. Baseline **1,326 tests**.

---

## 5. ACCEPTANCE CRITERIA

1. M1–M7 satisfied and independently verifiable.
2. R1–R6 honoured.
3. Drift removed; determinism test **re-run unmodified** and green.
4. No CHART test expected-value edited.
5. Initial chunk materially smaller; RBAC gating proven at chunk level.
6. Watchlist clip resolved without truncating values.
7. Orphan placeholder deleted.
8. Confluence emits a score with uncertainty — **no eligibility, no risk/reward, no verdict**.
9. Login and logo match the Operator's description.
10. All seven captures legible, hashed, reconciled.
11. Every named test fails on current code, passes after.
12. Full transcripts supplied.
13. Delivery report documents changes and **all deviations, including failed attempts**.
14. Patch applies clean on the 15-element chain; sha256 declared and matching.
15. Bundle initial + total reported.

---

## 6. DELIVERY PROTOCOL

Upload: patch · delivery report · capture verification JSON · PNGs. **Artifact of record is the verified patch, not a commit.** No commits, pushes or pulls — repository activity is Operator-timed.

**Before uploading, verify every sha256 declared in the report resolves to an attached file.** The check worked in CHART-P03; keep it.

---

## 7. NOTES TO THE DA

This is the final Build Order of the programme. Five phases have been approved, three of them unqualified, and across CHART-P01/P02/P03 I hand-verified thirty-five formulae and detections and found no arithmetic error.

Two cautions specific to this phase.

**M1 reopens code that is otherwise closed.** The authorization is deliberately narrow. The risk in a cleanup phase is scope creep into stable code because it is finally being touched again. **If you believe something adjacent needs changing, raise it as a recommendation — do not build it.**

**M5 is where this programme could still fail its own constitution.** Everything built so far describes data. Confluence is the first surface that aggregates *interpretations*, and the distance from "7 of 9 aligned" to "high-probability setup" is one adjective. The Operator authorized evidence aggregation and explicitly did not authorize eligibility. **Count the evidence; refuse the conclusion.**

Two standards worth repeating because they have held throughout: fix the defect **class** rather than the cited line — you have done this five phases running — and disclose failed attempts, which has caught real defects including a bubble-phase click handler that jsdom could never have found.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Authorizes POLISH-P01 only. Programme closure is a separate determination after this delivery is reviewed.

**We don't guess. We prove.**
