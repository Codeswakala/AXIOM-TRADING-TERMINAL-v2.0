# DA TECHNICAL REVIEW — REQ-V2-BE-12-001 (input to the Operator adjudication)
# AXIOM-V2-BE-12-DA-REQREV-001 · v1.0.0 · 2026-09-08 · AXIOM Trading Terminal v2.0
# Objects: OPERATOR DIRECTION — BE-12 Completion Model (filed md5 `6a6ef76c20627b3f9a7a15071a7dabcc` ·
#   sha256 `bb7642f9…6ff7`) and REQ-V2-BE-12-001 (filed md5 `5f89f3f2399df2664b7b5fe65d1ebcac` ·
#   sha256 `539bf81e…8ca75`)
# Author: Replacement Development Authority (DA)
# Reading rule: adjudication is the OPERATOR'S (ADOPT/AMEND/REFUSE per section).
# DA-side feasibility input only. No ruling made or implied.

---

## §0 — The Direction, acknowledged as the band's constitution

Capability vs activation as SEPARATE STATES is the same law this programme
has been running under other names: BE-11 shipped complete with its seed
slots EMPTY-FORCED — built whole, unable to act until a separate instrument
armed it. BE-12 generalizes that shape to its logical end: **a live-execution
capability whose activation instrument does not exist yet.** The DA can build
under that model; it is the empty-forced law at band scale. The Direction's
own closing line is honored throughout this review: no implementation is
authorized by the Direction alone, and none has begun.

## §1 — FOUR STRUCTURAL COLLISIONS WITH STANDING LAW (survey facts, not objections)

These are not defects in the REQ — they are places where the REQ's mission
**requires amending standing structural law**, and each amendment must be
BO-cited explicitly or the suite will refuse the band on contact. Enumerated
now so the design prices them, not discovers them.

**S-1 · The forbidden-marker wall (permissions).** The standing
`V2_FORBIDDEN_PERMISSION_MARKERS` set contains `live`, `execution`,
`execute`, `order` — the proposed `v2.live_exec.*` family trips the `live`
marker on its face. Unlike BE-11 (which was marker-clean, no exemption
consumed), **BE-12 cannot register a single permission without a new
D-1-class literal-prefix exemption** (`v2.live_exec.` with trailing-dot law +
must-die boundary arms, following the `v2.paper.`/`v2.broker.`/
`v2.account_context.` precedent exactly). This is a one-clause law change but
it is THE gate: the marker wall was built precisely to make this band
impossible to reach by accident. Crossing it deliberately is the point of the
BO; the exemption text should be in the BO verbatim.

**S-2 · The mode contract.** Standing law: `VALID_MODES = ("RESEARCH",
"SIMULATION", "PAPER")`, `DEFERRED_MODES = ("LIVE",)` — LIVE is currently
**unconstructible**, and multiple standing coupons pin that. R-1.2's
capability-before-activation demands LIVE become a *recognized, typed,
posture-gated* mode while remaining *behaviorally locked*. That is a
two-state law the current contract cannot express (it knows only
valid/deferred). The design must introduce a third state — e.g.
`REGISTERED_LOCKED_MODES = ("LIVE",)`: constructible for typing/wiring/wall
proofs, refused at every actuation seam by the posture gate — and every
standing mode coupon that asserts LIVE-unconstructible must be superseded
BO-cited, not silently edited. The DA flags this as the band's deepest
standing-law amendment.

**S-3 · The N2 single-key registry.** BE-8's `EXECUTION_BACKENDS` frozen
registry holds exactly one key (`paper`), and its single-entry-ness is
test-pinned as the N2 isolation mechanism. A live execution leg means a
second key. The registry was DESIGNED to be extended by governance (frozen
MappingProxyType, single registration point) — but the coupon that pins
`len == 1` becomes a coupon that pins `len == 2 AND live-entry
posture-locked`. Same discipline as S-2: supersession by citation.

