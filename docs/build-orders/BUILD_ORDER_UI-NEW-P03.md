# BUILD ORDER — UI-NEW-P03

**Primary Chart Stage · Multi-Timeframe Controls · Technical Overlays · Research Annotations · Seed Provenance Discipline**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional Trading Terminal Transformation |
| Workstream | UI-NEW — Institutional Trading Terminal Rebuild |
| Phase | **UI-NEW-P03** |
| Preceding determination | `ITRGA_REVIEW_UI-NEW-P02.md` — ✅ **APPROVED WITH OBSERVATIONS** |
| Approved plan | `UI-NEW_ENGINEERING_DESIGN_PLAN.md` · SHA-256 `8834aa91…` · §V-P03 |
| Governing docs | Operator Directive §§18–20, 25–32; Plan §N (T-1…T-7), §V-P03, §W, §X; `17_INSTITUTIONAL_SECURITY_STANDARD.md`; Doc 16 Part XIV; `QUALITY_GATE_SPEC.md`; `REPOSITORY_PROVENANCE_PROTOCOL.md` §2; GA-050 (W5-U03 annotation posture) |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend **414** · frontend **152f / 631t** · platform **1,045** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Precondition — CA-P02-1 must close before delivery review

**`GA-167` remains unrecorded at origin (GA-166 is the register head), now for a third cycle.** I stated in the P02 determination that I would not approve P03 with it open, and I hold that.

P03 places the chart stage — the programme's centrepiece — inside the panel architecture that displaces Tier-5 `08_UI_UX_SPEC.md`. `10_CONSTITUTIONAL_HIERARCHY.md` holds Tier 5 prevailing until formally amended. Implementation may proceed under this order; **the delivery will not be approved until GA-167 is recorded under Operator authority.** Owner: **Operator**. Neither DA nor ITRGA may record it (`03_AXIOM_SPEC.md`).

---

## 2. Purpose & scope

Elevate the candlestick chart to the terminal's first-class centre stage, answering Directive §33 — *"why is this a trading terminal rather than another dashboard?"*

**IN scope (Plan §V-P03):**

1. **`TerminalChartStage.tsx`** — full-height TradingView `lightweight-charts` canvas in the P01 centre slot, consuming the active symbol from `TerminalContext` (P02).
2. **Timeframe toolbar** — M1 · M5 · 15M · 1H · 4H · 1D, with the honest-resolution notice required by §4 below.
3. **Chart style toggles** — Candles · Bar · Line · Area.
4. **Technical overlays** — client-side presentation indicators only, subject to §5.
5. **Research annotations** — read and create over the existing `/api/v1/collaboration/chart-annotations` seam, subject to §6.
6. **`terminalChartStage.test.tsx`** + `uinew_p03_security_invariants.test.ts`.

**OUT of scope — do NOT build:**

- Order book, depth ladder, bid/ask/size (C-1, permanent while the Gate is closed).
- P04 signal stream · P05 dock content · P06 audit.
- Any actuation (T-1); any external LLM (T-4); any new endpoint, table, migration, or dependency. Alembic locked at `20260717_0037`.
- Any price, bar, or indicator value not traceable to a backend source (T-6).

---

## 3. 🔴 B-P03-1 — `getComputedToken` does not exist

**Evidence: Level I.** `grep -rn "getComputedToken" frontend/src` returns **0 occurrences** on origin.

Plan §T RSK-NEW-02 designates this resolver the mitigation for canvas colour-parsing failure, and §Z.1 Q6 states the chart "retains `lightweight-charts` with dynamic CSS token resolution (`getComputedToken`)." The mitigation is currently notional.

This matters concretely: `lightweight-charts` renders to canvas and requires resolved colour values. It cannot parse `var(--ix-color-*)`. Passing an unresolved custom property yields a black void or a silent default — and under Doc 16 the alternative (hardcoding hex) is a brand violation. The resolver is the only compliant path.

