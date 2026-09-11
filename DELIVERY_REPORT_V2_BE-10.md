# DELIVERY REPORT — AXIOM V2 BE-10: Signal-Against-Account Intelligence

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-10-DR-001 |
| Version | 1.0.0 |
| Build Order | BO-V2-BE-10-001 (B-0 rulings sealed: D-4 revised — symbol-map extension, zero new tables; 12 map pairs sealed) |
| Date | 2026-09-06 |
| Author | Development Authority (DA) |
| Status | **SUBMITTED FOR INT (sandbox apply + census + suite per B-4)** |
| Baseline in | OPERATING head `20260905_0049` · 1,077 tests · triggers 76 · permissions 64 · compver 11 |
| Baseline out | migration `20260908_0050` (**DA test chains only**) · **1,121 tests** (1,077 + 44) · triggers **76** (zero new — seed-only) · permissions **65** · compver **12** — the B-3 tattoo hit exactly |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive summary

Band BE-10 implemented per the BO body set, all ten laws test-armed:
a **read-only analytics join** (BE-9 broker projections × BE-5 signal
registry) behind two GETs; the **closed 7-verdict enum in the sealed
order** with the wording law enforced by scan (state nouns only — no
action verb anywhere in vocabulary or code identifiers); the **basis
law fail-closed** (`account_context.no_basis` typed); the **mapping law
explicit** (seeded rows only; a miss is a VISIBLE `unmapped` verdict,
never a filter, never a guess); **digest determinism ×3**; the **seed-only
0050 migration** landing exactly the sealed 12 map pairs + the fourth
source + one permission + one compver row, reversible-exact.
**1,121/1,121 passed.** Zero broker contact, zero writes of any kind
from band code, zero network.

## 2. Laws L1–L10 (evidence map)

| Law | Evidence (executed) |
|---|---|
| L1 GET-only | `test_l1_get_only_route_census`: exactly `/alignment` + `/summary`, zero non-GET methods |
| L2 zero broker writes | `test_l2_zero_mutation_verbs_in_band_code`: no session.add/delete/commit/INSERT/UPDATE/DELETE token anywhere in band modules (the band reads; it never writes ANYTHING — stronger than the broker_*-only law) |
| L3 banned imports | `test_l3_banned_imports_absent`: providers.exness_mt5 / vault / MetaTrader5 / network libs / paper_trading — zero hits on the import graph |
| L4 basis fail-closed | `test_l4_no_basis_typed_refusal` (engine) + `test_l4_no_basis_refusal_on_the_wire` (API): typed `account_context.no_basis`, never synthesized; `test_basis_is_newest_complete_only`: a newer FAILED run never becomes the basis; mapping-artifact-absent arm typed too |
| L5 closed enum + wording | `test_l5_verdict_enum_closed_and_sealed_order` (the 7, sealed order); `test_l5_wording_law_state_nouns_only` (no action verb in vocabulary OR band code identifiers, docstring-stripped); R-3.5 distinct-states assertion |
| L6 unmapped visible | `test_full_matrix_and_l6_unmapped_visible`: an unseeded symbol lands as verdict `unmapped` in the matrix with `unmapped_count=1` — present, counted, never filtered |
| L7 digest ×3 | `test_l7_digest_deterministic_x3`: three computations over the same (basis, mapping, signal pins, ace version) → equal 64-char digests |
| L8 banner end-to-end | `test_l8_stale_basis_banner` (engine: >24h ⇒ stale + banner, still answers) + `test_l8_banner_carried_end_to_end` (both GETs carry staleness + banner) |
| L9 RBAC both routes | `test_l9_rbac_gates_both_routes`: operator-role 403 generic on both; 401 unauthenticated on both; admin passes (the new permission is the sole gate) |
| L10 seed-only reversible | `test_0050_seed_only_no_schema_ops` (zero table/trigger delta across 0050 — content law); `test_0050_downgrade_reverses_exactly` (all four seed families byte-restored; compver delete-guard dance + count-assert); `test_0050_seed_idempotency` (down/up cycle, no duplicates) |

