# AXIOM — ITRGA INDEPENDENT REVIEW
# V2-BE-12A — LIVE-EXEC INTENTS, ELIGIBILITY, PRE-TRADE RISK, LOCK-ORDER CHAPTER

**Review ID:** `ITRGA-REV-V2-BE12A-001`
**Version:** `v1.0.0`
**Date:** `2026-09-08`
**Authority:** `ITRGA`
**Requirement:** `REQ-V2-BE-12-001 (ADOPTED + amendments absorbed; Operator Adjudication 2026-09-08)`
**Design Record:** `DR-V2-BE-12-001 (ADOPTED AS AMENDED 2026-09-08; five answer-laws incl. DR-F1 + LOCK-ORDER)`
**Build Order:** `BO-V2-BE12A-001`
**Delivery Report:** `AXIOM-V2-BE-12A-DR-001`
**Status:** `REVIEW`

---

# 1. REVIEW PURPOSE

Independent review and verification of the BE-12A delivery against its Build Order:
package birth + wall law · intent engine · eligibility + pre-trade risk · LOCK-ORDER
chokepoint · standing-law amendments AM-1..AM-4 · migration `20260909_0053` · coupon
battery (BO range 30–40) · the register line as fielded evidence shape. Judged only
from the marshalled evidence; no implementation implied.

---

# 2. REVIEW AUTHORITY

Governing documents and sections applied:

- `REQ-V2-BE-12-001` R-0..R-6 + Operator Adjudication amendments (S-1..S-4; R-1.4/R-6.2
  DA wording adopted verbatim; V2-TD-29 single-operator line; R-3.2 + mode_locked/
  posture_mismatch distinction).
- `DR-V2-BE-12-001` DR-0..DR-6 as amended: AM-1..AM-4 implementation laws (incl. the
  DR-F1 byte-pin law), DR-0.75 LOCK-ORDER chokepoint law, DR-3 verification-honesty
  pair, DR-4 schemes/surfaces floor, DR-5 evidence-shape register line, DR-6 non-goals.
- `BO-V2-BE12A-001` §§1–6 (engineering mission; coupon range 30–40; F1 recitals;
  acceptance clauses; delivery shape; register moves).
- House standing laws: N-O13 determinism, CWS register-recoverability, three-layer
  enumeration, OBS-E fail-first form, zero-UPDATE regime, byte-pin recitals (BE-11
  pin sha `9ba9fd82…f91f`).

---

# 3. EVIDENCE REVIEWED

| Evidence | Source | Reviewed | Sufficiency |
|---|---|---|---|
| DELIVERY_REPORT_V2_BE-12A.md | DA delivery | YES | SUFFICIENT |
| V2_BE-12A_SOURCE_TRANSCRIPT.md (20 files literal bodies + SHA manifest) | DA delivery | YES | SUFFICIENT |
| V2_BE-12A_TESTRUN_TRANSCRIPT.txt (full suite, 1,201) | DA delivery | YES | SUFFICIENT |
| V2_BE-12A_FAILFIRST_WITNESS.txt (OBS-E form) | DA delivery | YES | SUFFICIENT |
| BO-V2-BE12A-001 / DR-V2-BE-12-001 / adjudication custody copies | shared custody | YES | SUFFICIENT |

---

# 4. SCOPE VERIFICATION

## 4.1 Required Scope

BO §1.a–§1.g; §2 coupon range 30–40; §4 acceptance clauses; §5 delivery shape;
§6 register move.

## 4.2 Delivered Scope

`app/v2/live_exec/` (7 modules incl. posture-stub adapter boundary) · intent engine
(digest N-O13, idempotency, step-up shape) · eligibility + risk engines (typed
refusals; positive-reason pair) · `require_actuation` chokepoint with pinned
`LOCK_ORDER` L1→L6 · AM-1 fourth literal-prefix exemption · AM-2 third-state mode
(`REGISTERED_LOCKED_MODES`, tuples byte-identical, single superseded coupon cited) ·
AM-3 registry 2-keys posture-locked · AM-4 `practice_trade` class registered
fail-closed · migration `20260909_0053` (+1 table, +3 perms, guards, no compver) ·
38 coupons across 3 files · API surface per authorized scope; register line on
envelopes. Suite **1,201 passed, 0 failed**.

## 4.3 Scope Differences

None unauthorized. Two disclosure-class build notes logged by the DA (scanner
self-catch; wall-scan re-cut to import needles) — accepted as transparency, no
requirement impact. One boundary between the implemented API write path and the
migration's zero-UPDATE guards is DEFECTIVE in the delivered combination — see
§9 Finding `V2-BE12A-DEL-001`.

---

# 5. SIX-QUESTION / DESIGN DISCIPLINE REVIEW

### Q1 — Boundary (package birth + wall law)

