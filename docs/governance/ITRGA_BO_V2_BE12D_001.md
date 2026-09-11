──────────────────────────────────────────────────────────────────────────
BUILD ORDER — V2·BE-12D: ACTIVATION INSTRUMENT + KILL-SWITCH
(sanctioned boundary; LIVE gate machinery; force NEVER taken)
POSTURE: builder-capable · execution-authority: NONE — the activation
instrument NEVER takes force in this chapter (no force-verb is built,
ever); the kill-switch machinery is constructed, armed/cycled only in
COUPON worlds and by operator verbs in the corridor witnesses. Register
posture everywhere else: ACTIVATION INSTRUMENT NOT IN FORCE; LIVE=
REGISTERED_LOCKED; funded account: NONE.

CITATIONS: REQ-V2-BE-12-001 (R-1.1; R-3.2/3.3; R-2; R-6.1 ordering law) ·
DR-V2-BE-12-001 (DR-0.75 chokepoint; DR-1 sub-ladder 12D; DR-2 L3/L5;
DR-4 surface floor; DR-5/DR-6 posture) · BO-V2-BE12A/12B/12C (predecessor
chapters CLOSED: 12A FIELDED+WIRE-PROVED · 12B FIELDED · 12C FIELDED at
head 20260909_0055 per ITRGA-VERDICT-V2-0055-FIELDED-001) · DEL-001-class
defense standing law (every new writer walked by armed coupons +
counter-arms) · LAW-BORDER-01 (extended §1.f) · ERRATUM E-0054-A11.4
(drift gate = ITEMIZED 9-inherited-V1-token law, never absolute-silence)
· ERRATUM E-0055-A10.3 (refusal-text pins taken from RENDERED DDL names —
ck_<table>_<short>; pre-verified on rehearsal render before the field
act) · DIRECTION-POSTBE11-001 §1/§7 · C-2 compver disclosure law ·
N4/N-O11 (no self-activity of any kind) · Suite floor: 1,265. Alembic
head: 20260909_0055 (FIELDED) → sub-head target 20260909_0056. Pointer
lane: ENUMERATIONS DRIFT — the census/perm/compver figures below are
enumerated vs landed bytes; when in doubt, re-enumerate, never recite.

──────────────────────────────────────────────────────────────────────────

