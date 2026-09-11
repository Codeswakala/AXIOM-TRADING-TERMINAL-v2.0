──────────────────────────────────────────────────────────────────────────
BUILD ORDER — V2·BE-12B: LIVE-EXEC SUBMISSION, ACK/Fill PROCESSING,
PRACTICE ACTUATOR WIRING (sanctioned boundary, two-lane actuation)
POSTURE: builder-capable · execution-authority: NONE except the PRACTICE
world under the sealed practice leg, and only inside coupons/witnesses
(posture REGISTERED_LOCKED everywhere else; funded account: NONE).

CITATIONS: REQ-V2-BE-12-001 (R-1.1; R-3.2/3.3; R-2; R-6.1 ordering law) ·
DR-V2-BE-12-001 (sub-ladder 12B: submission·ack·fills; adapter boundary
practice wiring; DR-0.75 chokepoint law; DR-2 L1..L6; DR-3 refusal-injection) ·
BO-V2-BE12A-001 (standing 12A chapter, accepted + CR-1) · LAW-BORDER-01 ·
DIRECTION-POSTBE11-001 §1/§7 (no practice trading activity at this stage). ·
Suite floor: 1,202. Alembic head: 20260909_0053 (fielded) → sub-head target
20260909_0054. Pointer lane: ENUMERATIONS DRIFT — concrete figures for
census/perm/compver deltas are enumerated vs the bytes per sub-BO; when in
doubt, re-enumerate, never recite from a memory of an earlier suite state.

──────────────────────────────────────────────────────────────────────────

1) THE ENGINEERING MISSION (12B only; 12C/12D/12E are separate BOs)
   a. PREMISE LOCK: no production/live-network behavior anywhere;
      the practice leg is the ONLY actuating world this sub-band may
      reach. The chokepoint speaks TWO LANES now:
        - LIVE lane (exactly the 12A door, unchanged: six locks incl.
          activation instrument + funded posture; nothing reaches it);
        - PRACTICE lane (typed `practice_*` vocabulary closed; refusal
          types enumerated at design commit: e.g., `practice_posture_absent`
          = no resolved practice_trade credential; `practice_boundary_not_wired`;
          `practice_mode_not_armed` = mode not PAPER; `basis_stale`;
          `actuation_lane_mismatch`; the LIVE-lane refusals stay untouched).
      The two lanes' refusals may never commute: a practice-lane ask
      answered by a LIVE-lane reason (or vice-versa) = defect (coupon-pinned).
   b. ADAPTER BOUNDARY WIRING (the 12A stub, moved by citation):
      `adapter_boundary.py` stance literal updated `posture_stub` →
      `practice_wired` BY CITED EDIT (supersession coupon names the BO);
      the boundary gains the PRACTICE submission path — reaching the
      terminal family ONLY via the sanctioned BE-9 provider leg
      (`app/v2/broker_read/providers/*`), never directly; wall coupon
      amended by citation (package-wide provider-token ban now reads:
      banned everywhere in the package EXCEPT inside
      `adapter_boundary.py`; amended wall coupon = both directions
      still scanned, exception scoped to the one file by name-literal).
   c. SUBMISSION CHASSIS (`submissions.py` + api verbs): POST
      `/v2/live-exec/intents/{intent_id}/submit` (SAL-4) — writer is
      migrate-gated: input intent must exist, eligible per 12A engines,
      AND pass the PRACTICE lane door; envelope carries the actuation
      answer; idempotency 12A-inherited: a submitted intent never
      re-submits (typed `duplicate_submission`, standing row cited);
      submission event persisted under zero-UPDATE law.
   d. ACK + FILL PROCESSING (`ack_fills.py`): terminal-returned ack
      captured {server_ack_ref, terminal_state}; fill events correlated
      to submissions by (server_ack_ref or terminal-order identifier);
      DE-DUPE anchored on fill-event identity (BE-9 election-derived
      dedupe law — fills are never double-attributed; second sighting
      of the same fill event = typed `duplicate_fill_event` + standing id);
      UNKNOWN states FIRST-CLASS typed (timeouts/retcode absences →
      `quarantined_unknown` per BE-8 S2.4 preimage law; a timeout is a
      state transition to quarantine, NEVER an exception from the seam);
      tables `v2_live_exec_submission`, `v2_live_exec_fill_event` with
      guard-pair triggers, surrogate uuid pks, closed CHECK vocabularies.
   e. AM-4 PRACTICE_TRADE DOORWAY (`vault.py` milestone):
      `resolve_practice_trade_credential()` moves from ABSENT stub to
      real SEALED resolution BY CITED EDIT — own sealed payload file
      (salt+nonce+AES-256-GCM, class field pinned "practice_trade";
      path env `AXIOM_BROKER_PRACTICE_VAULT_PATH`, OUTSIDE the repo;
      absent env/file → ABSENT, never an exception carrying material);
      REGISTRATION acts remain operator-console RECORDS-OF-INTENT
      (no credential plaintext ever travels any API); the standing
      investor class + read-only operating law untouched (coupon-pinned:
      reading investor payload cannot manufacture practice resolution).
   f. REFUSAL-INJECTION BATTERY generalized (DR-3 law): refusal-injection
      probes for every practice-lane arm (no credential; non-wired
      boundary; mode not armed; stale basis; terminal unreachable;
      retcode-absent timeout → quarantine; duplicate fill; double-submit).
   g. MIGRATION `20260909_0054` (AMEND-0054): +2 tables
      (`v2_live_exec_submission`, `v2_live_exec_fill_event`) + their
      guard pairs +2 triggers; permission additions ENumerated fresh
      (submission writer SAL-4; fills/submissions reads SAL-2 — count
      pinned at design commit, coupon-verified); compver row for
      `lxe-1.0.0` LANDS HERE (BO-cited: the 12A-deferred engine row,
      added exactly once); ONE upgrade line; census re-tattoo (head
      figures enumerated fresh pre-commit; base-line 80/72/13 + addon).