**Requirement:** `BO §1.a; DR-0 move 1 — no domain imports live_exec; writers reach
providers ONLY through the sanctioned boundary (posture-stub in 12A).`

**Evidence:** `adapter_boundary.py` (closed stance vocabulary; typed refusal on every
submission-shaped call); wall coupons scanning import needles both directions;
no-submission-verbs scan on the package.

**Assessment:** `PASS`

### Q2 — Mode contract third state (AM-2 / DR-F1 law)

**Requirement:** `tuples byte-identical; REGISTERED_LOCKED_MODES added; get_mode()
constructs LIVE tagged locked; sole superseded coupon replaced BY CITATION;
byte-pinned wall file untouched.`

**Evidence:** `app/v2/mode/contract.py` (exact per law) · `tests/test_v2_mode.py`
(SUPERSEDES-BY-CITATION text with BO citation; third-state pins) · two coupons
re-asserting sha `9ba9fd82…f91f` · nowhere-scan for the retired coupon.

**Assessment:** `PASS`

### Q3 — LOCK-ORDER chokepoint (DR-0.75)

**Requirement:** `ONE door; pinned order L1→L6; first failure typed; mode_locked
computed ONLY from the mode contract; order itself coupon-tested.`

**Evidence:** `locks.py` (pinned LOCK_ORDER; predicates in order; L6 proxies sub-classes
first-class) · order-fixture battery (L1-vs-L3, L2-vs-L6, kill-vs-all, all-failing→L1)
· promenade coupons both directions.

**Assessment:** `PASS`

### Q4 — Registry & credential amendments (AM-3/AM-4)

**Requirement:** `EXECUTION_BACKENDS 1→2 keys with live entry posture-locked; frozen
literal retained; practice_trade class vault-only, fail-closed stub, hygiene proof.`

**Evidence:** `contracts.py` mapping (frozen MappingProxyType; live entry names the
boundary package) · be8 boundaries supersession coupon with citation · vault
`CREDENTIAL_CLASSES` + hygienic stub + repr-blind + no-env/file/provider coupon.

**Assessment:** `PASS`

### Q5 — Migration discipline (BO §1.g)

**Requirement:** `exactly one upgrade line; census re-tattoo 80/72/13; no compver row;
guard pair verbatim; idempotency at schema; downgrade restores 78; drift gate clean.`

**Evidence:** `20260909_0053` file exact; migration-wall coupons (one-line law, census,
row sets, guards fired, downgrade, drift gate, zero live_exec drift).

**Assessment:** `PASS`

### Q6 — API write path vs zero-UPDATE regime (combined behavior)

**Requirement:** `fielded POST /live-exec/intents must persist under the schema's
zero-UPDATE guards (guard pair law BO §1.c/§4; DR-4).`

**Evidence:** `api_register_intent()` sets `row.step_up_ref = step_up` AFTER
`register_intent()`'s `session.flush()`; commit then emits
`UPDATE v2_live_exec_intent SET step_up_ref=…`, tripping trigger
`v2_live_exec_intent_immutable_update` (BEFORE UPDATE → RAISE(ABORT)) on any
alembic-applied deployment. No delivered coupon crosses this border: migration
coupons exercise guards via raw sqlite3; engine coupons never commit post-flush
mutation; TestClient suites in this programme are create_all-built (triggers absent).

**Assessment:** `FAIL`

**Finding:** `V2-BE12A-DEL-001`

---

# 6. REQUIREMENT TRACEABILITY REVIEW

| Requirement | Evidence | Independent Result | Finding |
|---|---|---|---|
| BO §1.a package + walls | package + wall coupons | PASS | — |
| BO §1.b intent chassis + digest + step-up shape | intents.py + engine coupons | PASS (logic) | — |
| BO §1.c eligibility/risk | eligibility.py / risk.py + coupons | PASS | — |
| BO §1.d chokepoint + order coupons | locks.py + 17 lock coupons | PASS | — |
| BO §1.e AM-1..AM-4 | amendment surfaces + supersession coupons | PASS | — |
| BO §1.g migration + census | migration + migration-wall coupons | PASS | — |
| BO §4 fielded-writer behavior under guards | api.py vs guards interaction | FAIL | V2-BE12A-DEL-001 |
| BO §2 coupon range 30–40 | 38 delivered | PASS | — |
| BO §6 register move | AC12A line appended (custody disclosure accepted) | PASS | — |

---

# 7. SECURITY REVIEW

- authentication/RBAC: sa role grants SAL-4/SAL-2 as ordered; default-deny elsewhere.
- secret isolation: repr-blind type retained; stub reads no env/file/provider (coupon);
  no credential tokens in transcript beyond class vocabulary (delivery scan accepted).
- API boundaries: scoped permission trio only; C3 refusal posture preserved (no
  PUT/PATCH/DELETE added by this delivery).