1) THE ENGINEERING MISSION (12D only; 12E is a separate BO)
   a. PREMISE LOCK — ACTIVATE-NOTHING LAW: nothing in this chapter arms,
      pulls, clears, or takes force on the machine's own initiative. Every
      state transition of either artifact is an OPERATOR-INITIATED VERB
      with an actor and — on each confirm-rank verb — a step-up reference
      (DR-2 carriage: second FACTOR, never second actor; no two-operator
      claims). Absence of the step-up reference answers the chassis's
      standing step-up typed refusal (enumerated at design commit, carried
      sealed — never a new untyped shape).
   b. THE ACTIVATION INSTRUMENT (`activation/` package):
      b.1 THE TABLE IS THE FORCE SWITCH: `v2_live_activation_instrument`
          — zero-row == L3 `activation_instrument_not_in_force` (the
          12A lock's schema arm, now brought into existence AS SCHEMA).
          Row shape: surrogate uuid pk; `sole` discriminator CHECK
          ('SOLE') + UNIQUE index (at most one row may ever exist);
          `version` closed CHECK (enumerated: 'lai-1.0.0' only);
          `template_hash`; authority-reference columns
          (funded_posture_ref, step_up_ref, operator refs, correlation
          refs); regime block (actor_id, data_class, mode, operator_id,
          created_at). **`data_class` CHECK = single member
          ('live_marker')** — the coupon/test worlds' own law
          ('simulated') is structurally BANNED from this table, so no
          test fixture can ever simulate force. Guard pair
          (UPDATE/DELETE triggers, house messages: `V2 live activation
          instrument is immutable; UPDATE/DELETE prohibited`).
      b.2 THE TEMPLATE ARTIFACT is the instrument's extant form:
          versioned (`lai-1.0.0`), hash-pinned (coupon recomputes the
          artifact hash from final bytes — C-2-family discipline), and
          **NOT-IN-FORCE ON ITS FACE**: the template text itself DECLARES
          non-force (its own opening clause states it confers no
          activation; taking force is a future register act requiring
          funded-posture witness + step-up + kill-switch check —
          pinned text, coupon-witnessed substring). The artifact is
          READ-ONLY data in `activation/template.py`; the coupons prove
          (i) the declaration is present, (ii) the hash stands against
          the landed bytes, (iii) NO code path exists anywhere in the
          band that INSERTS into the instrument table (absence-with-pin:
          token scan over the band + API surface enumeration shows no
          writer route).
      b.3 SURFACE (DR-4 floor): GET `/v2/live-exec/activation`
          (SAL-2) — the force-row state (zero-row ⇒ the typed
          not-in-force shape on the envelope face, never an error);
          GET `/v2/live-exec/activation/template` (SAL-3) — the draft
          template body with version + hash echoed on the envelope.
          BOTH read-only. There is NO POST/PUT/DELETE route against the
          instrument in this BO (taking force = future register act =
          own build order).
      b.4 THE L3 WITNESS: the 12A door's lock ORDER is UNCHANGED (coupon
          recites LOCK_ORDER exact — the L1..L6 tuple does not move);
          12D wires the FACT READER for `activation_instrument` (the
          row count) from schema truth over the real chain: engine
          coupon — rows=0 ⇒ `activation_instrument_not_in_force` typed
          at position 3 (L1, L2, L3-bypass constructed under coupon
          facts only); ORDER coupon — fixture failing L1 AND L3 answers
          `mode_locked` (order law re-proven over the real schema). A
          coupon-world armature proof MAY insert the future-lawful
          row SHAPE (data_class 'live_marker', sole 'SOLE', version
          'lai-1.0.0', valid hash) in-transaction and witness the lock
          evaluate in-force — ROLLED BACK, never committed; this proves
          the armature behaves as designed for a hypothetical sanctioned
          row WITHOUT taking force anywhere.
   c. THE KILL-SWITCH (`killswitch/` package):
      c.1 TABLE `v2_live_kill_switch` — singleton sole-row shape (CHECK
          sole='SOLE' + UNIQUE); closed status CHECK IN
          ('armed','pulled','cleared'); regime block; data_class CHECK
          = ('evidence') single member (the switch is an authority/
          evidence artifact, never trade data; 'simulated' BANNED).
          Guard pair (UPDATE/DELETE prohibited) — PLUS **the single
          sanctioned VALVE**: the ONLY legal transitions are executed by
          the three governor verbs, each wrapped in the house DANCE
          pattern proven by the compver delete-guard (drop the UPDATE
          guard → perform exactly one transition → recreate the guard →
          verify restored, hard-fail the transaction otherwise). Any
          transition attempted OUTSIDE the valve = guard refusal typed;
          that inversion is coupon-witnessed (direct SQL update ⇒
          REFUSED; valve transition ⇒ allowed exactly once).
      c.2 LIFECYCLE LAW (append-witnessed, coupon-pinned every cell):
          arm (no row ⇒ INSERT 'armed') · pull ('armed' ⇒ valve ⇒
          'pulled') · clear ('armed'|'pulled' ⇒ valve ⇒ 'cleared') ·
          re-arm ('cleared' ⇒ valve ⇒ 'armed'). **RE-ARM WHILE
          'armed'|'pulled' ⇒ typed refusal `killswitch_armed`,
          non-firing** (DR-1 law: re-arm blocked until cleared) — the
          engine pre-read types it; the singleton UNIQUE is the
          schema-fatal backstop. Pull when not 'armed' ⇒
          `killswitch_state_invalid` typed. Clear when no row ⇒
          `intact` no-op shape typed (the verb answers the standing
          state, never invents one). Each transition stamps
          actor/step_up/operator refs (R-3.4 carriage).
      c.3 L5 WIRING: the 12A door's `killswitch_armed` lock (position 5)
          reads the sole-row status via the 12D fact reader: no row or
          'cleared' ⇒ NOT armed; 'armed'|'pulled' ⇒ armed. Engine
          coupons cover all four states of the sole row; order law
          re-recited (LOCK_ORDER tuple UNCHANGED). The L5 fact reader
          rides the real chain in the border coupon (§1.f), never a
          fixture-only proof.
      c.4 SURFACE (DR-4 floor; confirm = HIGHEST rank):
          POST `/v2/live-exec/killswitch/arm` (SAL-4 + step-up) ·
          POST `…/pull` (SAL-4 + step-up) · POST `…/clear` (SAL-4 +
          step-up; THE single sanctioned clear path — no other clear
          exists anywhere, coupon-scanned) · GET `…/killswitch`
          (SAL-2 — standing state; zero-row shape typed, never error).
   d. LANE NON-COMMUTATION UNDER THE NEW MACHINERY: the kill-switch and
      activation artifacts are LIVE-GATE law ONLY. **The PRACTICE lane
      must NEVER consult them**: PRACTICE_LOCK_ORDER stays exactly five
      members (recited); a coupon arms/pulls the switch in-coupon-world
      and proves a lawful PRACTICE act still refuses with 12B/12C
      practice vocabulary ONLY when degraded and still PASSES when lawful
      — the switch/instrument state may not leak into the practice lane
      by any refusal word. Conversely the LIVE door's answers stay L1–L6
      vocabulary only. THE LANES' REFUSALS STILL NEVER COMMUTE, now
      under an armed switch.
   e. CLOSED VOCABULARIES (12D extension, enumerated at design commit,
      coupon-pinned closed, CWS-register-recoverable): the two NEW
      refusal ids — `killswitch_state_invalid` (plus `killswitch_armed`
      reused as the arm-while-engaged refusal — the SAME token as the
      L5 lock, by design) — are DISJOINT from the practice lane (5), the
      12C act set (9), and each other; L3/L5 tokens (
      `activation_instrument_not_in_force`, `killswitch_armed`) REMAIN
      pure LIVE-lane members (LOCK_ORDER unchanged). F1 recital coupon:
      full active refuse set over LIVE (6) + PRACTICE (5) + ACTS (9) +
      12D GOVERNOR refusals, closed and exactly-overlapping ONLY at the
      two lock tokens as declared here.
   f. DEL-001-CLASS DEFENSE (standing law; LAW-BORDER-01 extended):
      every NEW governor writer (arm / pull / clear) gets API-LEVEL
      border coupons over the real alembic-applied chain WITH
      COUNTER-ARMS — the full witness cycle in ONE border: arm 200 ⇒
      GET shows armed (L5 fact reader proves armed over the real
      schema) ⇒ pull 200 ⇒ re-arm ⇒ 409 `killswitch_armed` (non-firing;
      no row mutation; valve never opened) ⇒ clear 200 ⇒ re-arm 200 ⇒
      lifecycle stands CLEARED→ARMED end state. Counter-arms: permission
      absent ⇒ 403 family typed; step-up absent ⇒ chassis step-up
      refusal; pull-before-arm ⇒ `killswitch_state_invalid`; direct-SQL
      mutation ⇒ guard refusal (never the valve). Level-I: guard pair
      fires; dance leaves guard VERIFIED-restored after each verb;
      tables roll back to zero rows in the field (witness §5). The
      activation table's absence-of-writer is proven by surface
      enumeration + token scan (§b.2.iii).
   g. MIGRATION `20260909_0056` (AMEND-0056): +2 tables
      (`v2_live_activation_instrument`, `v2_live_kill_switch`) + guard
      pairs (+4 triggers) + singleton/discriminator indexes + closed
      CHECKs per §b.1/§c.1 (+6 permissions enumerated fresh:
      `v2.live_exec.killswitch.arm`, `.pull`, `.clear` SAL-4;
      `v2.live_exec.killswitch.read` SAL-2; `v2.live_exec.activation.read`
      SAL-2; `v2.live_exec.activation.template.read` SAL-3) +1 compver
      row INSERT-ONLY `live_exec_engine|lxe-1.2.0` over the EXPANDED lxe
      set (the eight 12C-set files + `activation/{__init__,engine,
      template}.py` + `killswitch/{__init__,engine}.py` — set enumerated
      at design commit, DISCLOSED per C-2; note template.py rides the
      hash so the instrument artifact is compver-scoped). Append-only
      registry law: `lxe-1.0.0` AND `lxe-1.1.0` rows STAND; update path
      refused (guard live-witnessed). ONE upgrade line; census re-tattoo
      target **90/83/16** (base 86/77/15 + §g deltas, RE-ENUMERATED
      pre-commit); DOWNGRADE EXACT (restores 86/77/15; delete-guard
      dance; 1.0.0/1.1.0 preserved). **CHECK-name pins in every card/
      probe carry the RENDERED form (`ck_<table>_<short>`) per
      E-0055-A10.3 law, pre-verified on the rehearsal render.** Drift
      gate: ITEMIZED (exactly the 9 inherited V1.0-table tokens; ZERO
      12D tokens).