2) COUPON RANGE (12B): 35–45 new; LAW-BORDER-01 in force (one API-level
   coupon per NEW guard-tabled writer over the alembic-applied chain —
   meanings: the submit endpoint and any fill/ack write path each get a
   border coupon in this same BO). Expected suite head-of-line after
   close: 1,202 + Δ(35..45) = 1,237..1,247. Compver/perm deltas named
   in the migrated coupon set, coupon-verified as exact.

3) F1 RECITALS: every refusal id in this sub-band is REGISTER-recoverable
   with CWS discipline; the LIVE-vs-PRACTICE lane language must always be
   typed separable (coupon: the full ACTIVE refuse set over both lanes,
   enumerated closed). Binding re-tattoos clean F2 shadow first.

4) ACCEPTANCE (12B CLOSURE CLAUSES):
   - Two-lane chokepoint coupons: lane answers never commute; LIVE-lane
     refusal set still exact from 12A; practice-lane set enumerated closed.
   - Boundary wiring: stance practice_wired by cited edit; amended wall
     coupons hold both directions with the one-file exception pinned;
     no other package file may speak a provider token.
   - Vault doorway: real resolution only with the sealed file present;
     everything else ABSENT; investor law/payload untouched (pin coupons);
     registration console-act posture (no API credential surface) stands.
   - Submission: writer gated through the practice lane; persisted under
     zero-UPDATE; duplicate_submission typed; intent cannot re-fire.
   - Acks/fills: correlation law + DE-DUPE anchored; unknown-state to
     `quarantined_unknown`, never exceptions from the seam.
   - Migration: one upgrade line; census re-tattooed; downgrade exact;
     drift gate names only inherited V1 set.
   - Full-room suite green at 1,237..1,247; micro-compare (projection of
     the 12B chapter vs byte repository) green.
   - JURISDICTION NOTE (DIRECTION-POSTBE11-001): coupon-verified PRACTICE
     submissions in TEST worlds are sufficient for acceptance. A REAL-WIRE
     demo submission through the live terminal is NOT required for this
     BO's acceptance and, if later desired as a campaign witness act,
     requires SEPARATE operator authorization as its own register act —
     the same discipline as V2-TD-30. (12B's evidence plan does not lean
     on manual practice trading.)

5) DELIVERY SHAPE: REM-001 source transcript (changed files only) + full
   suite transcript + OBS-E-class witness for the practice-wire + failure
   witness artifacts + migration witness; register line on all envelopes
   stays the 12A form with sub-band posture updated at close:
   `BE-12B SUBMISSION+FILLS | PRACTICE=WIRED | LIVE=REGISTERED_LOCKED |
   funded account: NONE`.

6) REGISTER MOVES: on issuance, campaign register line appends AC12B
   "BE-12B ISSUED | practice lane two-door law | 0054 target | suite
   floor 1,202 → head-of-line 1,237..1,247".
──────────────────────────────────────────────────────────────────────────
