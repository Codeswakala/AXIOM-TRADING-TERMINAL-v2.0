# ITRGA DESIGN REVIEW — DR-V2-BE-11-001
`STATÁ: FOR OPERATOR REVIEW — 2026-09-06 — registers REQ-V2-BE-11-001 (ADOPTED, all sections)`

## REGISTER NOTE
Band id BE-11 · roadmap re-enumeration A-2026-09-06 ADOPTED (execution → BE-12; AI → BE-13).
DR does not amend requirement law; it registers design against it.

---

## Q1. What problem in current production behavior/mapping is NOT solved?
- The BE-8 paper machinery is a perfect lock with no key: `prg-1.0.0` (risk gateway)
  and `pxs-1.0.0` (execution simulator) exist as verified compver components, and all
  eight `v2_paper_*` tables stand refugee-empty — because no real basis ever arrived.
- BE-9 now brings live practice-book truth (balances; positions when held; fills when
  priced); BE-10 supplies canonical vocabulary; there is no lawful join between them.
- EVIDENCE (E-B11-1, executed as this DR's first station, fielded DB, read-only):
  (a) V1 `candles` = 0 rows; (b) all v2 md bar/series families (`v2_md_series`,
  `v2_market_context_report`, `v2_chart_intelligence_report`, `market_series_metadata`,
  `dataset_snapshots`) = 0 rows each; (c) `v2_broker_fill` = 1 row of tx_type `2`
  (MT5 DEAL_BALANCE; instrument '', units 0.0, price 0.0 — a deposit, not a price),
  `v2_broker_position` = 0 rows, `v2_broker_balance` = 10000.0/0.0/10000.0/0.0
  (supersession-pinned, two rows); (d) all `v2_paper_*` = 0 rows.
  **Consequence (RESOLUTION-GRADE): NO LAWFUL PLATFORM PRICE BASIS EXISTS TODAY** —
  REQ R-1.4's fail-closed default fires by evidence, not by speculation.

## Q2. What would a senior debugger see at 2am?
- The basis contract is exactly `v2_broker_balance` snapshot fields + optional
  positions/prices from later syncs; with positions today at [], sizing fields reduce
  to balance, margin_used/available, unrealized_pl — true, and enough for risk framing
  in units-of-money, NOT in units-of-instrument.
- When an intent asserts an instrument and side, **no platform-side price may be
  conjured**; the lawful nucleus: reference_price arrives **BY OPERATOR CITATION**
  per intent (`{value, currency_unit, cited_source, cited_at}`, auditable), and the
  engine treats it as INPUT, never platform truth. (Design law, named D-B11-CITE.)
- The N3 wall live-tests (`test_n3_paper_wall_from_broker_side` /
  `_from_paper_side`) forbid cross-imports between `app/v2/broker/` and
  `app/v2/paper_trading/`. THEREFORE the bridge occupies NEITHER domain: a third
  package `app/v2/paper_bridge/` imports BOTH domains' projections/engines;
  neither domain may import the bridge or each other. Wall tests stay byte-still;
  boundary-scan law GAINS a bridge clause. (D-B11-TOPO.)
- All writers of this beast run in `PAPER` mode (BE-8 D-2 law: writers demand
  mode == "PAPER"); the bridge knows no other mode. (D-B11-MODE.)

## Q3. What registration does the REQ demand and what does the system already hold?
- Digest canon (R-3.1): digest over (basis sync_run_id, intent payload,
  pxs/prg/bridge versions) — pxs/prg already versioned as compver rows;
  bridge joins as ONE new component, `paper_bridge_engine`, version pbr-1.0.0,
  rolling-hashed like its neighbors. Determinism is PER-WORLD (N-O13 law; never
  re-assert cross-env equality).
- Reuse law (R-2): pxs/prg bodies consumed AS-IS. Any byte drift trips the
  standing compver hash law — this is a feature.
- Fail-closed set (R-3.2): (i) basis absent (no complete sync_run) → typed refusal
  `basis_unavailable`; (ii) basis stale beyond seeded max_age_hours (Operator value
  at BO) → REFUSE-GENERATION arm (stale basis may still READ with banner, never
  spawn ledger entries); (iii) citation price absent for an intent → typed refusal
  `reference_price_uncited`; (iv) duplicate `(account_id, idempotency_key)` →
  typed refusal `duplicate_intent` (schema-level uq already stands, BE-8 law;
  the API turns the collision into the typed refusal).
- Gateway vocabulary (R-3.3): closed enum `accept_with_notes | deferred |
  refused_under_policy`; refusal reasons closed sub-enum; naming law extends to
  DDL identifiers — one test scanning table/column identifiers for broker-order
  verbs (D-B11-NAMING on top of D-B10-SCAN).
- Drift surface (R-3.4): bridge reads paper-ledger derivations vs broker projection;
  comparison is a DIFFERENT CLASS than BE-9's reconcile (two independent simulations
  of the same world — tolerance is not heresy here). Tolerances live as SEEDED,
  audited inputs: `{name, value, unit, citation}` (BE-7 citation chassis);
  DEFAULT VALUES ARE OPERATOR INPUTS AT BO; the band ships with seeds seeded
  empty-forced (refuse-to-compare until tolerances seeded — drift arm does not
  quietly guess). Verdict enum: `within_tolerance | drift_minor | drift_major |
  uncomputable` (closed; 2dp arithmetic discipline from BE-10 D-2/D-3 carries).
