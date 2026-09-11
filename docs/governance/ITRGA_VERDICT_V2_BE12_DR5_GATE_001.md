# ITRGA-VERDICT-V2-BE12-DR5-GATE-001 — DR-5 CLOSEOUT-GATE ENUMERATION

**The DR-5 band-closeout register line is LOCKED-AND-HELD, not yet issued. Condition (i) of the closeout gate is adjudicated herein: L3 is DISCHARGED BY FIELDED RECORD; L5 is DISCHARGED BY DESIGN; L1, L2, L4, L6 are ADDENDUM-REQUIRED. One governed battery — the closeout addendum card — stands between the ladder and its final line.**

- **Date:** 2026-09-09 · issued alongside ITRGA-VERDICT-V2-0057-FIELDED-001
- **Authority (the gate's own text, BO-V2-BE12E-001 closeout conditions, binding):** "(i) the five locks L1–L6 enumerated with their fielded-lineage refusal witnesses across the 0053–0057 card record — ANY lock lacking a fielded-lineage witness is witnessed by a CLOSEOUT ADDENDUM card (read-only/400-pin pattern; operator-elective harness) BEFORE the DR-5 line issues." · DR-5 (evidence shape) · DR-3(i) (honesty clause) · the five field cards 0053–0057 with the 0057 cumulative-witness record · ITRGA-REV-V2-BE12{A,B,C,D,E(-CR)}-001
- **Jurisdiction (BO, carried):** coupon-verified + corridor-witnessed acts are acceptance-grade; NO real-network activation act of any kind is performed or required — not by any band, not by the closeout; the instrument NEVER takes force; any future force-taking is its own register act under a future build order.
- *Naming-of-numbers (register-logged, non-gating): the BO clause says "the five locks L1–L6" — the enumeration is of SIX locks; the DR-2 table is authoritative.*

---

## §1 — THE L1–L6 ENUMERATION (the gate's condition (i), adjudicated)

| Lock | DR-2 witness arm (typed) | FIELDED-LINEAGE record (0053–0057) | Typed-refusal witness of record | ADVANCED RULING |
|---|---|---|---|---|
| **L1** Mode REGISTERED_LOCKED | attempt actuation in LIVE ⇒ 400 `mode_locked` | REGISTERED_LOCKED register fact at all five card boundaries; no armed session ever; §6 law GETs-only; **no actuation attempt was ever issued on the fielded lineage — by the field law itself** | **L1-and-L3 fixture answers `mode_locked`** with `order_position` metadata, **over the real migration-applied schema**, in-transaction, rolled back (12D review §1.b.4; order law coupon-tested) | **ADDENDUM-REQUIRED** — the lineage has never heard itself say `mode_locked` |
| **L2** Posture mismatch | practice credential vs LIVE seam ⇒ `posture_mismatch` | Double env sweeps at every card's open AND close (incl. V1 A0b; CONT B0b/B4.6): **no `AXIOM_TD_*`, no `AXIOM_BROKER_PRACTICE_*` on the fielded host, ever** — the mismatch condition cannot arise as fielded posture | Eligibility distinction battery (`mode_locked` vs `posture_mismatch` disjointness, R-3.2 family) at suite floor | **ADDENDUM-REQUIRED** — arm constructible only inside a sanctioned probe window: the practice credential may be present **only within the addendum's window**, re-swept absent at close (the cards' own bookend law) |
| **L3** Activation instrument absent | **zero-row table == refusal reason pinned** | **The DR-2-designated arm, delivered to the letter and beyond:** `v2_live_activation_instrument` pinned ZERO ROWS at every witness point — 0056 (A3/A6/A9/A10-post, ×4) and 0057 (A3/A6/A9.8/B1.8/B3, ×5) — `uq_v2_lai_sole` sole-row constraint live; `SOLE`/version/data_class vocabulary closed and rendered; **force cannot even be simulated: `data_class='simulated'` refused at schema in the field (0056 A10 battery)** | L3 typed at position 3; lock-opener armature proof (`live_marker` insert in-transaction opens L3 ⇒ L4 answers), **ROLLBACK, zero-row re-witnessed** (12D review §1.b.4) | **DISCHARGED BY FIELDED RECORD** — the DR says the zero-row IS the witness; the lineage pins it nine times |
| **L4** Funded posture required | basis/venue lacks funded posture ⇒ `funded_posture_required` | `funded account: NONE` register fact standing since the ladder's base, restated at every register line and register boundary; no vault provisioning at any card | L4 **answered** in the L3-armature walk (12D review §1.b.4); eligibility battery at suite floor | **ADDENDUM-REQUIRED** — refusal-only (basis arm), no write path exists behind it |
| **L5** Kill-switch armed/pulled | pull + every writer verb refuses; re-arm blocked ⇒ `killswitch_armed` | Resting posture pinned: `v2_live_kill_switch` ZERO ROWS at every 0056/0057 witness point — the armed condition is **dormant by doctrine**; guard pair refused VERBATIM on the fielded file (0056 A10.3/A10.4); `uq_v2_lks_sole` + closed status vocabulary (`armed/pulled/cleared`) rendered | 12D typed battery: **re-arm blocked `killswitch_armed` NON-FIRING on BOTH engaged states** (engaged/cleared cells all typed); three invalid pulls ⇒ `killswitch_state_invalid`; clear cells intact/idempotent (12D review §1.c.2) | **DISCHARGED BY DESIGN** — ruling text below |
| **L6** RK/signing/contract failures | E-ENV-1-style refusal-injection ⇒ downstream `sub_*` first-class subreasons | None direct — by construction: refusal-injection classes fire from the practice leg, which the fielded host never carries outside sanctioned windows | Refusal-injection coupon family at suite floor (E-ENV-1 proxy law generalized, DR-3); practice=WIRED register tokens (0054/0055 era) | **ADDENDUM-REQUIRED** — practice-leg failure-injection at the fielded surface; injection writes nothing |

### L5 ruling text (DISCHARGED BY DESIGN — read into the register)

A *fielded firing* of `killswitch_armed` requires a pulled kill-switch, which requires arm+pull **engine verbs on the fielded file** — and those are forbidden by the field law the ladder itself wrote: the 12D tables' zero-row **doctrine** (resting posture is the law, not the posture-of-the-moment) and the 12E law that no engine verb of any band runs on the fielded lineage. The closeout amends no doctrine. The fielded-lineage witness for L5 is therefore **its dormant-arm condition plus its live guard pair and closed vocabulary** (all witnessed), with the typed refusal proven acceptance-grade in the 12D review battery over the real schema. The register records the asymmetry deliberately: **some locks, in their final form, are witnessed by the impossibility of their fielded condition — and that impossibility is itself the fielded witness.**

## §2 — THE DR-5 LINE, LOCKED-AND-HELD (composition exact; issues ONLY after the addendum witness)

Per the BO's binding shape — DR-5 **exact** + DR-3(i) appended **exactly**:

```
BE-12 CAPABILITY-COMPLETE · ACTIVATION INSTRUMENT: NOT IN EXISTENCE · funded account: NONE (activation prerequisite) · LIVE mode: REGISTERED-LOCKED · LIVE real-network behavior: NOT PROVEN (≠ FALSE)
```

Definitional note (per BO, prevents the DR-5-vs-12D register-reading collision): **"ACTIVATION INSTRUMENT" names the FORCE-BEARING RECORD (zero-row == not in existence); the fielded template artifact is the instrument's extant non-force form per 12D BO §b.2 law and does not contradict the phrase.**

Suite-floor stairs for the closeout preamble (DR-5, "from 1,163"): **1,163 → 1,202 → 1,240 → 1,265 → 1,290 → 1,311** — five bands, five steps, zero regressions; no floor ever moved backward.

## §3 — RIDE-IN INVENTORY (carried by the closeout record when the line issues; all log-only)

1. **DEL-005 (LOW)** — disposition recorded: the DEL-003-election absent-price / uncanonicalizable / value-mismatch drift branches are witnessed **coupon-minimally at the suite corpus**; the closeout carries this line in lieu of a field witness — the field law forbids firing those paths on the lineage, and no such firing is required.
2. **DEL-006 (LOW needle)** — witness-line correction recorded: the §6.4 witness line overstated "full-text byte-equality restored"; the aligned claim is the **four-field witness (name / event / table / message)**; the 16- vs 4-space indent is a representation detail, zero code movement.
3. **Counterfeit-witness scan:** the corpus ships with the **12E DR line** — no evidence artifact of the band family claims live-network proof (PGF-022 lesson applied to claims), matching the honesty clause the DR-5 line carries.
4. **Errata family:** E-0054-A11.4 (itemized drift) and E-0055-A10.3 (rendered CHECK names) — standing, closed at their bands; **E-0057-A10.5 closed-as-witnessed** in the 0057 FIELDED verdict this date. The rehearsal-coverage advisory of §3.3 of that erratum becomes permanently binding on any future ladder: **probe-class gates get a rehearsal counterpart before their first fielded firing.**
5. Standing electives, unchanged: the 22-route GET-only survey at next restart; the real-wire witness (separate authorization); DEL-005's coupon runs by suite law, not by this gate.

## §4 — THE NEXT ARTIFACT (the ladder's true last field act)

**Card `ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001` + one pack (`ITRGA_V2_BE12_LOCKREFUSAL_400PIN_V1.ps1`)** — authored by ITRGA on operator go. Shape, fixed now so the design cannot drift before the build:

- **Application RUNNING for this act** (it is a surface witness, not a schema one); every attempt is a refusal-only POST harness against the running dev app, admin-authenticated **file-fed per the credential law (N-O18)** — the keyboard never crosses the transcript.
- **Arms (one per outstanding lock, four total):** L1 = actuation attempt in LIVE ⇒ 400 `mode_locked` · L2 = practice credential present **only inside a declared probe window** vs the LIVE seam ⇒ `posture_mismatch`, window re-swept absent at close · L4 = basis/venue arm ⇒ `funded_posture_required` · L6 = practice-leg failure-injection ⇒ first-class `sub_*` subreasons. Arms pin exact routes/payloads from the 12A–12E delivery contracts at authoring time (OpenAPI enumeration law).
- **Every attempt refuses at the eligibility layer — before any write; nothing lands;** the pack itself re-pins the election (seven tables zero) and the head/tattoo BEFORE and AFTER the battery, so the witness proves by construction that the refusal battery cannot have mutated the lineage.
- **After witness return:** ITRGA issues the **DR-5 CLOSEOUT VERDICT** — the band-closeout line of §2 entering the register EXACTLY, with this gate verdict cited as its condition (i) discharge. That act is the ladder's last.

---

**GATE VERDICT: condition (i) adjudicated — four locks addendum-required; the DR-5 line is composed, locked, and held. The ladder stands one battery from completion.** — ITRGA (BE-12 corridor), 2026-09-09
