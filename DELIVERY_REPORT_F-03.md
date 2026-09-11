# DELIVERY REPORT — BO-F-03
## Intelligence Presentation (all five families + governed generation)

| Item | Value |
|------|-------|
| Build Order | `BO-F-03` (Operator directive 2026-08-21: "authorized") |
| Predecessors | F-02 CLOSED (ITRGA 2026-08-21) · B-04 (generation endpoints, no prior frontend caller) |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 34) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-03 §2: F-03.1 generation client, F-03.2 five-family
rendering, F-03.3 governed generation surface, F-03.4 non-actuation + honesty.
§3 exclusions honored: no backend change (pure consumer of B-04), no ML
generation/promotion, no signal/alert emission, no background generation
(on-request only), no design-language weakening, no repo publication. §6
allowed files plus one disclosed addition (D1). Register rows ship in the
patch per the standing append-only convention (BO §9 binding).

## 2. What changed (files + SHAs + chain position)

Patch `f03.patch` — **chain position 34**, 5 files (3 modified + 2 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–33; post-apply cmp
5/5; register hunk proven to apply onto a drifted (baseline-era) register with
the code at chain-33. Patch sha256:
`cc7554df691740205280449d4773ec3bdcfe8ed0f485e68d379cf7dda28d2db6`.

| File | Change |
|---|---|
| `frontend/src/api/client.ts` | Five governed generation functions + typed request schemas + `IntelligenceGenerationError` (structured 4xx/insufficient-data mapping); optional `notes`/`limitations` read fields on the correlation/regime/signal-validation types (B-04 read-surface fields, rendered verbatim) |
| `frontend/src/components/terminal/TerminalIntelligenceCards.tsx` | Five family tabs (scenario + portfolio-risk added); per-card uncertainty/sample/limitations/data-class/lineage/framing rows; the governed generation surface (per-family triggers, real-window derivation, honest notices) |
| `frontend/src/components/terminal/TerminalMultiPane.css` | F-03 styles (generation panel, scenario/portfolio-risk cards, framing lines) — pure token consumption (D1) |
| `frontend/src/test/f03_intelligence_generation.test.tsx` | **New** — 13 tests (§7) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows + F-02 CLOSED status row — pure-addition hunk in the patch (§9) |

## 3. Generation client description (5 functions + schemas)

`createCorrelationReport`, `createRegimeReport`, `createScenarioReport`,
`createPortfolioRiskReport`, `createSignalValidationReport` — each POSTs the
exact B-04 request schema with Bearer JWT and returns the persisted report.
The structured B-04 422 (`{error_code, detail, insufficient_data}`) maps to
`IntelligenceGenerationError` carrying `status`, `errorCode`, and
`insufficientData` — an honest, typed insufficient-data signal, never a
fabricated report. **Naming deviation disclosed (D2):** the functions are
named `create*Report`, not `generate*` — the standing UI-006-P06 static pin
forbids `generatesignal`/`generatescenario` tokens in frontend source
(client-side generation would bypass the gated backend). The pin is unchanged
and still passes; the functions are the governed server-side B-04 callers.

## 4. Five-family rendering description

All five families now render with the full honesty discipline:

| Family | Card contents |
|---|---|
| Correlation | r + Fisher-z CI + N + `data-class` + report-hash prefix + framing |
| Regime | label + confidence band + symbol/TF + N + `data-class` + hash + framing |
| Scenario | name + hypothetical return + assumptions JSON + symbol/TF + N + limitations + `data-class` + hash + framing |
| Portfolio-risk | max drawdown + realized volatility + stress loss + symbol/TF + N + limitations + `data-class` + hash + framing |
| Signal-validation | Wilson-interval metrics + sample N + outcome-data status (verbatim) + framing |

`data-class` is parsed from the server-appended `notes` label; every card
carries the research-only framing: *"Research artifact only — not a signal,
not causation, not a prediction, not financial advice."* Server-values-only:
no client-side metric recomputation (pinned by test).

## 5. Governed generation surface + insufficient-data handling

A per-family Generate trigger under "GOVERNED GENERATION · B-04 ·
RESEARCH-ARTIFACT CREATION ONLY". The generation window is derived from the
**freshest persisted candle of the active series** (30-day span, H1 — the
corpus timeframe, D3): never fabricated — if no series exists, the triggers
are disabled with an honest no-window notice. Success persists the report and
re-reads the family (refresh tick). The structured insufficient-data 422
renders as *"Insufficient data: {error_code} — nothing fabricated."* Errors
and 401s surface as honest notices. On-request only; no background generation.

## 6. Screenshot evidence (Level-I, `docs/evidence/f03/`)

| Capture | File | Result |
|---|---|---|
| Generation surface | `f03_generation_surface.png` | Framing + resolved real window (BTCUSD H1, 2026-06-30 → 2026-07-31) |
| Scenario card | `f03_scenario_card.png` | UI-generated over real data: persisted `be653ac8…`, hypothetical return −15.00%, `data-class: historical:real` |
| Portfolio-risk card | `f03_portfolio_card.png` | UI-generated: drawdown −6.20% · vol 0.35% · stress −1.01%, `data-class: historical:real` |
| Correlation card | `f03_correlation_card.png` | UI-generated: BTCUSD⇄ETHUSD r=0.877, CI [0.86, 0.89], `data-class: historical:real` |
| Insufficient-data | `f03_insufficient.png` | Honest structured-422 notice: `SIGNAL_VALIDATION_EMPTY_SCOPE — nothing fabricated` |
| Probe log | `f03_capture_log.txt` | All statuses, window, framing, no-actuation scan (violations: none) |

Backend log for the capture window: three POST 201s with
`intelligence:*_report_generated` pipeline events and the signal-validation
POST 422 — the governed generation round-trips are real. Capture fixture
disclosed (same as F-02): the real corpus bars under the terminal's
BTCUSD/ETHUSD symbol keys; local dev DB only; honest labels preserved.

## 7. Non-actuation + no-fabrication evidence

- No-actuation scan (test + browser): zero occurrences of
  buy/sell/order/broker/execution/account across the intelligence surface.
- No fabrication: no-series → generation disabled with an honest notice;
  insufficient-data → typed error → honest notice; loading shows the existing
  skeleton; metrics are rendered verbatim from the persisted reports.
- No client-side recomputation (pinned): the scenario return is rendered
  directly from the server's `hypothetical_return` value.

## 8. Test evidence (executed)

- Workspace full frontend suite: **933 passed / 176 files** (920 floor + 13
  new), 175.48s, exit 0 — `f03_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0 — `f03_tsc.log`.
- Production build: green (chunk-size warning pre-existing).
- Clone-side (gold standard): pristine `34f4c62` → 34 elements → `npm ci` →
  tsc clean → **933 passed** — `f03_cloneside_vitest.log`.

## 9. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `TerminalMultiPane.css` edited — the dock stylesheet home (not named in §6) | Same accepted class as F-00/F-01/F-02; pure token consumption; governance scans pass. |
| D2 | Generation functions named `create*Report` (not `generate*`) | The UI-006-P06 static pin forbids `generatesignal`/`generatescenario` tokens in frontend source (client-side generation would bypass the gated backend). The pin is unchanged and the functions are the governed server-side B-04 callers. |
| D3 | Fixed H1 generation timeframe + deterministic correlation partner | The corpus timeframe (H1) and a deterministic partner table (BTCUSD↔ETHUSD; forex↔EURUSD/GBPUSD) — disclosed; the window itself is real-data-derived. |
| D4 | Correlation r over the 30-day window (0.877) differs from the full-corpus figure (0.7321) | Both are server-computed over their respective windows — window-scoped honesty, not a discrepancy. |

## 10. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

The patch's register hunk is a zero-context pure-addition (11 appended lines):
TD-F02-UNIT-STATUS (CLOSED — APPROVED WITH OBSERVATIONS), TD-F03-UNIT (this
unit). Verified to apply onto the chain-33 register (cmp byte-identical) AND
onto a baseline-era drifted register (DRIFT-PROOF OK).

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/f03_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f03_transmission/f03.patch.txt` | `cc7554df691740205280449d4773ec3bdcfe8ed0f485e68d379cf7dda28d2db6` |
| 2 | `f03_transmission/f03_applycheck_transcript.txt` | `cc97ab5b1ce0797d821add6d83661c323f72798005e850e77feb1222e4c1336c` |
| 3 | `f03_transmission/f03_capture_log.txt` | `24ce6e8a31bae6f2d613488eb67aef7437e7dd6bafad53f4cb15f660dee541f2` |
| 4 | `f03_transmission/f03_cloneside_vitest.log.txt` | `2c81b4c0474b90e72d2df32405f6c44a61a65bb7b5a07af98524e2f1afc35bff` |
| 5 | `f03_transmission/f03_correlation_card.png` | `34a851c4ff1b9831d4e4a56a2234e2f4101e0859c362de0c0c55f8035ef45663` |
| 6 | `f03_transmission/f03_generation_surface.png` | `9d69416e82dc0964549ddbea881703615eee3d330cca575798cab1e1a12925f8` |
| 7 | `f03_transmission/f03_insufficient.png` | `c30f08a523a1ee9bb4555a0b9a509979cd07997110188ee0d3dcc6b73149ce84` |
| 8 | `f03_transmission/f03_portfolio_card.png` | `efa1d83d47e9d3d995db2d62ef462b1eb7bf09a235166f32891f837470b6aefa` |
| 9 | `f03_transmission/f03_scenario_card.png` | `693d0e714a476b092c26850cc72807e2be9855c1c56c78dda577d89224a02f52` |
| 10 | `f03_transmission/f03_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 11 | `f03_transmission/f03_vitest_fullsuite.log.txt` | `9154a54cf4452973bf165073064763ec02a5f2c45bfa49c11c59ddeabc747768` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
