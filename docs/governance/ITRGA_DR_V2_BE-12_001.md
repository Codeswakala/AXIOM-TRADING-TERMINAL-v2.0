# DR-V2-BE-12-001 — DESIGN RECORD: CONTROLLED LIVE EXECUTION GATEWAY (capability-before-activation)
`STATUS: FOR REVIEW — 2026-09-08`
`Register: V2_BACKEND_ROADMAP §BE-12 scope · sub-ladder 12A–12E (R-6.1 ordering law) ·
 REQ-V2-BE-12-001 adopted + operator adjudication amendments absorbed · citizens:
 DIRECTION-POSTBE11-001, DIRECTION-BE12-001, ADJ-REQ-BE12-001. Suite base law = 1,163.`

## DR-0 — ARCHITECTURAL POSTURE (the band in three moves)
1. **A fourth package family** — `app/v2/live_exec/` (per sub-band modules), importing
   BE-9 projections and BE-11 bridge engines READ-ONLY; no domain imports live_exec;
   live_exec writes to brokers ONLY through a single sanctioned adapter boundary.
2. **The activation boundary is the product** — three locks, each a TYPED, INDEPENDENTLY
   WITNESSED refusal (never one merged reason): posture lock, authorization instrument
   lock, kill-switch lock; plus the schema-armed lock: `v2_live_activation_instrument`
   with a zero-row check — absence is `activation_instrument_not_in_force`.
3. **LIVE becomes a third-state mode** — `REGISTERED_LOCKED`: recognized, typed,
   constructible for architecture/wiring/refusal/verification; behaviorally locked at
   every actuation seam (`mode_locked` ≠ `posture_mismatch`, both first-class).

## DR-0.5 — STANDING-LAW AMENDMENTS (BO-cited, from adjudication)
- **AM-1 (S-1):** `V2_FORBIDDEN_PERMISSION_MARKERS` gains literal-prefix exemption
  `v2.live_exec.` (trailing-dot law; must-die boundary arms: writer without the prefix,
  and `live_exec` outside the package, both die).
- **AM-2 (S-2):** mode contract: `VALID_MODES = ("RESEARCH","SIMULATION","PAPER")`,
  `DEFERRED_MODES = ("LIVE",)` —> introduce `REGISTERED_LOCKED_MODES = ("LIVE",)`;
  standing `VALID_MODES`-asserting coupons superseded BY CITATION of this DR/BO.
- **AM-3 (S-3):** `EXECUTION_BACKENDS` registry: 1 key -> 2 keys (`paper`, `live`);
  live entry posture-locked; len==1 coupon superseded BY CITATION.
- **AM-4 (S-4):** credential class `practice_trade` introduced; VAULT ONLY; isolated
  from investor/read-only class; absent from frontend/logs; funded-account class
  remains NONEXISTENT (register line law, R-6.3).

## DR-1 — SUB-LADDER ARCHITECTURE (12A -> 12E; ordering law: no sub-band opens until the
predecessor's coupons stand; each BO names suite/perm/compver/exception deltas + migration)

- **12A — Intents, eligibility, pre-trade risk** (`app/v2/live_exec/intents/risk/`)
  intent chassis (uuid, idempotency key, requested basis id, posture field); eligibility
  engine (account + instrument + session); risk engine (money-units sizing inherited
  from BE-11 flat-account law); digest per R-3.1/N-O13 per-world.
- **12B — Submission, acknowledgement, fills** (`submission/`) — adapter submission path;
  ack + fill event ingestion; unknown-state FIRST-CLASS typed (`unknown_fill_state`);
  submission-side dedupe anchored on fill-event correlation (BE-9 fill dedupe precedent);
  timeout -> hold-quarantined (BE-8 S2.4 preimage).
- **12C — Cancel/modify + unknown-state handling** (`modify/`) — only verbs the provider
  contract supports; cancel-on-unknown semantics; all fail-closed arms per R-3.2, plus
  S-2's `mode_locked`.
- **12D — Activation instrument + kill-switch** (`activation/`, `killswitch/`) —
  instrument TABLE zero-row lock; template artifact versioned, hash-pinned, NOT-IN-FORCE
  on its face; taking force = future register act (own evidence arms: funded-posture
  witness + step-up + kill-switch check). Kill-switch: persisted table, guard-pair
  triggers, zero-UPDATE regime with single sanctioned clear path; re-arm blocked until
  cleared (schema CHECK + typed refusal `killswitch_armed`).
- **12E — Reconciliation + incident workflows** (`reconcile/`, `incident/`) — fill/
  position parity vs projection; C-2 clean-runs-evidenced law; incident record shape
  (opened_by, severity, instruments pinned, recovery path) with register-facing digest.