**S-4 · The credential posture wall.** BE-9 standing operating law:
**investor (read-only) session ONLY; the master password never again on the
AXIOM station.** A submission-capable adapter (R-1.1) eventually requires
trade-capable credentials — which the standing law currently forbids to
exist anywhere the DA's code runs. The REQ's practice-world verification
(R-2) is compatible: a practice-account trade credential is not the funded
master, and the vault (AES-256-GCM/Argon2id, sole-resolution) can hold a new
credential CLASS (`practice_trade`) without touching the investor posture.
But the boundary must be drawn in the design in writing: **which credential
class the practice actuator uses, where it lives (vault-only), and the
register statement that the funded-account credential remains NONEXISTENT
until the activation instrument** (aligning with R-6.3's register line).
The V1 containment guards (MT5/ORDER_TYPE token scans) also need one more
BO-cited allowlist extension for the write-adapter package — the BE-9
precedent covers the form.

## §2 — Section-by-section assessment

| Section | DA assessment |
|---|---|
| R-0 | Sound under the Direction. "Complete capability that cannot legally fire" is buildable with standing machinery: BE-11's empty-forced pattern + BE-8's hold/confirmation seam + BE-9's fail-closed binding precedent, composed. The three locks (funded posture · operator LIVE authorization instrument · kill-switch armed) should each be a TYPED, independently witnessed refusal — three distinct reasons, never one merged `not_activated` |
| R-1.1 | Feasible; the scope list maps 1:1 onto the roadmap §BE-12 scope (verified against the custody roadmap at lines 407–418 — no scope creep, no omission). Topology note: this is a FOURTH package family (`app/v2/live_exec/` or per-sub-band), importing broker_read projections and paper/bridge engines read-only; N3/BE-11 wall pairs stay byte-pinned; a new wall law (no domain imports live_exec; live_exec writers reach brokers ONLY through the sanctioned adapter boundary package) |
| R-1.2 | The activation boundary as product is the band's best idea. DA suggests the boundary carry a SCHEMA arm too, not only code arms: an activation-instrument table whose zero-row state IS the lock (the E-B11-1 doors precedent — "all four doors EMPTY on the fielded DB" was BE-11's strongest evidence; "activation instrument: zero rows" is BE-12's) |
| R-1.3 | Fully enforceable; every named non-origin (assistant text, model output, signal, chart state, paper result) already lives behind existing walls; the coupon form is an origin-witness assert on the intent chassis (operator-actor + step-up ref present, or typed refusal) |
| R-1.4 | The register-truth clause ("never a euphemism for ready") is the wording law applied to the register itself. DA proposes the ed-wording in §4 below |
| R-2 | Correct strategy, one discipline to name: the LIVE leg's real-network behavior is out-of-band and must be registered as **NOT PROVEN (≠ FALSE)** — the exact evidence-class honesty the programme already runs. Practice-leg actuation reuses the sealed BE-9 terminal family; refusal-injection is the E-ENV-1 proxy law generalized |
| R-3.1 | Ports directly (N-O13 per-world; digest tuple gains `posture`) |
| R-3.2 | Eight typed arms enumerated closed — good. Add the S-2 arm explicitly: `mode_locked` (LIVE registered-locked) as distinct from `posture_mismatch` (mode lawful, locks not satisfied). Two different truths, two reasons |
| R-3.3 | BE-8 anchor inherits; the duplicate-live-intent-never-refires law needs the anchor PLUS a submission-side dedupe (ack/fill correlation) — the BE-9 fill-anchor dedupe precedent covers it |
| R-3.4 | Human confirmation with SAL-rank recording: standing chassis exists (BE-8 S2.6 hold seam + `confirmed_by`). Interplay flag: **V2-TD-29** (actor-segregation unenforceable in single-operator reality) — R-3.4 should state whether step-up (a second FACTOR) substitutes for a second ACTOR in this deployment, because the DA cannot test a second human into existence |
| R-3.5 | C-2 clean-runs-evidenced law ports from BE-9 reconcile verbatim |
| R-3.6 | Kill-switch persisted-not-in-memory = one table, guard-pair triggers, zero-UPDATE regime with a single sanctioned clear path; re-arm-blocked-until-cleared is a schema CHECK + typed refusal. Standing discipline fits exactly |
| R-4 | See S-1 (exemption required). Suggest the read family split ranks: writers SAL-4 (highest standing rank in seed data), reads SAL-3/SAL-2 per surface; the confirm verb the highest, since R-3.4 hangs identity on it |
| R-5 | The sub-band split 12A–12E is the right shape and matches how this programme already behaves (band → mini-acts). DA sizing (non-binding, per sub-band): 12A ~30–40 · 12B ~35–45 · 12C ~20–30 · 12D ~25–35 · 12E ~25–35; five migrations 0053–0057-class; suite floor stairs from 1,163 with each sub-BO naming its own deltas. R-6.1 ordering law = the BE-3-phases precedent |
| R-6.2/R-6.3 | Correct and constitutionally clean: draft in band, adopt later, separately. Proposed wording in §4 |

## §3 — DA readiness statement

On ADOPT (with S-1…S-4 carried into the design as explicit BO-cited law
amendments), the DA is ready to produce the BE-12 design document
(12A–12E architecture, the three-lock activation boundary, the credential-
class boundary, the mode-contract amendment text) as the next artifact.
Nothing is built before the BO; nothing in this review starts the clock.

## §4 — Proposed wording (requested by the REQ's adjudication note; Operator may adopt, amend, or discard)

**R-1.4 (amended):** "Band completion means: every verb of the roadmap
§BE-12 scope implemented, coupon-proven, and independently reviewed, with
the activation pathway's three locks each witnessed REFUSING on the fielded
lineage. The register line at closeout reads: `BE-12 CAPABILITY-COMPLETE ·
ACTIVATION INSTRUMENT: NOT IN EXISTENCE · funded account: NONE (activation
prerequisite) · LIVE mode: REGISTERED-LOCKED`. This line is the deliverable.
Production certification and the funded-account journey are separate future
instruments; nothing in this band's completion may be cited as evidence
toward them."

**R-6.2 (amended):** "The ACTIVATION INSTRUMENT is drafted within the band
(12D) as a TEMPLATE artifact — versioned, hash-pinned, and marked
NOT-IN-FORCE on its face. It takes force only when a future Operator
election executes it as its own register act, with its own evidence arms
(funded-posture witness · step-up confirmation · kill-switch armed check),
under whatever additional conditions the governing production instrument
then imposes. Until that act, the template's NOT-IN-FORCE marking is itself
coupon-tested: the capability code refuses activation-shaped inputs citing
the instrument's absence as a first-class typed reason
(`activation_instrument_not_in_force`)."

**We don't guess. We prove.** This band's product is a lock that has been
watched holding — from both sides.

— AXIOM-V2-BE-12-DA-REQREV-001 · v1.0.0 · 2026-09-08
