──────────────────────────────────────────────────────────────────────────
BUILD ORDER — V2·BE-12C: LIVE-EXEC CANCEL/MODIFY + EXPANDED
UNKNOWN-STATE HANDLING (sanctioned boundary, two-lane actuation)
POSTURE: builder-capable · execution-authority: NONE except the PRACTICE
world under the sealed practice leg, and only inside coupons/witnesses
(posture REGISTERED_LOCKED everywhere else; funded account: NONE).

CITATIONS: REQ-V2-BE-12-001 (R-1.1; R-3.2/3.3; R-2; R-6.1 ordering law) ·
DR-V2-BE-12-001 (DR-1 sub-ladder 12C: cancel/modify + unknown-state
handling; DR-0.75 chokepoint law; DR-2 L1..L6; DR-3 refusal-injection) ·
BO-V2-BE12A-001 (12A chapter, accepted) · BO-V2-BE12B-001 (12B chapter,
ACCEPTED + FIELDED at head 20260909_0054 per ITRGA-VERDICT-V2-0054-
FIELDED-001) · ITRGA-REV-V2-BE12B-001 / -CR-001 (finding V2-BE12B-DEL-001
CLOSED; the DEL-001 between-lane class is now STANDING LAW for every new
writer: the corridor is walked by coupons, never assumed) · LAW-BORDER-01 ·
ERRATUM E-0054-A11.4 (drift gate = itemized 9-inherited-V1-token law, never
absolute-silence) · DIRECTION-POSTBE11-001 §1/§7 · C-2 compver disclosure
law · Suite floor: 1,240. Alembic head: 20260909_0054 (FIELDED) → sub-head
target 20260909_0055. Pointer lane: ENUMERATIONS DRIFT — concrete figures
for census/perm/compver deltas are enumerated vs the landed bytes per
sub-BO; when in doubt, re-enumerate, never recite from memory.

──────────────────────────────────────────────────────────────────────────

