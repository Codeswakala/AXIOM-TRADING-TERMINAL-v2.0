# BUILD ORDER — UI-NEW-P02

**Market Watchlist Dock · Candle-Derived Market Telemetry · Instrument Selection · T-6 Provenance Discipline**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional Trading Terminal Transformation |
| Workstream | UI-NEW — Institutional Trading Terminal Rebuild |
| Phase | **UI-NEW-P02** |
| Preceding determination | `ITRGA_REVIEW_UI-NEW-P01_ATTEMPT3.md` — ✅ **APPROVED WITH OBSERVATIONS** |
| Approved plan | `UI-NEW_ENGINEERING_DESIGN_PLAN.md` · SHA-256 `8834aa91…` (ITRGA-verified) · §V-P02 as re-scoped by C-1 |
| Governing docs | Operator Directive §§18–20, 25–32; Plan §N (T-1…T-7), §V-P02, §W, §X; `17_INSTITUTIONAL_SECURITY_STANDARD.md`; Doc 16 Part XIV; `QUALITY_GATE_SPEC.md`; `REPOSITORY_PROVENANCE_PROTOCOL.md` §2 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend **414** · frontend **150f / 617t** · platform **1,031** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Populate the P01 left dock and right telemetry slot with **instrument discovery and honest market telemetry**. This phase introduces the terminal's first live data consumption. It computes no analytics and renders no order book.

**IN scope (Plan §V-P02, as re-scoped by C-1):**

1. **`TerminalWatchlistDock.tsx`** — multi-asset watchlist in the P01 left slot: symbol list across Forex and Crypto, last price, change, search/filter, and active-symbol selection that publishes to terminal state for P03 consumption.
2. **`TerminalSpreadTelemetry.tsx`** — right-dock telemetry over **genuinely available fields only** (see §3): tick frequency, session volume, feed lag, message counts, connection state.
3. **Active-symbol state** — selection propagated through terminal state; may reuse `operator_workspace_preferences` for last-selected symbol (presentation only) or remain in-memory. DA's choice, justified.
4. **`terminalWatchlistDepth.test.tsx`** + `uinew_p02_security_invariants.test.ts`.

**OUT of scope — do NOT build:**

- **Order book, depth ladder, bid, ask, or size rendering.** Permanently excluded by C-1 while the Gate is closed.
- P03 chart stage · P04 signal stream · P05 dock content · P06 audit.
- Any actuation (T-1); any external LLM (T-4); any new endpoint, table, migration, or dependency. Alembic locked at `20260717_0037`.
- Any fabricated price, spread, volume, or telemetry value (T-6).

---

## 2. 🔴 BINDING CONSTRAINT B-P02-1 — "Spread" has no backend source

**This is the defining constraint of the phase and it must be resolved in design, not discovered in implementation.**

I traced the data before issuing this order. The findings are Level I:

**The live tick payload** (`backend/app/market/live_service.py`) carries exactly:
```
type · channel · market_class · symbol · timeframe · open_time
open · high · low · close · volume · source · received_at
```

**`/api/v1/market/status`** (`LiveMarketStatsResponse`) carries:
```
running · auto_start · adapter · connected · market_class · symbol · symbols
timeframe · messages_received · persist_count · persist_errors
lag_ms · last_message_at · last_persisted_at · started_at
```

**There is no bid, no ask, and no spread field in either.** The only occurrence of `spread` anywhere in the backend is `backend/app/ml/economic/service.py` line 57 — a required **cost-model input** for economic validation, not market data.

**A bid-ask spread cannot be derived from OHLC candles.** High-minus-low is intraperiod range; close-minus-open is directional change. Neither is a spread. Labelling either as "spread" would be a T-6 violation of exactly the kind C-1 was raised to prevent — and it would be worse than the depth ladder, because a plausible-looking number invites reliance.

**Required of the DA, before implementation:**

- **(a)** Rename the component and its surfaced fields to what the data actually supports — e.g. `TerminalMarketTelemetry` rendering tick frequency (derivable from `messages_received` / `lag_ms`), session volume (`candle.volume`, nullable — handle the null honestly), intraperiod range (`high − low`, **labelled as range, never as spread**), feed lag, connection state; **or**
- **(b)** retain a spread field only if the DA identifies an actual bid/ask source I have not found, citing file and line; **or**
- **(c)** render a spread row in a permanent explicit `unavailable` state with the reason disclosed (`no bid/ask source — broker seam Gate-closed`).

Option (a) is what the platform can honestly support today. The DA selects and justifies; I do not dictate the architecture.

**Note for the record:** the P01 capture already renders `SPREAD: --`. That is honest today because the feed is idle. Once the feed runs, that field must not populate with a derived number — it must stay unavailable or be renamed.

---

## 3. Conditions carried from P01