- ONE LINEAGE TABLE QUESTION (as charged by the DA): drift runs recorded on the
  BE-9 `reconcile_run` precedent (C-2: clean runs must be evidenced) →
  `v2_paper_bridge_drift_run` gets its own table (one only; census delta +1 table,
  +1 compver row, +indexes examinable in BO).
- Fill-simulation: DEFERRED by E-B11-1. Register note: DEFERRAL IS NON-REVIVAL —
  its revival requires a future REQ amendment with its own price-basis evidence.

## Q4. What architecture pattern does the system already use for this?
- Projection-in, state-noun-out (BE-9); computation-versioned plan with
  compver census (BE-10); citation-chassis inputs (BE-7/BE-8); typed refusals
  and degraded banners (platform law); N3 wall + scan-suite architecture
  (L-8-class); rolling hash canon; registration-first test discipline (L-1..L-10
  all carry).

## Q5. Failure exploration
- Basis present but its sync_run superseded mid-request → snapshot pinned by
  sync_run_id at request start (consistency ARM).
- Balances present, positions absent (today) → ledger funds in money-units only;
  instrument-exposure checks gracefully `deferred` with notes, not failure.
- Citation price cited but wildly inconsistent with any later broker-derived price
  (when one exists) → drift arm will find it; no pre-judgment at intent time.
- Operator attempts POST with mode == "LIVE" → 4xx refusal (D-B11-MODE test).
- Alembic: ascended head 00xx, single migration, touched-object census re-tattoo
  (76 triggers baseline; +permission enum delta expected minimal:
  `v2.paper_bridge.intent.write`, `.evaluate.write`, `.ledger.read`, `.drift.read`
  — final enum BO law).

## Q6. Test coupon plan (verifiable or no-ship)
- L-1: pbr-1.0.0 engine tuple pinning + compver mutation subject.
- L-2: end-to-end pen→paper intentions: fixed patched clock, fixed basis fixture
  (sync_run_id pinned), one citation-priced intent → gateway decision tuple ×3
  identical; digest law ride-along (determinism arm; ×3 within one world; the
  world's requirements per N-O13).
- L-3a..: fail-closed battery: basis_unavailable / fresh-read-but-stale-for-generation
  / reference_price_uncited / duplicate_intent typed-refusal pins, distinct statuses.
- L-4: gateway vocabulary pins incl. refusal-reason closed-set; banner emission arm
  for degraded-but-readable; staleness triple (`fresh/stale/unavailable`) carried
  verbatim from D-B02-COMP staleness law.
- L-5: drift arms ×4 (within / minor / major / uncomputable) on crafted ledgers;
  refusal-to-compare until tolerances seeded.
- L-7-scan: D-B11-NAMING (identifier verbs) + D-B10-SCAN (response-text verbs)
  + extended banned-import law (bridge package must not import providers/MT5/terminal).
- L-8: N3 wall tests byte-unchanged; NEW wall law test: neither broker nor paper
  domain imports paper_bridge; bridge imports contain only projection/engine modules.
- L-9: RBAC positive/negative on all four permission classes; 401/403 pins.
- L-10: order matters law — ascended revision == census consistency (triggers index
  of 76 baseline plus exactly the bridge's own interface).
- Budget: ~35–45 tests non-binding (DA early sizing); suite floor 1,121 + additions.

## Findings ledger
- E-B11-1 (evidence station): all four doors of price basis EMPTY on the fielded DB;
  fill-sim deferred by evidence (register: revival needs future REQ amendment).
- Register baseline–DA inventory divergence logged (candles 0 here vs "109,326" in an
  earlier inventory note — different DB lineage; no action; documentation debt absorbed).
- Carryover note: BE-9 requester-side secret-hash disposal confirmation still
  pending from operator (non-gating, informational).

## PROCESSED UNDER
DR template law D-BO13 (questions 1–6 = this review); no language other than
registered design commitments; SEAL of decision = operator ruling on this document.