**Required:** implement `getComputedToken` (or an equivalently-named resolver), reading computed CSS custom-property values before passing them to the canvas API, with a named test proving a token resolves to a concrete colour and that the chart renders no hardcoded hex. If it already exists in DA-local custody, cite file and line.

## 4. 🔴 B-P03-2 — Timeframe honesty (TD-029)

`TD-029` — *"Multi-TF UI vs M1 sim"* (register L40, **Open**) — records that the simulated feed produces M1 bars while the UI offers multiple timeframes. P02's own §17 disclosed this and promised "an honest resolution notice."

Selecting 4H or 1D against an M1-only source produces either resampled bars or sparse/empty series. **Neither may be presented as native higher-timeframe market data.** The chart must disclose, at the point of display, when the rendered series is resampled from M1 or is incomplete. Silence here would be a T-6 breach of the same class as the depth ladder.

## 5. 🔴 B-P03-3 — Indicators are presentation, not analysis

`05_SYSTEM_ARCHITECTURE.md` §30 constrains the Chart State Service to **"presentation state only — no analytical reasoning in the chart layer."**

Client-side moving averages or similar visual overlays are permissible as presentation. What is **not** permissible is the chart computing or displaying anything that constitutes analytical output — signal generation, confidence, probability, regime classification, or any derived recommendation. Those belong to P04 and to the governed backend research seams.

State explicitly which overlays are implemented and confirm each is presentation-only.

## 6. 🔴 B-P03-4 — Annotations: the phase's only mutation

`POST /api/v1/collaboration/chart-annotations` is a **write** — the first mutation UI-NEW has introduced. It is pre-authorized by **GA-050** (W5-U03: *"inert persisted markups… no execution/order/signal/Gate path"*), so it is permitted, but it is bounded:

- Operator-authored research markup only. **No AI-generated annotation** (Plan T-5; Directive §10).
- **No order, entry, stop-loss, take-profit, position-size, or account field** may enter an annotation payload — that would be an order ticket by another name (T-1).
- Annotations are inert markup. They emit no signal and trigger nothing.
- Existing W5-U03 audit behaviour must be preserved, not bypassed.

## 7. 🔴 B-P03-5 — Feed and seed controls are MUTATING endpoints

Plan §E shows `[Start Feed]` and `[Seed]` in the chart toolbar. I traced both:

| Control | Endpoint | Effect |
|---|---|---|
| Start / Stop Feed | `POST /market/live/start` · `/stop` | Starts or stops the live market adapter (service state) |
| Seed | `POST /market/live/seed-history` | **Writes 80 synthetic OHLC bars per symbol to the database** |

`seed_history` docstring: *"Insert `seed:synthetic` bars when series are sparse."* This is a **database write of synthetic market data initiated from a UI control**, and `TD-028` ("Chart seed synthetic") is open.

These are not execution controls and are not T-1 violations — no order, no broker, no account. But they are **state-mutating operator actions on market data**, and the terminal has been strictly read-only until now. Accordingly:

- If either control is surfaced, it shall be **explicitly labelled as writing simulated data** — a `Seed` button that silently inserts synthetic bars an operator may later read as market history is a T-6 hazard.
- Any bar originating from `seed:synthetic` shall be **visually distinguishable from `live:simulated` bars at the point of display**. Two different synthetic provenances must not be conflated.
- The DA may defer both controls to a later phase and state so. Deferral is acceptable; silent inclusion is not.

---

## 8. Conditions carried

- **B-P03-6** — CA-P01-1(iii) logged-out `/` redirect capture, outstanding since P01. Owner: **Operator**.
- **B-P03-7** — Provenance: commit, annotated tag, `git rev-parse --verify` output (form was correct at P02 — maintain it).
- **B-P03-8** — Single Active Phase; P04–P06 unauthorized.
- **B-P03-9** — No security regression (Doc 17 §17.11): `dangerouslySetInnerHTML` = 0, `eval(` = 0, RBAC, ticket-authenticated WS.
- **B-P03-10** — SAL declaration. P03 introduces a **write path** (annotations); confirm classification against Doc 17 §4 rather than assuming SAL-2.
- **B-P03-11** — Maintain the §19.1 **field-provenance table** established at P02, extended to every chart-rendered value including OHLC bars, overlays, and annotation fields.

