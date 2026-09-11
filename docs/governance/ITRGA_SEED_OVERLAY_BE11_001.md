# ITRGA SEED OVERLAY SPEC — OV-V2-BE-11-001
`STATUS: FOR DA IMPLEMENTATION UPON OPERATOR GO — 2026-09-07`
`Citizenship: a mini-act within the BE-11 register (closeout stands OPERATING at 0051;
this overlay is the BO §0 "seed slots" consumer — data rows only, zero DDL/model edits).`

## Operator-approved payload (verbatim; citation = operator seed)
Revision id proposal: `20260909_0052` · Parent: `20260909_0051` · counted items exactly:

ROW 1 — table `v2_paper_bridge_drift_run`, kind `seed`:
  seed_name = "drift_tolerance.minor"
  payload = {"value": 1.0, "unit": "percent_of_compared_magnitude_2dp", "citation": "operator_seed"}
  data_class "simulated" · actor/operator as register act identity · mode "PAPER"

ROW 2 — kind `seed`:
  seed_name = "drift_tolerance.major"
  payload = {"value": 2.5, "unit": "percent_of_compared_magnitude_2dp", "citation": "operator_seed"}

ROW 3 — kind `seed`:
  seed_name = "generation_staleness.max_age_hours"
  payload = {"value": 48, "unit": "hours", "citation": "operator_seed"}

NO further rows. NO permission changes (enum confirmed as-shipped: v2.paper_bridge.intent.write,
evaluate.write, ledger.read, drift.read — adopted without substitution; the overlay MIGRATION takes
no action on the enum; the confirmation is register-only).

## Lawful shape (DA obligations, sourced from BO/ACC law)
- ONE migration, one upgrade line `20260909_0051 -> 20260912_0052` (internal id family continues
  monotonic); exactly THREE INSERT statements; zero CREATE/ALTER/DROP.
- CHECK-conformance guaranteed a priori (all three rows carry kind seed + seed_name + simulated).
- Determinism: values fixed at authoring; uuid4 for ids is lawful (not part of the digested world).
- Coupons needed: +gate pair (drift-gate 0051→0052 line) + overlay semantic tests:
  (a) exact 3 rows landed, kinds/names/values/units/citations exact;
  (b) engine post-overlay: generation refusal changes ONLY for bases newer than 48h
      (test: basis 23h → armed path; basis 49h → basis_stale refusal);
  (c) drift armed-state flips (refuse_to_compare_unseeded → able-to-compare; seed census = 2);
  (d) EMPTY-FORCE assertion for the rest (no other rows touched).
  Budget ~6-10 tests; suite floor moves 1155 → (1155 + delta, small).
- Downgrade: deletes the 3 seed rows by seed_name (content-based, no destructure).

## After delivery: ACC (micro), INT (micro), APPLY (one line), P-4 (seeds=3; census unchanged
78/69/13; compver 13), suite seal, FIRST-READ micro-witness:
expect drift endpoint to report comparison_state ARMED + seed census 2; intent generation now
arms when a fresh-enough basis exists AND mode==PAPER (mode remains RESEARCH on the box —
operator elects the mode flip as its own register act at that time).

**We don't guess. We prove.**
