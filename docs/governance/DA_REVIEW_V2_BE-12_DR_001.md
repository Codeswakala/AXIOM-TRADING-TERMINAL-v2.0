# DA REVIEW — DR-V2-BE-12-001: REGISTER-AS-DESIGNED WITH FIVE ANSWERS AND THREE AMEND-CLASS FINDINGS
# AXIOM-V2-BE-12-DA-DRREV-001 · v1.0.0 · 2026-09-08
# Objects: OPERATOR ADJUDICATION (ADOPT + amendments absorbed; filed md5
#   `8d4ac4d6c5709356b7701506d7255a49`) · DR-V2-BE-12-001 (filed md5
#   `b24061d844f77bb654746c06d61b96eb`)
# Author: Replacement Development Authority (DA)
# Answering the DR's five review questions with Level-I survey facts (line numbers
# from the standing suite, enumerated fresh this hour). Verdict at §7.

---

## §0 — Adjudication acknowledged

ADOPT across the board; S-1…S-4 absorbed as AM-1…AM-4; R-1.4/R-6.2 DA wording
adopted VERBATIM; §10 authorizes the DR stage only. Nothing below starts
implementation.

## §1 — Answer (1): AM-1…AM-4 BO-citation feasibility — WITH ONE HARD COLLISION FOUND

**The standing coupon lineage for AM-2, enumerated from the suite (fresh):**

| Coupon | File | What it pins |
|---|---|---|
| `test_mode_rejects_live` | `tests/test_v2_mode.py` L39–43 | `get_mode()` under `AXIOM_V2_MODE=LIVE` raises `ValueError` |
| `test_valid_modes_include_paper_as_of_be8` | `tests/test_v2_mode.py` L53 | `VALID_MODES == ("RESEARCH","SIMULATION","PAPER")` |
| `test_deferred_modes_are_live_only` | `tests/test_v2_mode.py` L57 | `DEFERRED_MODES == ("LIVE",)` |
| mode-pin block | `tests/test_v2_be8_boundaries.py` L207–210 | both tuple equalities |
| mode-pin block | `tests/test_v2_be9_boundaries.py` L199–201 | both tuple equalities |
| mode-pin block | `tests/test_v2_be10_boundaries.py` L101–103 | both tuple equalities |

