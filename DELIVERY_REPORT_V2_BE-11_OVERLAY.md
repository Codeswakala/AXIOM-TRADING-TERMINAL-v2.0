# DELIVERY REPORT — BE-11 SEED OVERLAY (OV-V2-BE-11-002, EXIT (a))
# AXIOM-V2-BE-11-OV-DR-001 · v1.0.0 · 2026-09-07
# Implements: ITRGA-SEED-OVERLAY-BE11-002 (filed md5 `14a12fbf88e3e450d0bc88c6e4ed1353` ·
#   sha256 `5d58403da4efca9fcb61c115ec7bf321ca0e9b1fbbb05b84eeafbd83ee37186a`),
#   superseding OV-V2-BE-11-001 (BLOCKED at DA-OVREV-001; OV-F1/F2/F3 disarmed in the 002 edition).
# Author: Replacement Development Authority (DA). This report is a SUBMISSION, not a ruling.
# Awaiting: micro-ACC per OV-002 §3. The console apply is a separate act; NOT performed.

---

## §0 — What this delivery is, and the one condition it stood on

The overlay is the BO-V2-BE-11-001 §0 seed-slot consumer, Exit (a) of
DA-OVREV-001: **data rows only** — the Operator's values re-cut to the
chassis the accepted engine actually reads. OV-002 §0 made the build gate
explicit: *probe THIS payload against the accepted bytes on a scratch 0051
chain, deliver with the probe witness hash-pinned, or do not deliver.*

**The gate was run FIRST and PASSED** (evidence
`docs/evidence/V2_BE-11_OV2_BUILDGATE_PROBE.txt`, md5
`42999a6b0fad0b8f62d34cead5910bc7`, sha256 `58eeae83…b696`):

```
G-0 engine hash assert (unchanged): 4c243435103a1498... OK
G-1 five spec-verbatim rows landed CHECK-clean: 5
G-2 read_tolerance_seeds() -> 4 · read_staleness_seed() -> 48.0
G-3 comparison_state -> armed
G-4 0.00/125.00 within · 125.01/250.00 minor · 250.01 major (all OK)
G-4b all four seeded fields individually resolvable
G-5 basis 23h -> accept_with_notes · 49h -> typed basis_stale
```

The N-O19 lesson is structural now: this payload was enumerated FROM the
engine source, and the probe proved it LIVE — not schema-conformant, LIVE.

## §1 — Delivered artifacts (exactly two files; full bodies in REM-001)

| File | Bytes | sha256 |
|---|---|---|
| `alembic/versions/20260909_0052_v2_be11_seed_overlay.py` | 6,312 | `004ecdd64bb72003630d5d04698a1848e5cb88a5839444f82372b41530e1dd5e` |
| `tests/test_v2_be11_seed_overlay.py` | 10,060 | `52830b937e2a6e9b0b0c3afcffbcf8f6c262ca4268e7d0578ec8c6dbd89e6586` |

**Zero other bytes moved.** Engine/model/API untouched — pbr rolled hash
re-measured at every stage (gate, transcript build, this report):
`4c243435103a149830fd448d4f84a931af7543aa08b901299ebb5d1a27ff178b` (the
spec §4 assert-not-mutate pin holds). Compver OFF. DDL none. Triggers none
on net (§2 dance disclosure below). Permissions untouched (enum was
confirmed as-shipped at OV-001 review — register-only, closed).

## §2 — The migration (revision `20260909_0052`, parent `20260909_0051` — the OV-F3 single-id election honored)

- **Five INSERTs, nothing else**: 4× `drift_tolerance` rows
  (`{name, value, unit, citation}` — balance / margin_used /
  margin_available / unrealized_pl, each `"125.00"` USD, citation
  `"operator seed"`, values QUOTED from OV-002 §1, never retyped) + 1×
  `generation_staleness` row (`{max_age_hours: 48, citation}`).
- Rows carry `run_kind='seed'`, `data_class='simulated'`, `mode='PAPER'`,
  actor/operator = the act reference `OV-V2-BE-11-002` (register-act
  identity per spec §1), fixed `created_at` (determinism: values fixed at
  authoring; uuid4 ids lawful per spec — not part of any digested world).
- **DEL-004 existing-set filter** on upgrade, content-keyed
  (seed_name + payload name) — re-entry safe, never duplicates.
