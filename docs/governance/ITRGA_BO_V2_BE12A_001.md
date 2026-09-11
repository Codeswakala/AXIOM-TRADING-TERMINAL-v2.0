──────────────────────────────────────────────────────────────────────────
BUILD ORDER — V2·BE-12A: LIVE-EXEC INTENTS, ELIGIBILITY, PRE-TRADE RISK, LOCK-ORDER
CHAPTER
POSTURE: builder-capable · execution-authority: NONE (capability-before-activation
under REGISTERED_LOCKED; no funded account exists — R-6.3 register line).

CITATIONS: REQ-V2-BE-12-001 (adopted + amendments) · DR-V2-BE-12-001 (adopted as
amended, DR-F1/§2/§4/DR-F2/DR-F3 absorbed) · OPERATOR ADJUDICATION 2026-09-08 ·
DIRECTION-BE12-001. Objects touched: new `app/v2/live_exec/` modules; AM-1..AM-4
amendment surfaces; migration 0053; tests/test_v2_live_exec_12a*.py. Suite floor:
1,163 (re-tattooed by migration AM-0053 head 20260909_0053).

POINTER LANE (KEEP, AND NO DRIFT, IN EVERY RESPONSE:
   *Alembic chain head AFTER this BO: `20260909_0053` = AMEND-0053 (live_exec
   intents chapter; census re-tattoo law: counts re-enumerated fresh per sub-BO).
   Custom enumerations DRIFT — concrete targets: account_classify None -> None
   change; trading_device None; live_exec component family pins (mode/vault/
   execution adapter stance, register pins) are DR-authored per V2 law. When
   doubt: re-enumerate vs the bytes; NEVER from a memory of an earlier suite state.)

──────────────────────────────────────────────────────────────────────────

1) THE ENGINEERING MISSION (12A only; later sub-ladders are separate BOs)
   a. Package family `app/v2/live_exec/` born with the wall law: no domain
      imports live_exec; live_exec reads projections/bridge engines READ-ONLY;
      live_exec writers may ONLY reach providers through the sanctioned adapter
      boundary package (present in 12A as the POSTURE-STUB — practice actuator
      wiring lands in 12B; in 12A the boundary package EXISTS, is imported, and
      its existence is coupon-verified).
   b. INTENT ENGINE (`intents.py`): uuid chassis; idempotency key; requested basis
      id; posture field; operator-actor + step-up reference shape on confirm writes
      (V2-TD-29 adopted line: SECOND FACTOR not SECOND ACTOR); digest per
      N-O13 per-world (pxs-1.0.0 bound surface) — pins named by bytes.
   c. ELIGIBILITY ENGINE (`eligibility.py`): account + instrument + session
      checks; typed refusals `account_ineligible`, `instrument_ineligible`,
      `session_ineligible`, `basis_stale` (BOP law: Basis must be PRESENT not
      stale); money-units sizing inheritance from BE-11 flat-account law in
      `risk.py` (pre-trade risk evaluation: position-size evaluation surfaces,
      decline verbs typed — this act carries NO live submission).
   d. THE LOCK-ORDER CHOKEPOINT (`locks.py`): `require_actuation(...)` per
      DR-0.75 — single door for all actuating verbs, pinned order L1..L6; in
      12A the verbs ARE evaluation/registration only (no submission — 12B), so
      actuation-seam behavior is coupon-witnessed via test-only promenades and
      the ledger-verified refusal arms; order-fixture coupons (fail L1 AND L3
      → refusal must be `mode_locked`).
   e. AM-1..AM-4 IMPLEMENTATION, verbatim:
      - AM-1: `V2_FORBIDDEN_PERMISSION_MARKERS` gains literal-prefix exemption
        `v2.live_exec.` with must-die boundary tests.
      - AM-2 (DR-F1 law): tuples STAY BYTE-IDENTICAL; NEW
        `REGISTERED_LOCKED_MODES = ("LIVE",)`; `get_mode()` accepts LIVE and
        tags it locked; the ONE superseded coupon `test_mode_rejects_live` is
        replaced BY CITATION in `tests/test_v2_mode.py` with
        `test_mode_live_registered_locked` (constructs; carries locked tag;
        actuation refuses `mode_locked`); NO edit to any byte-pinned boundary
        file (`test_v2_be9_boundaries.py` named expressly).
      - AM-3: `EXECUTION_BACKENDS` extended to 2 keys (`paper`, `live`);
        live entry posture-locked; the len-pinning coupon superseded BY CITATION.
      - AM-4: `practice_trade` credential class in the vault registry —
        behavior stubs + hygiene coupons this act (registration doorway in 12B).
   f. MODE/vault/execution-adapter stances per the live_exec pins ledger
      (operator-authored config-register, matches DA line-pair references,
      exact register line law `BE-12 CAPABILITY-IN-PROGRESS … LIVE mode:
      REGISTERED_LOCKED` — visible in drift/execution-mode payloads).
   g. Migration `20260909_0053` with census re-tattoo (AMEND-0053): creates
      the 12A chapter tables `v2_live_exec_intent`, guard-pair triggers,
      surrogate seeds, per DR-4 floor; NO compver, NO permission, NO
      exception-table entries this act (perm family arrives with 12A's surface
      verbs in the AUTHORIZED surface scope below: POST /live-exec/intents
      (register + evaluate) writes SAL-4; GET intents(+evidence) reads SAL-2
      with register pinning — the surface-scope addition text ships as part of
      amendment-0053's migration deltas in the BO body).

2) COUPON RANGE (12A): 30–40 new; overridable ONLY per the ceremony coupon-budget
   law: if the final stand falls 27–29, BO may still close with a register
   supplement + written rationale; suite floor stairs recited by head-of-line==1,193–1,203.