**FINDING DR-F1 (GATING for AM-2's mechanics):**
`tests/test_v2_be9_boundaries.py` is **byte-pinned in-suite** by BE-11's wall
coupon (`test_v2_be11_api_walls.py` L284–291, sha
`9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f`) — the
"wall pair byte-unchanged" law that ITRGA itself verified at ACC and INT.
**That file contains one of the LIVE-pin coupons. It cannot be edited without
breaking the BE-11 byte pin** — which would be a BE-11 register act, not a
BE-12 supersession.

**The lawful path exists and the DA proposes it as the AM-2 implementation
law:** the three boundary-file blocks assert only the TWO TUPLE EQUALITIES.
Both stay TRUE if AM-2:
- **keeps `VALID_MODES` and `DEFERRED_MODES` byte-identical** (LIVE remains
  "deferred" in the standing vocabulary — true: its BEHAVIOR is deferred),
- **adds** `REGISTERED_LOCKED_MODES = ("LIVE",)` as a new name, and
- moves the constructibility change into `get_mode()`/a sibling constructor
  (LIVE accepted, tagged locked; every actuation seam refuses `mode_locked`).

Then the ONLY superseded coupon is `test_mode_rejects_live` in
`test_v2_mode.py` — a file that is NOT byte-pinned anywhere — replaced by
citation with `test_mode_live_registered_locked` (constructs, carries the
locked tag, actuation refuses). The three boundary blocks stand UNTOUCHED and
UNSUPERSEDED; the BE-11 byte pin never moves; drift = one file, one test, one
citation. **AM-1** (marker exemption in `permissions.py` — not byte-pinned,
D-1 precedent exact), **AM-3** (`EXECUTION_BACKENDS` literal + its coupon
`test_v2_be8_boundaries.py` L69–75 — NOT byte-pinned [BE-11 holds it
presence-only, L286 comment: "None # presence-only check"], so the len==2
supersession is a clean cited edit), **AM-4** (vault credential class — new
code, no standing coupon collides): all three verified feasible as drafted.

## §2 — Answer (2): can L1 `mode_locked` mis-fire through a posture-only promenade?

As drafted — **yes, it can**, and the fix is one law. The hazard: L1–L6 are
six predicates that MANY code paths will evaluate. If each writer verb
composes its own checks, the same fielded state can refuse with DIFFERENT
reasons on different paths (a posture check reached before a mode check on
one route, after it on another) — nondeterministic witnesses, flaky
closeout evidence, and a promenade where a posture refusal masks the mode
lock (or worse, vice versa).

**Proposed law (LOCK-ORDER):** ONE chokepoint —
`require_actuation(mode_state, posture, activation, killswitch, ...)` — the
only door to any actuating verb, evaluating the locks in PINNED ORDER
L1→L2→L3→L4→L5→L6, first failure typed, order itself coupon-tested (a
fixture that fails L1 AND L3 must refuse `mode_locked`, never
`activation_instrument_not_in_force`). `mode_locked` computed ONLY from the
mode contract (never from posture inputs); `posture_mismatch` computed only
from credential-class facts. With the chokepoint + order law, L1 cannot
mis-fire because nothing else is allowed to answer. This is the BE-8
`may_execute`-owned-once law generalized to six locks — same reasoning that
won there.

## §3 — Answer (3): sub-band sizing and migration ranges — CONFIRMED

12A 30–40 · 12B 35–45 · 12C 20–30 · 12D 25–35 · 12E 25–35 matches the DA's
REQ-stage sizing. Migrations `0053…0057`-class confirmed against the chain
head on disk (`20260909_0052`, verified fresh). Suite stairs from 1,163 with
per-sub-BO deltas. One accounting law to carry: each sub-band re-tattoos the
census in ITS migration (the BE-11 precedent), so no sub-band's counts float.

## §4 — Answer (4): is practice + refusal-injection sufficient for CAPABILITY-COMPLETE?

**Yes — by construction, under the adopted R-1.4 wording.** The Operator
adopted VERBATIM a completion definition whose evidence set is: every scope
verb coupon-proven + L1–L6 witnessed refusing on the fielded lineage. The
LIVE real-network leg is NOT in that set; it belongs to the activation
instrument's own future evidence arms. Practice-leg actuation covers every
behavioral requirement (R-2's own claim, DA concurs — the practice book IS a
real broker book); refusal-injection covers the failure arms the practice
world can't produce on demand (E-ENV-1 precedent). Two conditions to keep it
honest: (i) the register line carries `LIVE real-network behavior: NOT
PROVEN (≠ FALSE)` explicitly at closeout; (ii) a **counterfeit-witness scan**
ships in 12E — a coupon asserting no evidence artifact in the band's family
claims live-network proof (the PGF-022 lesson applied to claims instead of
banners). With those, the honesty clause is load-bearing, not decorative.

## §5 — Answer (5): the `docs/arena_spec` / "seat-book law" citation — NOT IN THE CUSTODY RECORD

Enumerated fresh: **no `docs/arena_spec` directory exists anywhere in the
repository**, and no "seat-book law" appears in any governance document in
custody. Same for the citizens line: `DIRECTION-POSTBE11-001` is not a
document the DA holds (custody has OPERATOR_DIRECTION_BE12_001 =
DIRECTION-BE12-001, and ADJ-REQ-BE12-001). NOT PROVEN ≠ FALSE — these may be
ITRGA-side instruments not yet relayed. But a DR citing paths and laws
outside the shared record is the N-O19/OV-F3 defect family (names not
measured against the bytes that must consume them). **Request:** either
relay the instruments/create the path, or correct the citations (the DA
reads the intent as: design documents land in `docs/design/` per the
standing ADR convention — which the DA will follow for the AM-2 amendment
text unless directed otherwise).

## §6 — Two further AMEND-class observations (unrequested but priced)

- **DR-F2 (money-unit law variance):** DR-4 declares live_exec money as
  minor-unit INTEGERS / signed-4dp basis points. Standing BE-9/BE-11 facts
  are string decimals with 2dp presentation law (D-B10-2DP mirror). Fine as
  a NEW domain law — but 12E's reconciliation compares live_exec facts
  against BE-9 projections, so the CONVERSION law (string-decimal ↔ minor
  units; rounding mode; who converts, once, where) must be written in the
  12E BO or the parity coupons will grow ad-hoc conversions — the exact
  place silent drift breeds.
- **DR-F3 (vocabulary nit, non-gating):** DR-3 says the practice leg rides
  the "sealed BE-10/BE-11 boundary family" — the practice ACTUATOR is BE-9's
  provider family (broker_read/providers, the sanctioned MT5 leg); BE-10/11
  are projection consumers. One-word correction to keep the wall map exact.

## §7 — Verdict

**REGISTER-AS-DESIGNED, with:** DR-F1's AM-2 implementation law adopted into
the BO text (tuples byte-still + `REGISTERED_LOCKED_MODES` + single
superseded coupon — the BE-11 byte pin never moves); the §2 LOCK-ORDER
chokepoint law adopted into 12A's BO (it is foundation, not polish); §4's
two honesty conditions bound to 12E; §5's citations corrected or the
instruments relayed before BO-V2-BE12A-001 issues; DR-F2's conversion law
assigned to the 12E BO. On those, the DA is ready for BO-V2-BE12A-001 and
build of 12A.

**We don't guess. We prove.** Six locks, one door, a pinned order — and the
byte pin that BE-11 set stays exactly where the reviewer left it.

— AXIOM-V2-BE-12-DA-DRREV-001 · v1.0.0 · 2026-09-08
