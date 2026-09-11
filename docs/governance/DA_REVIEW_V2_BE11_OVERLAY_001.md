# DA REVIEW — SEED OVERLAY SPEC OV-V2-BE-11-001: **BLOCKED BEFORE GO** (THREE FINDINGS, LEVEL-I EVIDENCED)
# AXIOM-V2-BE-11-DA-OVREV-001 · v1.0.0 · 2026-09-07
# Reviews: ITRGA-SEED-OVERLAY-BE11-001 (filed: md5 `3ae73739b92462eab489d78329953fdc` ·
#          sha256 `8a3a617d8c7c7b18468e4d70e41ca92a3ef5b7d0d61ffce499d8cf1e29e50777`)
# Author: Replacement Development Authority (DA)
# Verdict vocabulary: **BLOCKED** — the overlay, implemented verbatim, seeds NOTHING.
# Evidence: `docs/evidence/V2_BE-11_OVERLAY_PROBE_WITNESS.txt`
#          (md5/sha256 pinned in §5; probes A/B/C, engine bytes untouched, hash-held at
#          `4c243435103a149830fd448d4f84a931af7543aa08b901299ebb5d1a27ff178b` throughout).

---

## §0 — Posture and why this lands BEFORE the Operator GO

The spec is styled "FOR DA IMPLEMENTATION UPON OPERATOR GO." The DA ran the
payload against the ACCEPTED pbr-1.0.0 bytes on scratch 0051 chains before any
GO could consume it, because the overlay's whole premise — "CHECK-conformance
guaranteed a priori" — is a schema claim, and schema conformance is not the
same thing as ENGINE conformance. The first is true. The second is false.
Implementing as written would be concealing a known defect inside a delivery,
which the DA may not do.

## §1 — FINDING OV-F1 (GATING): the spec's seed rows are INERT against the accepted engine

**Probe A (Level I, verbatim payloads):** all three rows INSERT cleanly
(the CHECK claim holds) — and then:

```
read_tolerance_seeds() -> 0 rows      (engine reads seed_name == 'drift_tolerance', exact)
read_staleness_seed()  -> None        (engine reads seed_name == 'generation_staleness', exact)
comparison_state       -> refuse_to_compare_unseeded
compute_drift          -> uncomputable
evaluate_intent(23h)   -> basis_staleness_threshold_unseeded
```

The spec's dotted names (`drift_tolerance.minor`, `drift_tolerance.major`,
`generation_staleness.max_age_hours`) never match the accepted engine's exact
equality reads (engine.py, the ACCEPTED and compver-pinned bytes). Every
coupon the spec orders — (b) 23h armed / 49h `basis_stale`, (c) armed-state
flip with seed census 2 — would FAIL against its own payload.

**Severity shape — worse than fail-closed:** the rows land on an immutable
lineage (guard pair prohibits UPDATE and DELETE; INT-witnessed live). The
register would read "seeded" while the fielded engine still refuses
everything, and the dead rows cannot be repaired in place — only superseded
by yet more rows. That is fail-SILENT with permanent debris, the exact
failure family the naming-of-numbers and enumeration laws exist to kill:
names written into a record without being measured against the bytes that
consume them.

**Probe C (isolation):** name corrected, spec chassis kept →
`uncomputable: seed rows malformed (citation chassis incomplete)`. The
accepted per-field chassis is `{name, value, unit, citation}`; the spec ships
`{value, unit, citation}` with no `name` (no compared-field binding at all).
So the defect is BOTH arms independently: names AND chassis.

## §2 — FINDING OV-F2 (GATING): the (minor=1.0, major=2.5) pair is NOT EXPRESSIBLE in pbr-1.0.0

**Probe B (Level I):** the accepted engine arms only on per-field tolerance
rows; the minor/major boundary is STRUCTURAL — `delta ≤ tol` |
`delta ≤ 2×tol` | `> 2×tol` — around ONE tolerance per compared field, in
ABSOLUTE comparison units (witnessed: tol 1.00 → 1.80 `drift_minor`,
3.00 `drift_major`). Two consequences:

1. An INDEPENDENT major threshold (2.5) cannot be seeded: with tol=1.0 the
   major boundary sits at 2.0 by law. No seed row can move it.