---

## 9. Mandatory named tests

1. `test_uinew_p03_chart_stage_renders_candles_from_backend_series_only`
2. `test_uinew_p03_timeframe_switching_discloses_resampled_or_incomplete_series`
3. `test_uinew_p03_chart_tokens_resolve_to_concrete_values_with_no_hardcoded_hex`
4. `test_uinew_p03_annotations_reject_order_entry_stop_target_and_size_fields`
5. `test_uinew_p03_seed_and_live_provenance_are_visually_distinguished`
6. `test_uinew_p03_chart_contains_no_execution_or_order_or_broker_or_account_control`
7. `test_uinew_p03_overlays_are_presentation_only_and_emit_no_signal_or_confidence`

Test #3 is the B-P03-1 spine. Test #4 is the T-1 spine for the new write path. Test #5 is the T-6 spine.

## 10. Mandatory evidence

- **(a)** Build identity at declared commit; SHA-256 per artifact (standing R-1).
- **(b)** Seven named tests DISPLAYED passing by name, verbose reporter.
- **(c) 🔴 T-1 grep CLEAN** — including annotation payload fields: `entry|stop_loss|take_profit|position_size|lot|volume_size|order`.
- **(d) 🔴 C-1 permanence grep CLEAN** over `components/terminal/`.
- **(e) 🔴 Extended field-provenance table** (B-P03-11).
- **(f) 🔴 Browser evidence at 1920×1080** (OBS-P01-5 — resolution now matters for chart density): (i) chart rendering candles with `live:simulated` labelled; (ii) a higher timeframe showing the resampled/incomplete disclosure; (iii) empty/no-data series rendering an honest state, not a blank canvas that reads as "flat market"; (iv) an annotation created and displayed; (v) **the logged-out redirect** discharging B-P03-6.
- **(g)** T-4 grep clean; `package.json` diff — `lightweight-charts` already present, **no new dependency**.
- **(h)** Sandbox safety; token purity (no ad-hoc hex — critical given canvas colours); secrets scan.
- **(i)** No-drift — Alembic `20260717_0037`; no new endpoint, table, or dependency.
- **(j)** Regression — Vitest **≥152f / 631t** no test lost; `pytest -q` **≥414**; `tsc -b` exit 0; `vite build` exit 0 with bundle delta against 660.64 kB (**OBS-5 — charting is the phase most likely to move this materially; disclose and justify**).
- **(k)** Doc 16 B-1…B-7, with particular attention to chart canvas palette conformance.
- **(l)** Doc 17 §17.8 Gates 1–4; SAL per B-P03-10.
- **(m)** Provenance per B-P03-7.
- **(n)** Local CI `LOCAL_CI_EXIT_CODE: 0` + sentinel, or disclosed `TD-090` waiver.

## 11. Acceptance criteria

Plan §W P03 row: *"TradingView candlestick chart renders at top-center; timeframes switch seamlessly; 100% tokenized canvas colors."*

Binding additions: token resolver implemented and tested (B-P03-1); timeframe resolution disclosed (B-P03-2); overlays presentation-only (B-P03-3); annotations carry no order fields (B-P03-4); seed/live provenance distinguished (B-P03-5); regression ≥152f/631t and ≥414.

## 12. Authorization

**`BUILD_ORDER_UI-NEW-P03` IS HEREBY ISSUED.** The DA is authorized to implement §2 IN-scope items only.

Resolve **B-P03-1** first — the chart cannot render compliant colours without it.

**Delivery will not be approved while CA-P02-1 (GA-167) remains open.**

**Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
