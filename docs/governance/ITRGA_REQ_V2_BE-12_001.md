# REQ-V2-BE-12-001 — BE-12: CONTROLLED LIVE EXECUTION GATEWAY (CAPABILITY-BEFORE-ACTIVATION)
`STATUS: FOR ADJUDICATION — 2026-09-08 — built on OPERATOR DIRECTION — BE-12 Completion Model`
`Register: roadmap §BE-12 scope; ruling (b) numbering in force; citizens: DIRECTION-BE12-001.`

## R-0 — Mission
Engineer the controlled live-execution capability end-to-end as LAW software: every verb
from the roadmap §BE-12 scope present, tested, verified — while every ACTIVATION pathway
remains provably behind its three locks (funded postura, operator LIVE authorization
instrument, kill-switch armed). The band ships a complete capability that cannot legally
fire a live order, because its activation instrument does not exist — not because its
code is incomplete.

## R-1 — Scope declarations
R-1.1 (IN — the full roadmap §BE-12 scope, engineered): order intents; account/
instrument/market-session eligibility; pre-trade risk evaluation; explicit human
confirmation; step-up authorization; broker/execution adapter boundary;
submission; acknowledgement + fill processing; idempotency + duplicates;
cancel/modify where the provider contract supports; unknown-state handling;
reconciliation; kill-switch + emergency controls; execution audit; incident workflows.
R-1.2 (IN — activation boundary as *the product*): a distinct, auditable,
operator-controlled ACTIVATION instrument (human confirmation + step-up + register
act) required to convert POSTURE-LIVE-capable code into LIVE-capable behavior;
the boundary carries its own evidence arms (refusal-on-posture-mismatch as first-
class typed states).
R-1.3 (OUT — hard prohibitions, roadmap-law verbatim): NO live order may originate
from assistant text, model output, signal, chart state, or paper result; no frontend
toggle alone authorizes LIVE; no automatic PAPER→LIVE transition; no real-money
execution under this band (activation = later, separate instrument, R-6.2).
R-1.4 (OUT — THIS BAND DOES NOT ACTIVATE): band completion ≠ production activation.
The Production Certification and funded-account journey are explicitly deferred to a
later constitution instrument. The register will say precisely what that means and
never as a euphemism for "ready."

## R-2 — Verification strategy (capability-complete without a funded live account)
- Practice-world actuator: every dependency exercised live against the practice leg
  (the sealed practice adapter family) with failure-path arms synthesized by refusal-
  injection; every behavioural requirement testable on practice.
- LIVE-mode venue is engineered SO THE CODE IS PROVABLY COMPLETE (typing, wiring,
  walls, unknown-state handling, reconciliation laws) but its venue client stays in
  posture-gated posture; the LIVE leg's real-network behavior is explicitly out-of-
  band and registered as such (never implied-tested).
- All BE-9/BE-11 laws port: no order types in user-facing text; surrogate-error
  discipline CWS; banned-import set grows to refuse ANY broker outside the sanctioned
  boundary package; enumeration-from-projection law for inputs.

## R-3 — Behavioural requirements (testable or no-ship)
R-3.1 Determinism canon per-world; digest over (intent payload, versions, posture, basis id).
R-3.2 Fail-closed battery (first-class typed): posture-mismatch; basis staleness; gateway
decline; kill-switch pulled; duplicate; cancel-on-unknown; unknown-fill-state; session-ineligible.
R-3.3 Idempotency law with the BE-8 anchor; duplicate live-intent never re-fires.
R-3.4 Human-confirmation CANNOT be marked by anything but a human act with step-up
(context: rank-dependent: SAL rank of the confirmer recorded).
R-3.5 Reconciliation: fill/position fx-event parity against the projection model; C-2 clean runs.
R-3.6 Kill-switch: branch-wide, immediate, persisted (not state-in-memory), re-arm blocked until cleared.

## R-4 — Surface floor (design refines)
- POST intents/evaluate/confirm(/cancel-modify) + GET statuses/ledger/reconciliations —
  `v2.live_exec.*`-class permission family, operator-controlled RBAC additions; entire surface
  posture-gated with FIRST-CLASS typed refusals for posture (`live_exec.posture_mismatch`).

## R-5 — Budget & census laws
- Many bands' heaviest; the DR splits BE-12 into explicit sub-acts (12A intents+risk /
  12B submission+fill / 12C cancel-modify+unknown / 12D activation-instrument+kill-switch /
  12E reconciliation+incident workflows), each with its own migration and coupon range.
- Suite floor from 1,163; trigger/perm/compver deltas enumerated in each sub-BO.

## R-6 — Gates constitutional
R-6.1 No single sub-band opens until its predecessor's coupons stand (ordering law).
R-6.2 ACTIVATION INSTRUMENT is its own governance document at the END of the ladder
 (drafted in band; adopted later, separately, only when the Operator elects activation).
R-6.3 The band is testable without a funded account; the funded account remains UNBOUND
 until activation (register line: "funded account: NONE (activation prerequisite)").

## Adjudication request
ADOPT / AMEND / REFUSE per section. Amended wording of R-6.2/R-1.4 is welcomed here,
not later, because these two clauses express YOUR direction's §5/§6; they should say
exactly what you mean before design begins.