2. `percent_of_compared_magnitude_2dp` semantics exist NOWHERE in
   `compute_drift` — there is no percent computation to give that unit
   meaning. A seed can carry the string, but the engine would treat the
   value as absolute units: **1.0 would mean one whole currency unit, not
   one percent** — a silently wrong tolerance on a drift gate.

Honoring the spec's SEMANTICS (independent minor/major pair, percent-of-
magnitude units) requires an ENGINE change → `pbr-1.1.0`, compver row
movement, INT re-cycle — explicitly beyond "data rows only, zero DDL/model
edits." The spec's own citizenship clause forbids what its payload demands.

## §3 — FINDING OV-F3 (non-gating, record hygiene): the spec names TWO different revision ids

§ "Revision id proposal: `20260909_0052`" vs § "one upgrade line
`20260909_0051 -> 20260912_0052`" — same document, two ids for one
revision. Either is individually lawful under the revision-dating precedent;
carrying BOTH into a build is how a pin sheet grows a false stop (the
F-C1/N-O2/N-O9/DA-F1 family, now on the spec side). One id must be elected
in the corrected spec.

## §4 — The two lawful exits (both above the DA; the DA builds NOTHING until one is elected)

- **Exit (a) — re-cut the PAYLOAD to the accepted shapes (stays a true
  overlay: data rows only, zero engine edits).** The Operator restates the
  values in the accepted chassis:
  * `drift_tolerance` rows, one per compared field, payload
    `{name: <field>, value: <absolute tolerance in comparison units>,
    unit: <accepted unit noun>, citation: <operator citation>}` — the field
    list is itself an Operator input (the probes used `balance`
    illustratively; the DA does not elect fields);
  * `generation_staleness` row, payload `{max_age_hours: 48, citation: …}` —
    this one carries over almost as-is (Probe B: 48h arms; 23h/49h coupon
    arms both reachable);
  * the minor/major boundary REMAINS the structural 2× law — if 2× is
    acceptable, say so in the corrected spec; the "2.5" intent dies here or
    moves to exit (b).
- **Exit (b) — amend the ENGINE to read the spec's semantics** (dotted-name
  slots, global percent-pair tolerances): `pbr-1.1.0`, a BO amendment, a new
  compver expectation, full coupon + INT cycle. Lawful, but it is a BAND
  change wearing an overlay's name, and it must be ordered as what it is.

The DA recommends (a) on scope-hygiene grounds and holds no authority to
choose. NOT PROVEN ≠ FALSE applies to intent: the DA asserts nothing about
which semantics the Operator MEANT — only what the accepted bytes DO.

## §5 — Evidence identities (measured from final bytes, this hour)

| Artifact | md5 | sha256 |
|---|---|---|
| `docs/evidence/V2_BE-11_OVERLAY_PROBE_WITNESS.txt` | (see register line) | (see register line) |
| Spec as filed | `3ae73739b92462eab489d78329953fdc` | `8a3a617d8c7c7b18468e4d70e41ca92a3ef5b7d0d61ffce499d8cf1e29e50777` |
| pbr-1.0.0 engine (rolled, unchanged all probes) | — | `4c243435103a149830fd448d4f84a931af7543aa08b901299ebb5d1a27ff178b` |

Scratch worlds: `/tmp/be11_ov/` only; explicit `AXIOM_DATABASE_URL` every
step (§2.4); one harness lapse disclosed — the first Probe-C rise omitted
`AXIOM_TD_TRANSITION_AUTHORITY_REF` and FAILED CLOSED at the 0042 gate
(P-7 doing its work); corrected, no gate weakened. Fielded file untouched;
working lineage OPERATING at `20260908_0050` throughout.

## §6 — What the DA did NOT do

No migration authored. No engine byte touched. No seed value invented or
substituted (Probe B values are marked illustrative in the witness and in
their own citation strings). No unilateral election between §4(a)/(b).
The overlay build starts when a corrected spec + Operator GO arrive.

**We don't guess. We prove.** A seed that the engine cannot read is not a
seed — it is a label on an empty jar, sealed onto an immutable shelf.

— AXIOM-V2-BE-11-DA-OVREV-001 · v1.0.0 · 2026-09-07