Verdict matrix: `test_verdict_matrix_table_driven` — 11 parametrized
rows covering every (posture × signal-state × mapped) cell incl. the
mixed-book and expired-signal edges; posture law unit-tested.

## 3. Census tattoo (B-3) + test accounting

- **triggers 76 · permissions 65 · compver 12** — live-witnessed on the
  DA chain AND test-asserted (`test_0050_census_tattoo`).
- Sealed map rows: `test_0050_sealed_map_rows_exact` asserts the rowset
  EQUALS the 12 sealed pairs — no invented rows possible.
- compver: `account_context_engine | ace-1.0.0` seeded from disk;
  DA-disk value at delivery (§5 naming-of-numbers law — measured from
  the final bytes after the suite ran):
  `532ef0ce274dee16b111ec14a313bc618b826a006478207fb5fd06094c9850fd`.
  RPE/RJE/PXS/PRG/BRE untouched (append-only).
- Tests: contract 7 · boundaries 6 · engine 19 · api 5 · migration 7 =
  **44** (BO budget ~30; the overage is the table-driven verdict matrix
  — 11 parametrized rows counted individually). Suite **1,121/0**.

## 4. Disclosures (honest)

1. **Source-row vocabulary fit (B-0 D-4 consequential):** `v2_md_source`
   carries closed BE-2 CHECKs (`kind IN ('simulator','seed','import',
   'reserved')`, authority set + active-authority law). The fourth source
   row therefore lands as `kind='import'`, `authority='unknown'`
   (non-authoritative by construction; lawful with `active=true`). This
   is the honest classification — the row is a symbol-mapping ANCHOR for
   the read seam, not an authoritative market-data source. A seed-only
   migration may not amend CHECKs; if ITRGA prefers a dedicated
   `broker_read` kind, that is a future schema act.
2. **Permission namespace ruling consumed:** `v2.account_context.` is
   the third literal-prefix exemption (same mechanism as D-1/DECISION-1),
   with must-die arms: `v2.research.account.*` dies, `v2.account_contexts.*`
   dies (boundary; trailing-dot law).
3. `signal_direction` law: the engine reads `payload.direction ∈
   ('up','down')`; anything else (absent, malformed) = `indeterminate`
   — no guessing. Signals currently empty on the working lineage
   (`flat_no_signal`/fixture-verified until signals appear — B-0 census).
4. Fail-first witness shipped (`ModuleNotFoundError` with engine
   stashed). OBS-E honored.
5. Working-DB application of 0050: **not performed** — the B-4 protocol's
   operator-signed apply act follows acceptance.

## 5. Evidence package (full hashes; measured from final bytes)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| `docs/evidence/V2_BE-10_SOURCE_TRANSCRIPT.md` (REM-001; 10 new + 2 modified, literal bodies) | 68,409 | `f8f5a64e94bf2ed7121027425a757274` | `946e04d243742fc64fe7171c2d71ec03b1ec09311f9eb0247cbcc6777023eb79` |
| `docs/evidence/V2_BE-10_TESTRUN_TRANSCRIPT.txt` (raw `-v`; **1,121/0**) | 108,833 | `91a8ca0a10fe1585d8a15ebf78e57beb` | `d059cf0549f267b1285cd5ebfc59512dda3e182b5d7441cd713edc46d47f1dd1` |
| `docs/evidence/V2_BE-10_FAILFIRST_WITNESS.txt` (OBS-E) | 734 | `83af460024bde81ae5d3040d80be0f47` | `38a34f35811289501d6b08244184b8a3ff71d8879f796c52fc313168919b9c24` |

Credential scan CLEAN (household test-auth placeholders only). Ruff
clean. No Git operations; custody Operator-only.

## 6. B-4 protocol position

BUILD complete (this delivery; corpus SHAs in the transcript §1) →
**next: INT** (sandbox: apply 0050 on a clone, verify census 76/65/12,
suite band + full) → E1-style sandbox evidence (fixture basis + fixture
signals → matrix, ×3 digest) → acceptance doc (tattoo + pins) →
operator-signed apply act on the working DB → first-read witness →
closeout. No step self-promotes.

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-10-DR-001**