3) F1 RECITALS: every refusal taxonomy (AM-1..AM-4's crossings included) is DB-side
   recoverable FROM THE REGISTER with CWS discipline — text convertible from REGISTRY
   ids; wall/law-view boundary CSVs stay sworn in artifact; suppressions re-bound
   (015T1–015T3 pairs) per SEAL law from BE-2 before any mutation — BINDING RECITAL
   anyway: binding re-tattoos must CLEAN F2 shadow-zero drift first or name the deltas.

4) ACCEPTANCE (12A CLOSURE COUPONS — the house's heartbeat):
   - AM-1: `v2.live_exec.` family registers; non-prefix writers die; must-die arms stand.
   - AM-2: `test_mode_rejects_live` NOWHERE (superseded by citation — grep-able
     commentary pins the citation); `test_mode_live_registered_locked` pins the
     third state; boundary-file tuples byte-identical (BE-11 byte pin untouched —
     `git status`-class drift check names the byte-pinned wall sha unchanged).
   - AM-3: registry 2 keys; live posture-locked; cited supersession stands.
   - AM-4: `practice_trade` class registers; vault-only; investor class intact.
   - Chokepoint: order fixture coupons (L1-vs-L3, L2-vs-L6, kill-vs-all, etc.);
     `mode_locked` computed ONLY from mode contract (a promenade test proves
     posture inputs cannot manufacture mode answers).
   - Intent ledger: zero-UPDATE regime + guard-pair triggers + surrogate keys;
     enumeration lasers clean; idempotency + duplicate intent refusal.
   - Digest tuples, staleness refusal, eligibility refusals — all first-class,
     CWS-clean, POSITIVE-REASON pair where required.
   - End-of-line: full-room 1,163 + Δ green, `migrate --strict` 0 errors 0 skips,
     rehearsal PASS, band-ITRGA micro-compare (projection of the live_exec chapter
     vs byte repository) green.

5) DELIVERY SHAPE: pptx-styled PR: `BE-12A-API.zip` (chapter lanes only +
   delta suites + migration + spec-registers co-authored) AND console act
   delta-cards per the discipline document; pusps ready in the act.

6) REGISTER MOVES: this BO appends AC12A line "BE-12A INTENTS+RISK
   ENGINEERED-IN-PROGRESS | LIVE=REGISTERED_LOCKED | funded account: NONE" to
   docs/governance/ITRGA_V2_CAMPAIGN_REGISTER-001.md on issuance.
──────────────────────────────────────────────────────────────────────────