- external network/broker boundaries: zero provider/transport tokens in package;
  boundary stub refuses all submission-shaped calls.
- logging/audit: register line carried on envelopes; step-up reference shape enforced.
- refusal/fail-closed: all refusal vocabularies closed, typed, and coupon-pinned;
  L6 sub_* proxied first-class.
- (The one failure — V2-BE12A-DEL-001 — is a correctness defect, not an exploit
  surface.)

---

# 8. TEST REVIEW

> **A passing test demonstrates observed test behaviour. It does not automatically
> prove complete requirement compliance.**

| Test | DA Result | ITRGA Verification | Conclusion |
|---|---|---|---|
| test_v2_be12a_locks.py (17) | PASS | Confirmed by body review + suite transcript | valid |
| test_v2_be12a_engines.py (12) | PASS | Confirmed | valid |
| test_v2_be12a_migration_walls.py (9) | PASS | Confirmed | valid |
| Byte-pin recitals (2 in-coupon) | PASS | Confirmed | BE-11 pin unmoved |
| Fail-first witness (OBS-E) | genuine | Confirmed | valid |
| API-writer-under-guards coupon | ABSENT | — | THE missing witness (see §14 Action R1) |

---

# 9. FINDINGS

| Finding ID | Severity | Requirement | Evidence | Impact | Required Correction |
|---|---|---|---|---|---|
| `V2-BE12A-DEL-001` | HIGH | BO §4 (fielded write path lawful under guards) | api.py commit order (step_up assigned after flush) × migration 0053 UPDATE-guard | On any alembic-applied deployment, POST /live-exec/intents dies at commit (IntegrityError from its own immutability trigger) — the band's flagship writer is non-functional under its own schema law | (1) move validated step_up into register_intent() constructor kwargs BEFORE flush (no UPDATE ever); (2) add ONE coupon: TestClient POST against alembic-0053-chain DB asserting 200 + persisted row + duplicate-arm typed |

---

# 10. OBSERVATIONS

| Observation | Severity | Recommendation |
|---|---|---|
| Suite-invisibility of the commit/guard border: three coupon families each cover one side | LOW | Adopt a standing rule: every new gated table's authorized writer gets one API-level coupon against the migration-applied chain |
| Scanner self-catch + wall re-cut lessons (disclosed) recurring across eras | LOW | Keep disclosing; the pattern is becoming a documented house lesson class |

---

# 11. POSITIVE ASSESSMENT

- AM-1..AM-4 executed exactly under their governing laws; DR-F1's byte-pin law obeyed
  to the letter — one file, one test, one citation; the BE-11 pin never moved.
- LOCK-ORDER law implemented as designed: pinned literal order, promenade proofs both
  directions, L6 first-class proxying.
- Migration discipline exact: one upgrade line; downgrade restores 78; census 80/72/13.
- Delivery candour again exemplary (disclosed build lessons; custody disclosure re the
  new register file).
- Coupon range law satisfied: 38 within 30–40.

---

# 12. GOVERNANCE STATE

```text
Implementation: CORRECTION REQUIRED (one defect, writer-under-guards)
Tests: GREEN (1,201) + ONE MISSING BORDER COUPON
Evidence: SUFFICIENT (delta re-delivery expected)
Requirement compliance: 10/11 tracked clauses PASS, 1 FAIL
Governance approval: WITHHELD pending correction review
Production certification: NOT APPLICABLE (capability-before-activation; per REQ R-1.4)
```

---

# 13. DETERMINATION

### CORRECTION REQUIRED

One gating deficiency (`V2-BE12A-DEL-001`) must be corrected and re-reviewed. All other
requirements PASS at this review tier.

---

# 14. REQUIRED ACTIONS

| Action | Requirement | Owner | Re-review Evidence |
|---|---|---|---|
| R1: move validated step_up into register_intent() before flush; no UPDATE path on v2_live_exec_intent | BO §4; DR-4 zero-UPDATE | DA | patched intents.py/api.py literal bodies (v1.0.1) |
| R2: add ONE border coupon (API POST against alembic-0053 chain DB; 200 + persisted row + duplicate-arm absent→typed) | BO §2/§4 | DA | new coupon body + suite run 1,202 passed |
| R3: reproduce the defect pre-patch (OBS-E-class witness) | OBS discipline | DA | failure transcript of the API write under guards |

---

# 15. NEXT AUTHORIZED ACTION

```text
No next Build Order (12B) until v1.0.1 correction review closes ACCEPT.
```

---

# 16. ITRGA SIGN-OFF

> This review is an independent governance assessment based on the evidence identified
> above. It does not rewrite the Development Authority's delivery record. Where
> applicable, this determination authorizes only the state explicitly stated in this
> document.

**ITRGA Determination:** `CORRECTION REQUIRED (single micro-correction; delta review to follow v1.0.1)`

**END OF ITRGA REVIEW**
