# ITRGA SEED OVERLAY SPEC (CORRECTED) — OV-V2-BE-11-002
`STATUS: FOR DA IMPLEMENTATION UPON OPERATOR GO — 2026-09-07 — SUPERSEDES OV-V2-BE-11-001 (BLOCKED)`
`Correction ledger: N-O19 (ITRGA-owned): spec prose enumerated around the accepted engine bytes;
law: seed specs enumerate engine-read contracts from the engine source, never from design prose.
OV-F1/OV-F2/OV-F3 each named and disarmed in this edition.`

## 0. Enumerated engine contract (source of truth = ACCEPTED pbr-1.0.0 bytes,
   as probed by the DA at Level I; pinned hashes below)
- `read_tolerance_seeds()` consumes rows where `seed_name == 'drift_tolerance'` (exact), and
  binds per FIELD via payload key `name`; chassis per row EXACTLY `{name, value, unit, citation}`.
- `read_staleness_seed()` consumes rows where `seed_name == 'generation_staleness'` (exact);
  payload carries `max_age_hours` + `citation`.
- Verdict law is STRUCTURAL: `within_tolerance` if delta ≤ tol; `drift_minor` if delta ≤ 2×tol;
  `drift_major` above; units are ABSOLUTE comparison units — no percent semantics exist.
- DA pre-delivery obligation (build gate, not a courtesy): re-run Probes A/B/C semantics against
  THIS payload on a scratch 0051 chain; deliver with the probe witness hash-pinned, or do not deliver.

## 1. Operator-approved payload (Exit (a); SINGLE revision id: `20260909_0052`;
   parent `20260909_0051`; exactly FIVE inserts, nothing else)
ROWS 1..4 — kind `seed`, seed_name `drift_tolerance`, one per compared field:
  {"name": "balance",          "value": "125.00", "unit": "USD", "citation": "operator seed"}
  {"name": "margin_used",      "value": "125.00", "unit": "USD", "citation": "operator seed"}
  {"name": "margin_available", "value": "125.00", "unit": "USD", "citation": "operator seed"}
  {"name": "unrealized_pl",    "value": "125.00", "unit": "USD", "citation": "operator seed"}
ROW 5 — kind `seed`, seed_name `generation_staleness`:
  {"max_age_hours": 48, "citation": "operator seed"}
Declared intent map (register): minor boundary 125.00 USD; major boundary 250.00 USD
(structural 2×; closest lawful form of the earlier percent intent under pbr-1.0.0).
DDL: none. Model: none. Engine bytes: none. Compver OFF. Triggers: none.

## 2. Coupons (small, exact; budget ~6–10; suite floor 1,155 + delta)
- gate pair inherits: current 0051 base lands exactly; one upgrade line 0051→0052.
- seed census: 5 rows; names/payloads/units/citations enumerated exact (values quoted > retyped).
- armed flips: `comparison_state` becomes armed with tolerance census 4;
  generation: basis age 23h (armed fail-check relative?? — restated: age ≤ 48 → not stale for
  generation); age 49h → `basis_stale` typed refusal.
- drift arms: synthetic deltas pass the 125/250 law three ways (within / minor / major);
  a delta 0.00 → within tolerance exact boundary arm included (tol-inclusive-by-design).
- everything else stays EMPTY-FORCED (no other rows exist; assert).
- downgrade: delete the five rows by (seed_name, payload->>name) content-keyed, count-asserted.

## 3. Post-apply (micro): ACC → INT → APPLY (one line) → P-4 (seeds=5; census 78/69/13 unchanged;
compver 13; pbr hash 4c243435…178b TRUE UNCHANGED) → suite seal → FIRST-READ micro:
drift endpoint comparison_state ARMED; generation still mode-armed 403 on this box
(RESEARCH deployment); flip-to-PAPER remains an operator register act, separately elected.

## 4. Identity pins carried (three-layer law)
- pbr engine expected-hash (far-fetched to change; assert-not-mutate):
  `4c243435103a149830fd448d4f84a931af7543aa08b901299ebb5d1a27ff178b`
- supersedes-and-closes items: OV-F1 (exact seed_names + name-binding chassis),
  OV-F2 (absolute-unit intent map; structural 2× accepted), OV-F3 (single id elected:
  `20260909_0052`).