2) COUPON RANGE (12D): 22–32 new. Head-of-line after close: 1,265 +
   Δ(22..32) = 1,287..1,297. The supersession mechanism rides: the 12C
   corpus's exact register-line pin (`test_register_line_12c_form…`) is
   superseded BY CITATION; the 12D corpus carries the new exact-form pin
   and the lanes structural-invariants pin stands unchanged. Compver/
   perm/census deltas coupon-verified exact.

3) F1 RECITALS: every refusal id REGISTER-recoverable with CWS
   discipline; lane language separable (§1.d/§1.e coupons); closed
   vocabularies pinned at design commit; binding re-tattoos clean F2
   shadow first.

4) ACCEPTANCE (12D CLOSURE CLAUSES):
   - Activate-nothing law: every transition operator-initiated, actor +
     step-up stamped, no timer/scheduler/script path exists (absence-
     with-pin coupons + token scans).
   - Force switch: table zero-row ⇒ L3 typed over the real chain;
     template versioned/hash-pinned/NOT-IN-FORCE on its face; NO writer
     route exists anywhere (enumeration + scan); simulated-class rows
     structurally impossible (single-member data_class CHECK);
     armature proof coupon-world-only, rolled back.
   - Kill switch: singleton + closed cycle; valve is the ONLY
     transition path and its dance is witnessed verified-restored;
     re-arm blocked typed; pull-before-arm typed; clear is THE single
     sanctioned path; L5 reads sole-row truth over the real corridor.
   - Lane law: practice lane vocabulary/coupons untouched by switch or
     instrument state (coupon-proven arms while switch engaged + while
     force-absent); LOCK_ORDER byte-recital unchanged.
   - DEL-001 defense: the governor cycle border with counter-arms runs
     over the real corridor; no injection-only evidence for any writer.
   - Migration: one line; 90/83/16; lxe-1.2.0 insert-only + C-2; both
     prior rows stand; downgrade exact; CHECK pins in RENDERED form
     (E-0055-A10.3); drift itemized (E-0054-A11.4).
   - Suite green at 1,287..1,297; micro-compare green.
   - JURISDICTION NOTE (as carried): coupon-verified + corridor-
     witnessed acts are acceptance-grade; NO real-network activation
     act of any kind is performed or required — the instrument NEVER
     takes force in this chapter; any future force-taking is its own
     register act under a future build order.