- **Downgrade**: content-keyed deletes of exactly the five rows
  (`json_extract(payload,'$.name')` per tolerance row; act-scoped),
  count-asserted (`post == 0` for the act's rows, delta ≤ 5 law).
  **Disclosure — guard dance:** the 0051 immutable pair prohibits DELETE
  by design, so the downgrade drops/recreates the guard pair around its
  deletes, restoration count-asserted (`RuntimeError` if != 2) — the
  compver delete-guard dance precedent applied to the bridge pair. The
  UPGRADE path never touches the triggers (INSERTs are lawful under the
  guards). Net trigger census at 0052: unchanged, 78.

## §3 — Coupons (8 new; suite 1,155 → 1,163, +8 exactly; spec budget 6–10 honored)

| Coupon | Spec §2 line | Proof |
|---|---|---|
| `test_ov_one_upgrade_line_0051_to_0052` | gate pair | exactly ONE `Running upgrade` line, BOTH streams parsed (N-O8) |
| `test_ov_seed_census_exact` | seed census | 5 rows; names/values/units/citations == the quoted spec table; census tattoo 78/69/13 unchanged; zero non-seed rows (EMPTY-FORCE assert) |
| `test_ov_armed_flip_and_tolerance_census` | armed flips | engine reads: tolerance census 4 (all four field names), staleness 48.0, armed state |
| `test_ov_generation_staleness_arms` | 23h/49h arms | 23h → `accept_with_notes`; 49h → typed `basis_stale` (the spec's restated direction: age ≤ 48 not stale, above refuses) |
| `test_ov_drift_three_ways_and_boundaries` | 125/250 law | 0.00 within (spec's zero-delta arm) · **125.00 within (tol-inclusive-by-design boundary)** · 125.01 minor · **250.00 minor (2× boundary)** · 250.01 major · each seeded field individually resolvable |
| `test_ov_downgrade_reverses_exactly` | downgrade | 5→0 rows, head back at 0051, guard pair == 2 restored |
| `test_ov_guard_pair_live_after_overlay` | immutability | UPDATE + DELETE still refused live on the seeded lineage |
| `test_ov_drift_gate_0052` | drift law | zero band tokens at the 0052 head; inheritance witness present |

**Suite seal:** `1163 passed, 2 warnings in 597.53s` (quiet run) and the
delivered `-v` transcript `1163 passed, 2 warnings in 601.56s` — floor
moved 1,155 → 1,163, +8 exactly, nothing else moved. Warnings = the
carried registered pair.

**Fail-first witness (OBS-E):** migration stashed → gate-pair coupon
FAILED genuinely (absent revision unresolvable) → restored, post-restore
sha256 == manifest row. `V2_BE-11_OV2_FAILFIRST_WITNESS.txt`.

## §4 — Evidence pack identities (all measured from final bytes)

| Artifact | md5 | sha256 |
|---|---|---|
| `V2_BE-11_OV2_BUILDGATE_PROBE.txt` | `42999a6b0fad0b8f62d34cead5910bc7` | `58eeae83c189bc9e84b5447b6f4a408a6401e010d4b46a553779edb71954b696` |
| `V2_BE-11_OV2_SOURCE_TRANSCRIPT.md` (REM-001) | `16dbb1d696f78b4f1dc4f380549fabdd` | `3ce4f6f9137201ce4db159751ebc30da70d7d4c4547b59fc5a5a99082ffb124d` |
| `V2_BE-11_OV2_TESTRUN_TRANSCRIPT.txt` (full `-v`) | `ed631d18f76a1f4b5c64d99a0f0c09a4` | `595a60443faec967eac74aa16aee3e005caa50ba6722ca0e88fe20dd1d972f3d` |
| `V2_BE-11_OV2_FAILFIRST_WITNESS.txt` | `d40b3a3f1913195f0922a12f3af49cc6` | `2cfc406cbd254d1f4d20106c2a2a44d29daf832549901ce31a9ac6dd3a7ac604` |

Credential scan on both delivered files: sole hits are the standing test
fixture `AXIOM_JWT_SECRET_KEY = "test-secret-key-at-least-32-chars-long!!"`
— CLEAN-with-classification per precedent. Ruff clean, line-length 100.

## §5 — Register intent map (carried verbatim from OV-002 §1, for the record)

Minor boundary 125.00 USD · major boundary 250.00 USD (structural 2×) on
each of the four compared fields — the closest lawful form of the earlier
percent intent under pbr-1.0.0, as the spec declares. The 2× law was
accepted, not worked around.

## §6 — What was NOT done

- No console act: the fielded file is untouched; working lineage remains
  OPERATING at `20260908_0050`. The OV-002 §3 ladder (micro-ACC → micro-INT
  → one-line APPLY → P-4 seeds=5, census 78/69/13, pbr unchanged → suite
  seal → FIRST-READ micro-witness) begins after acceptance. Note the 0051
  band apply is itself still pending on the console — the overlay rides
  BEHIND it in the same family (0051 then 0052, or one two-line act if the
  authorities elect that; the DA flags the sequencing question rather than
  presuming).
- No mode flip: this box stays RESEARCH; generation writers still 403 by
  D-B11-MODE. Flip-to-PAPER = a separate operator register act, as §3 says.
- No engine bytes: the "2.5" percent intent was NOT resurrected; it died at
  Exit (a) per the spec's own intent map.

**We don't guess. We prove.** The jar has seeds in it now — and the engine
was watched eating from it before a single migration line was written.

— AXIOM-V2-BE-11-OV-DR-001 · v1.0.0 · 2026-09-07