1) THE ENGINEERING MISSION (12C only; 12D/12E are separate BOs)
   a. PREMISE LOCK + THE VERB LAW: cancel/modify verbs EXIST ONLY where
      the landed provider contract supports them, and the module's
      capability map must be READ BY CITED READ FROM THE LANDED ADAPTER
      (`app/v2/broker_read/providers/*`), never handwritten — OV-001
      pattern-matching counter-law: a verb the adapter cannot evidence
      does not exist in 12C. Scope = ORDER verbs on PENDING/UNKNOWN
      posture only: `cancel_order`, `modify_order` (the contract's
      supported fields only). POSITION verbs are OUT OF SCOPE by charter
      (no position modify, no close-as-modify; a close is a NEW opposite
      submission evaluated under 12B law, not this chapter). Position
      parity reads belong to 12E. Every unsupported-or-misapplied ask
      answers a TYPED refusal, never a partial act: closed vocabulary
      extended at design commit (coupon-pinned closed):
      `modify_not_supported_state` (submission in a terminal state —
      filled/rejected/expired — or verb not in the adapter capability
      map) · `cancel_on_unknown_applied` / `cancel_refused_terminal`
      (terminal's typed refusal mirrored) · `cancel_unknown_outcome`
      (the answer itself unknown) · `unknown_escalate` (escalation
      ARTIFACT typed here; the incident WORKFLOW is 12E's build, not
      this BO's) · `duplicate_modify_event` · plus the 12B practice set
      carried sealed (`practice_posture_absent`, `practice_mode_not_armed`,
      `basis_stale`, `actuation_lane_mismatch`) and the 12A LIVE set
      carried untouched.
   b. CANCEL/MODIFY CHASSIS (`modify/` package + api verbs):
      POST `/v2/live-exec/submissions/{submission_id}/cancel` and
      `/modify` (SAL-4) — each act gated through the SAME door chain as
      12B submit: target intent/submission exists and correlates;
      eligibility per 12A engines where applicable; the PRACTICE lane
      door; envelope carries the actuation answer. APPEND-ONLY LAW: every
      act persists exactly one row in `v2_live_exec_modify_event`
      (zero-UPDATE; uuid pk; submission-intent correlation; verb CHECK
      ('cancel','modify'); request payload; outcome closed CHECK;
      correlation_ref; actor/data_class/mode per house shape; created_at)
      — parent `v2_live_exec_submission`/`v2_live_exec_fill_event` rows
      are NEVER mutated by 12C (coupon: parent tables byte-stable across
      modify acts — count + digest-set pinned equal before/after).
      Idempotency 12A-inherited: same idempotency key, or same
      (submission, verb, payload digest), answers `duplicate_modify_event`
      + standing row cited; an act never re-fires. The R1 DOORWAY LAW
      rides unchanged (passphrase read at request time INSIDE vault.py
      only; absent provisioning ⇒ ABSENT ⇒ P3 typed — never an exception
      carrying material, never a module/app-state secret).
   c. UNKNOWN-STATE SEMANTICS (expansion of the 12B first-class citizen):
      timeout/no_answer/quarantined_unknown postures MAY be met with
      cancel-on-unknown — an OPERATOR-INITIATED recovery act (API verb,
      own idempotency key). GOVERNANCE DEFAULT IS FAIL-CLOSED: posture
      QUARANTINE-HOLD (no auto-acts, no background self-activity —
      N4/N-O11 law: the machine never issues cancel/modify on its own
      initiative); cancel-on-unknown executes ONLY under an explicit
      operator election surfaced in the request and recorded on the row.
      The act's answer is typed per the closed set in §1.a (applied /
      refused_terminal / unknown_outcome → `unknown_escalate`). A timeout
      remains a state transition, NEVER an exception from the seam
      (BE-8 S2.4 preimage law). Matrix coupons cover every cell of
      (posture × election) × outcome; unreachable cells are refusal-
      pinned, not silently absent.
   d. TWO-LANE LAW UNCHANGED AND NON-COMMUTING: verb reachability exists
      ONLY on the PRACTICE lane (wired + provisioned + mode PAPER); the
      LIVE door still answers the 12A locks (L1 `mode_locked` per S-2,
      L2 `posture_mismatch`) with L6 proxied downstream subclasses; a
      practice-lane ask answered by a LIVE-lane reason (or vice-versa)
      = defect (coupon-pinned both directions, 12B corpus extended).
   e. DEL-001-CLASS DEFENSE (standing law since V2-BE12B-DEL-001): every
      NEW writer this BO introduces gets an API-LEVEL border coupon WITH
      COUNTER-ARM — armed-pass full-chain cancel AND modify on PAPER over
      the real corridor (sealed vault + provisioning + injected fake
      terminal family, per 12B CR-1 R2 pattern), NEVER fixture-injection-
      only evidence; counter-arms: vault removed ⇒ P3 typed; provisioning
      absent ⇒ ABSENT. LAW-BORDER-01 extended: one such coupon per new
      guard-tabled writer over the alembic-applied chain (cancel and
      modify each), plus the level-I table coupons.
   f. REFUSAL-INJECTION BATTERY (DR-3 law, 12C set): no credential;
      non-wired boundary; mode not armed; stale basis; submission in
      terminal state (both verbs) ⇒ `modify_not_supported_state`;
      cancel-on-unknown matrix; duplicate modify; LIVE-lane ask ⇒ L1/L2
      exact, never a practice lane word; terminal unreachable ⇒ typed
      transport subclass (L6), never an untyped 500.
   g. MIGRATION `20260909_0055` (AMEND-0055): +1 table
      (`v2_live_exec_modify_event`) + its guard pair (+2 triggers →
      census 86) + indexes (`ix_v2_lxmod_created`, `uq_v2_lxmod_identity`)
      +2 permissions ENumerated fresh (`v2.live_exec.modify.write` SAL-4;
      `v2.live_exec.modifies.read` SAL-2 → 77) +1 compver row INSERT-ONLY:
      `live_exec_engine|lxe-1.1.0` whose source_hash = rolling hash over
      the EXPANDED lxe file set (the six + the 12C `modify/` files;
      set enumerated at design commit and DISCLOSED in the delivery
      report per C-2). The append-only registry law: `lxe-1.0.0`'s row
      STANDS; the update path is refused by design (the guard is
      coupon-witnessed refusing it). ONE upgrade line; census re-tattoo
      target **86/77/15** (base 84/75/14 + addon, enumerated fresh
      pre-commit); DOWNGRADE EXACT (restores 84/75/14; compver row
      removed via the 0054-proven delete-guard dance; new triggers,
      indexes, table, perms removed; expected refusal literal documented
      as in 0054). Drift gate: ITEMIZED law as amended (exactly the 9
      inherited V1 tokens; ZERO 12C tokens).

2) COUPON RANGE (12C): 22–32 new. Head-of-line after close: 1,240 +
   Δ(22..32) = 1,262..1,272. LAW-BORDER-01 as extended in §1.e in force.
   Compver/perm deltas named in the migrated coupon set, coupon-verified
   exact.

