# ITRGA ACCEPTANCE DECISION — ACC-V2-BE-11-001
`STATUS: EVIDENCE-GRADE VERDICT — 2026-09-06 (fielded apply pending, as BE-10 closed)`

**VERDICT: ACCEPTED — BE-11 DELIVERY ACCEPTED · INTEGRATION/PLACE-ON-FIELD STAGE NEXT**

## §0 — Register line tostand
`BE-11: APPLIED? NO — DELIVERY ACCEPTED 2026-09-06; fielding pending INT + APPLY + FIRST-READ`
(the cold facts: DA test chains only carry 0051 so far — per D-5 of the DER, fielded
apply follows acceptance, closing as BE-10's won).

## §1 — Evidence verification transcript (revealed, not asserted)
1. **FLIGHT-CHECK (hashes I recomputed on the pack, all four artifacts — bit-match
   to the DER §5 table):
   - TESTRUN `465f09fbf2…91a01d` == reported. SOURCE `ec29cdd733…16f1d96` == reported.
   - FAILFIRST `de74b87f28…53b2bb` == reported. MD5s equal likewise.**
2. **Suite gossip read from the transcript itself: `1155 passed, 2 warnings in 515.76s`
   — warnings pre-existing in unrelated module (test_b_audit_concurrency + the
   pytest.global-marks family; carried, already registered).**
3. **Battery-shaped couriers, all present and PASSED (naming engine 18 / walls 10 /
   migration 6 = 34, inside the ~35–45 band):**
   - L-1 tuple pin (`test_l1_engine_tuple_pinned`) · L-2 ×3 determinism + digest-moves-on-change ·
     L-3 five-reason closure (unavailable/threshold-unseeded/stale/uncited/policy-state) ·
     L-5 all four verdict arms + refuse-to-compare + malformed-seed + unseeded-field ·
     seed-slots-empty-forced + overlay-arms · basis-pinned newest-complete · closed enums.
   - L-7 verb scans (identifiers + payloads) · L-7 banned-import · **L-8 wall pair
     byte-unchanged (sha-pinned) + new wall law + allow-list** · L-9 RBAC 401/403 ×4 ·
     L-10 census tattoo + EMPTY-FORCED + guard verbatim + downgrade exact + fill-sim-absent scan.
4. **Fail-first witness: genuine import-fan failure (`ModuleNotFoundError` on engine.py
   stashed) — the test graft currently proves invocation (FA-2-type honest pause).**
5. **Census claims independently re-derived from the migration source itself:**
   76 triggers +2 guard pair = **78**; 65 perms +4 seeds = **69**; 12 compver +1
   `paper_bridge_engine|pbr-1.0.0` = **13**; exactly ONE upgrade line (single
   `op.create_table` etc.); the tattoo test enforces the same constants.
6. **The three-layer pin law holds end-to-end:** contract enums enumerated exactly the
   BO sets (3 decisions / 5 refusal reasons incl. `basis_staleness_threshold_unseeded` /
   4 drift verdicts); migration pins (revision/down_revision; guard brotherhood;
   compver ROLLING hash computed from landed bytes at apply time — DEL §4.4
   acknowledges the act-time recompute is the true gate; PBR hash claimed
   `4c243435…178b` measured post-suite) — nothing re-typed from prose.

## §2 — Register acts and honest notes (adopted into the ledger)
- **N-R1 (concurred):** seed-slot storage ruling — two row KINDS in the single
  C-2-lineage table (`drift_run` | `seed`), iff-CHECKs disjoint both directions;
  future operator VALUES arrive as `seed`-kind rows via overlay INSERTs. Reviewed the
  CHECK set (`verdict iff drift_run`, `seed_name ⇒ seed`, `data_class simulated`) —
  construct is lawful, no schema rework will be needed at seeding time.
- **N-R2 (concurred):** bridge intents reuse the standing BE-8 `V2PaperOrderIntent`
  (record NOUN, snapshot_ref `bridge-basis:<sync_run_id>`) — the BE-8 idempotency uq
  does R-3.5 at schema; the banned V1 `OrderIntent` shape remains import-scanned out.
- **N-R3 (informational):** permission enum registered as proposed
  (`v2.paper_bridge.*`; trailing-dot law kept it out of the marker set cleanly) —
  operator confirmation/substitution revised to a BO-SEAL one-line pin; no courier
  rides on it.
- **N-R4 (accounting note):** fielded head next = `20260909_0051`; fielded suite
  floor post-apply = **1,155** (1,121 + 34, the DA-chain count the INT packet
  re-witnesses on the integration lineage before any fielded byte moves).
- Date-basis: today's registry date 2026-09-06; migration id `20260909_0051`
  continues the monotonic family — lawful under the revision-dating precedent.

## §3 — What the band includes (truthful completeness)
Empty-forced by law: drift `uncomputable` until tolerance seeds; generation refuses
`basis_staleness_threshold_unseeded` until `max_age_hours` seeded. That IS the
shipped state — incomplete by design and honest about it, as the BO ruled.

## §4 — Grants (none beyond REQ/DR scope) and next stations
Next stations, in BE-10's proven order: **(1) INT-PACKET** (integration verify on a
scratch chain risen to 0050: apply 0051 → tattoo/census/wall pins + seeded-overlay
arm proof on scratch only); **(2) APPLY act** against the fielded file; **(3) suite
seal under (.venv)**; **(4) FIRST-READ witness** (expect empty-but-typed: reads
lawful, generation refused-until-seeded — the band's truth-to-self). On all four:
register line advances to `OPERATING`.

**We don't guess. We prove.**