- **B-P02-2 — CA-P01-3 (GA-167) must be closed before this phase's delivery is reviewed.** P02 is the first phase to genuinely exercise the displaced Tier-5 panel architecture. Owner: **Operator**.
- **B-P02-3 — CA-P01-2** — four debt descriptions restated verbatim from register v3.0.12 (`TD-005` is the design-token debt; `TD-UI-REACTROUTER-MODERATE` is an npm-audit advisory). Owner: **DA**.
- **B-P02-4 — CA-P01-1(iii)** — logged-out `/` redirect capture, outstanding from P01. Owner: **Operator**.
- **B-P02-5 — Provenance (OBS-P01-1).** Commit, annotated tag, and `git rev-parse --verify <tag>` **output** in evidence.
- **B-P02-6 — Single Active Phase.** P03–P06 remain unauthorized.
- **B-P02-7 — No security regression** (Doc 17 §17.11). Preserve: `dangerouslySetInnerHTML` = 0, `eval(` = 0, RBAC, ticket-authenticated WebSocket.
- **B-P02-8 — SAL declaration.** P02 consumes live market data; ITRGA assesses **SAL-2**, but the DA shall confirm against Doc 17 §4 given the data-consumption change.

---

## 4. Mandatory named tests

1. `test_uinew_p02_watchlist_dock_renders_multi_asset_symbols_and_selection`
2. `test_uinew_p02_active_symbol_selection_propagates_to_terminal_state`
3. `test_uinew_p02_telemetry_renders_only_backend_supported_fields`
4. `test_uinew_p02_no_bid_ask_or_depth_rendering_anywhere_in_terminal`
5. `test_uinew_p02_unavailable_and_stale_feed_states_render_explicitly_without_fabrication`
6. `test_uinew_p02_contains_no_execution_or_order_or_broker_or_account_control`

Test #3 is the B-P02-1 spine — it must assert that no rendered field lacks a backend source. Test #5 is the T-6 spine and must cover **null volume**, stale feed, and disconnect.

---

## 5. Mandatory evidence

- **(a)** Build identity at declared commit SHA; SHA-256 of every artifact (standing R-1 requirement).
- **(b)** Six named tests DISPLAYED passing by name, verbose reporter.
- **(c) 🔴 T-1 actuation grep CLEAN** — `buy|sell|place_order|submit_order|order_ticket|execute|connect-broker|broker|account_id|position|balance|margin|open_gate|allow_execution`.
- **(d) 🔴 C-1 permanence grep CLEAN** — `depth.?ladder|order.?book|orderbook|\bbid\b|\bask\b` over `frontend/src/components/terminal/`.
- **(e) 🔴 B-P02-1 field-provenance table** — every field rendered by both new components, mapped to its backend source field and endpoint. Any field without a source must be shown as permanently unavailable with the reason.
- **(f) 🔴 T-6 served-browser proof, 1920×1080 (OBS-P01-5)** — three states: **feed running** (real values, `live:simulated` labelled), **feed stopped/stale**, **null-volume symbol**. The running-feed capture is the critical one: it must show no fabricated spread.
- **(g)** T-4 external-LLM grep clean; `package.json` diff proving the four-package set unchanged.
- **(h)** Sandbox safety; token purity (no ad-hoc hex outside `tokens.css`); secrets scan.
- **(i)** No-drift — `alembic current` = `20260717_0037`; no new endpoint, table, or dependency.
- **(j)** Regression — Vitest **≥150f / 617t** no test lost; `pytest -q` **≥414**; `tsc -b` exit 0; `vite build` exit 0 with bundle delta against 650.02 kB.
- **(k)** Doc 16 B-1…**B-7** (B-7 unaddressed at P01 — OBS-P01-3).
- **(l)** Doc 17 §17.8 Gates 1–4; SAL declaration per B-P02-8.
- **(m)** Provenance per B-P02-5.
- **(n)** Local CI `LOCAL_CI_EXIT_CODE: 0` + sentinel, or disclosed `TD-090` waiver.

---

## 6. Acceptance criteria

Plan §W P02 row, as re-scoped: *"Multi-asset watchlist switches symbols instantly; telemetry renders live values with monospace tabular numbers."*

Binding additions: every rendered field traceable to a backend source (B-P02-1); no bid/ask/depth anywhere; unavailable and null states explicit; regression held at ≥150f/617t and ≥414.

---

## 7. Delivery Report

Per Directive §32 — all 21 elements, SHA-256 per artifact, one commit SHA cited consistently, debt stated against register v3.0.12 with `TD-AXIOM-DEV-CREDENTIAL-LITERALS` disclosed as an open Doc 11 §2 pre-certification blocker, and the §5(e) field-provenance table. The DA shall not state that the phase is approved.

---

## 8. Authorization

**`BUILD_ORDER_UI-NEW-P02` IS HEREBY ISSUED.** The DA is authorized to implement §1 IN-scope items only.

Resolve **B-P02-1** in design before writing the telemetry component — it determines what that component is permitted to display.

**Governance Gate remains CLOSED. Production remains NOT CERTIFIED. No order book, depth ladder, or bid/ask rendering may be introduced by this or any successor phase while the broker seam remains Gate-closed.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