5) DELIVERY SHAPE: REM-001 source transcript (changed files only) +
   fail-first witness + full suite transcript + OBS-E-class witness for
   each new governor writer + failure-witness set + migration witness;
   register line on all envelopes closes at:
   `BE-12D ACTIVATION-INSTRUMENT+KILL-SWITCH | LIVE=REGISTERED_LOCKED |
   funded account: NONE | activation instrument: NOT IN FORCE`.

6) REGISTER MOVES: on issuance, campaign register appends AC12D:
   "BE-12D ISSUED | force NEVER taken (no force-verb) | kill-switch
   singleton + sanctioned valve dance | L3/L5 fact readers schema-wired |
   0056 target | suite floor 1,265 → head-of-line 1,287..1,297".
   Carry-forwards UNMOVED (12E band): DR-F2 conversion law · honesty
   pair · counterfeit-witness scan · compver rows with last build ·
   LOW-2 (SELECT-then-insert concurrency note).

──────────────────────────────────────────────────────────────────────────
ITRGA — issued 2026-09-09. This order authorizes no production/live-
network behavior; execution-authority remains NONE; the activation
instrument NEVER takes force under this order; the kill-switch cycles
only inside coupon worlds and corridor witnesses. On completion the INT
review runs under the 16-section house template with finding IDs
V2-BE12D-DEL-NNN.