3) F1 RECITALS: every refusal id in this sub-band is REGISTER-recoverable
   with CWS discipline; lane language always typed separable; the closed
   vocabularies (verb set, outcome set, refusal set over both lanes) are
   ENUMERATED AT DESIGN COMMIT and coupon-pinned closed. Binding
   re-tattoos clean F2 shadow first.

4) ACCEPTANCE (12C CLOSURE CLAUSES):
   - Verb law: capability map provably read from the landed adapter by
     cited read (coupon names the adapter file/line; a handwritten map =
     defect). Position verbs absent by charter with refusal-pins proving
     absence.
   - Append-only: parent tables byte-stable across cancel/modify acts
     (count + digest-set equal); every act one row; duplicate typed and
     non-firing; intent/submission cannot be re-verbed silently.
   - Unknown-state matrix fully typed (every cell); quarantine-hold
     default; cancel-on-unknown only under recorded operator election;
     `unknown_escalate` artifact typed (12E workflow NOT built here —
     coupon asserts absence-with-pin, not presence).
   - Two-lane non-commutation coupons extended; L1/L2 exact LIVE answers.
   - DEL-001 defense: ≥2 NEW API-path armed coupons (cancel AND modify)
     over the real corridor + counter-arms (P3 typed on vault removal /
     absent provisioning). Injection-only full-pass evidence is not
     acceptance-grade for any new writer.
   - Migration: one upgrade line; 86/77/15; lxe-1.1.0 insert-only with
     C-2 disclosure; lxe-1.0.0 preserved; downgrade exact with the
     delete-guard dance; drift itemized (9 inherited V1, zero 12C).
   - Full-room suite green at 1,262..1,272; micro-compare green.
   - JURISDICTION NOTE (DIRECTION-POSTBE11-001): coupon-verified PRACTICE
     acts in TEST worlds are sufficient. A REAL-WIRE cancel/modify demo
     through the live terminal is NOT acceptance-required and, if desired,
     is its own separately-authorized register act (as V2-TD-30).

5) DELIVERY SHAPE: REM-001 source transcript (changed files only) +
   fail-first witness + full suite transcript + OBS-E-class witness for
   each new writer + failure-witness artifacts + migration witness;
   register line on all envelopes stays the standing form, closing at:
   `BE-12C CANCEL/MODIFY+UNKNOWN-STATE | PRACTICE=WIRED |
   LIVE=REGISTERED_LOCKED | funded account: NONE`.

6) REGISTER MOVES: on issuance, campaign register appends AC12C:
   "BE-12C ISSUED | verbs law (adapter-cited capability) | cancel-on-
   unknown typed matrix | 0055 target | suite floor 1,240 → head-of-line
   1,262..1,272".

──────────────────────────────────────────────────────────────────────────
ITRGA — issued 2026-09-09. This order authorizes no production/live-
network behavior; execution-authority remains NONE except the PRACTICE
world under the sealed leg inside coupons/witnesses. On completion the
INT review runs under the 16-section house template with finding IDs
V2-BE12C-DEL-NNN.