## DR-2 — THE LOCK-STACK (fielded states = evidence)
| # | Lock | Refusal (typed) | Witness arm |
|---|---|---|---|
| L1 | Mode REGISTERED_LOCKED | `mode_locked` | attempt actuation in LIVE + 400 pins: reason == mode_locked |
| L2 | Posture mismatch | `posture_mismatch` | practice credential vs LIVE seam -> typed refusal |
| L3 | Activation instrument absent | `activation_instrument_not_in_force` | zero-row table == refusal reason pinned |
| L4 | Funded posture required | `funded_posture_required` | basis/venue lacks funded posture -> refusal |
| L5 | Kill-switch armed/pulled | `killswitch_armed` | pull + every writer verb refuses; re-arm blocked |
| L6 | RK/signing/contract failures | downstream-`sub_*` classes proxied | E-ENV-1-style refusal-injection, first-class subreasons |
(Operator actor + step-up reference present on every confirm — R-3.4 + adopted V2-TD-29 line;
second FACTOR, not second ACTOR; true two-operator segregation = future deployment requirement.)

## DR-3 — VERIFICATION STRATEGY (capability-complete without a funded account)
- Practice-world actuator: every verb exercised against the practice leg (sealed BE-10/BE-11
  boundary family); `practice_trade` credential used ONLY there (S-4 boundary).
- Refusal-injection for live-path failure arms (E-ENV-1 proxy law generalized): posture,
  basis, kill, duplicate, unknown-fill, cancel-unknown, RK/contract arms all provable WITHOUT
  any live network.
- Honesty clause: LIVE leg's REAL NETWORK behavior registered as **NOT PROVEN (≠ false)** —
  never implied-tested; the activation instrument's own future evidence arms remain pending.
- The 8-arm fail-closed battery (R-3.2) runs as standing-coupon-class tests per sub-band.

## DR-4 — SCHEMES & SURFACES (design floor)
- Schemes (per sub-band migrations): `v2_live_exec_intent`, `v2_live_exec_submission`,
  `v2_live_exec_fill_event`, `v2_live_kill_switch`, `v2_live_activation_instrument`,
  `v2_live_exec_reconciliation`, `v2_live_exec_incident` — zero-UPDATE regime,
  guard-pair triggers, surrogate pk law; all cars money-units (minor units integers)
  or Basis Points (signed 4dp exact), never floating money.
- Surface floor (R-4 refined): POST intents / evaluate / confirm / cancel-modify /
  killswitch{arm,pull,clear} / activation{draft-template read} — writes SAL-4, confirm
  HIGHEST rank (identity hangs on it), reads SAL-2/3 per surface; entire surface
  permission family `v2.live_exec.*` under AM-1 exemption; NEW execution-shaped
  endpoint inventory registers near `app/v2/live_exec/*` (governing-scope law).
- Contract posture: `EXECUTION_CONTRACT` class error family V1 contract tests per
  component posture (contract posture computed at boot, drift pins).

## DR-5 — EVIDENCE SHAPE (the deliverable, per adjudication §5)
Band closeout register line, exact:
`BE-12 CAPABILITY-COMPLETE · ACTIVATION INSTRUMENT: NOT IN EXISTENCE ·
 funded account: NONE (activation prerequisite) · LIVE mode: REGISTERED-LOCKED`
— with each of L1–L6 witnessed REFUSING on the fielded lineage, plus suite floor
stairs from 1,163 (per sub-BO naming deltas).

## DR-6 — NON-GOALS (life-ring)
NO front-end work. NO funded account. NO activation instrument execution (template
only, NOT-IN-FORCE). NO PAPER-law relaxation (BE-8 stays sealed in its existence
posture; live_exec NEVER writes into BE-8's ledger). NO new broker beyond sanctioned
boundary. NO two-operator claims.

## Review request
ITRGA asks the DA to (1) confirm/refute AM-1..AM-4 amendment text against standing
coupon lineages (BO-citation feasibility), (2) pressure-test the lock-stack: can L1
(mode_locked) mis-fire through a posture-only promenade or is actuation-seam typing
airtight, (3) confirm sub-band sizing/migration ranges (12A 30-40 tests ... 12E 25-35,
0053-0057-class), (4) stress DR-3 honesty clause: is practice + refusal-injection
sufficient witness for capability-complete WITHOUT the LIVE real-network leg,
(5) confirm no shadow outside `docs/arena_spec` (design draw required per seat-book
law for AM-2's mode-contract amendment). REGISTER-as-designed, REFUTE-with-substance,
or AMEND per section. On ADOPT: BO-V2-BE12A-001 opens 12A.
