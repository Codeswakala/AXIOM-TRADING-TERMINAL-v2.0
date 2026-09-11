# ITRGA BUILD ORDER — BO-V2-BE-11-001
`STATUS: FOR DA EXECUTION UPON OPERATOR SEAL — 2026-09-06`
`Gates: REQ-V2-BE-11-001 ADOPTED · DR-V2-BE-11-001 SEALED · A-2026-09-06 applied on disk`

## 0. Register note (operator inputs, PENDING — fail-closed posture)
Three values belong to the Operator and were not supplied before this BO:
`(i)` drift tolerance seeds {(name,value,unit,citation) ×N},
`(ii)` REFUSE-GENERATION staleness seed `max_age_hours`,
`(iii)` final bridge permission-enum naming (two lawful candidates on file).
BO law: the band BUILDS COMPLETE with these slots EMPTY-FORCED:
- drift arm ⇒ `uncomputable` (refuse-to-compare) until tolerance seeds exist;
- intent GENERATION ⇒ typed refusal `basis_staleness_threshold_unseeded` until
  `max_age_hours` is seeded (fresh-read READS unaffected);
- permission naming ⇒ DA registers the proposed enum `v2.paper_bridge.intent.write /
  .evaluate.write / .ledger.read / .drift.read`, with operator confirmation or
  substitution captured at the BO-SEAL review (naming is a one-line seed/pin; not
  an architectural gate). Any operator value furnished LATER arrives by seeded
  overlay migration (no model/DDL edits) — these are seeds, not constants.

## 1. Deliverables (all-or-nothing band — no partial claims)
D-1 Package `app/v2/paper_bridge/` with four modules:
   `contract.py` (closed enums: gateway decision {accept_with_notes, deferred,
   refused_under_policy}; refusal reasons {basis_unavailable, basis_stale,
   reference_price_uncited, duplicate_intent, basis_staleness_threshold_unseeded};
   drift verdicts {within_tolerance, drift_minor, drift_major, uncomputable};
   engine version pbr-1.0.0), 2dp decimal quantization law (mirrors D-B10-2DP),
   and BANNED-VERB payloads guarded by the wording law (state nouns only);
   `engine.py` (pure computation; basis pinned by sync_run_id read ONCE at entry —
   consistency ARM; money-units-only sizing while positions absent; citation price
   consumed as INPUT per D-B11-CITE; rolled digest over (basis_sync_run_id,
   intent_payload, pxs/prg/pbr versions));
   `api.py` (POST intents, POST evaluate, GET ledger, GET drift; writers demand
   mode=="PAPER" per D-B11-MODE with 4xx on LIVE; marker convention D-1);
   `__init__.py` (package seam + boundary-scan surface).
D-2 ONE migration (00xx, ascended after fielded 20260908_0050):
   +1 table `v2_paper_bridge_drift_run` (reconcile_run precedent; guard-pair
   triggers ⇒ triggers 76→78), +1 compver row `paper_bridge_engine | pbr-1.0.0 |
   <rolled hash>`, +4 permission-enum seeds (per §0 naming), +tolerance/staleness
   seed SLOTS standing EMPTY-FORCED (census re-tattoo in the same revision; exactly
   ONE upgrade line).
D-3 Coupons L-1…L-10 per DR Q6, ~35–45 tests (suite floor 1,121 + band);
   includes: ×3 determinism on pinned basis fixture + citation-priced intent
   (per-world law N-O13); full fail-closed battery incl. staleness-refusal and
   refusal-on-unseeded-threshold; idempotency duplicate arm; drift 4-verdict arms
   with crafted ledgers; DDL identifier verb-scan (D-B11-NAMING) + payload verb-scan
   (D-B10-SCAN extended); extended banned-import scan on the bridge package
   (no providers / no MT5 / no terminal); N3 wall pair byte-unchanged PLUS new
   wall-law test (no domain imports bridge; bridge imports projections/engines only);
   RBAC 401/403 battery; migration census/tattoo tests (CENSU-computed triggers==78).
D-4 Evidence pack in `docs/evidence/` (V2_BE-11_* family): basis-pin transcript,
   ×3 digest law output, fail-closed battery log, drift-arm matrix, wall-scan logs.
D-5 DELIVERY REPORT → my acceptance review → integration sequence, then the
   fielded apply + first-read witness, closing as BE-10's won.

## 2. Standing laws bound into this BO (cite, don't restate)
Investor-only posture · no-plaintext-secret · three-layer enumeration · transcript
codec sovereignty · file-invoked act scripts · ASCII console · interpreter pretense
check (N-O12) · per-world digest law (N-O13) · full-hash diagnostics · register-of-
record re-issue (N-O11) · C-2 clean-run evidence · D-1/DECISION prefix · D-2 PAPER
writer mode · N3 walls.

## 3. Exit criteria (binary)
All L-coupons pass under (.venv); band evidence verified; DELIVERY filed; census
counts match exactly (triggers 78, perms 65+4=69, compver 13+ tables per revision
upgrade SQL); zero provider order-type strings anywhere; fill-sim absent (no
dormant scaffolding — dead code is a substitution surface).
