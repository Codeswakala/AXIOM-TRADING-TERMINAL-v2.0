# AXIOM — ITRGA INDEPENDENT REVIEW
# V2-BE-12B — LIVE-EXEC SUBMISSION, ACK/FILL PROCESSING, PRACTICE ACTUATOR WIRING

**Review ID:** `ITRGA-REV-V2-BE12B-001`
**Version:** `v1.0.0`
**Date:** `2026-09-08`
**Authority:** `ITRGA`
**Requirement:** `REQ-V2-BE-12-001 (as adopted)`
**Design Record:** `DR-V2-BE-12-001 (as adopted; sub-ladder 12B; DR-3)`
**Build Order:** `BO-V2-BE12B-001`
**Delivery Report:** `AXIOM-V2-BE-12B-DR-001 v1.0.0 (evidence pack E-01..E-03)`
**Status:** `REVIEW`

---

# 1. REVIEW PURPOSE

Independent review of the 12B delivery: two-lane chokepoint + non-commutation law,
boundary wiring via the sanctioned provider leg, submission/ack/fill engines with
dedupe + quarantine, AM-4 practice_trade vault doorway, migration 0054, LAW-BORDER-01
compliance, the DR-3 refusal-injection battery, and the BO §4 jurisdiction note.

---

# 2. REVIEW AUTHORITY

BO-V2-BE12B-001 §§1..6; DR-V2-BE-12-001 DR-0.75/DR-2/DR-3; LAW-BORDER-01;
DIRECTION-POSTBE11-001 §§1/7; N4 secret-handling law; house three-layer enumeration,
OBS-E, N-O13.

---

# 3. EVIDENCE REVIEWED

| Evidence | Source | Reviewed | Sufficiency |
|---|---|---|---|
| DELIVERY_REPORT_V2_BE-12B.md | DA | YES | SUFFICIENT |
| E-01 SOURCE_TRANSCRIPT.md (18 files literal + SHA) | DA | YES | SUFFICIENT |
| E-02 TESTRUN_TRANSCRIPT.txt (full suite) | DA | VERIFIED (1,239 passed lines; tail exact) | SUFFICIENT |
| E-03 FAILFIRST_WITNESS.txt (OBS-E; practice-wire note) | DA | YES | SUFFICIENT |

---

# 4. SCOPE VERIFICATION

## 4.1 Required Scope
BO §1.a–§1.g: two-lane law; wiring via provider leg; submission chassis; ack/fill +
dedupe + quarantine; vault doorway; injection battery; migration 0054; 35–45 coupons;
LAW-BORDER-01.

## 4.2 Delivered Scope
All present (37 coupons; borders #1+#2; migration one-line; 84/75/14; lxe compver
DB==disk; downgrade exact; boundaries & walls amended with literal-scoped exceptions;
byte-pins unmoved; suite 1,239).

## 4.3 Scope Differences
No unauthorized additions. ONE structural deficiency between the joined modules — §9
`V2-BE12B-DEL-001` — visible only on the chained path, invisible to any single
coupon family.

---

# 5. DESIGN-DISCIPLINE REVIEW (band questions)

### Q1 — Two-lane law + non-commutation
**Evidence:** locks.py disjoint `LOCK_ORDER` (6) vs `PRACTICE_LOCK_ORDER` (5); disjoint-
ness coupon; commutation coupons both directions; LIVE byte-posture recital coupon.
**Assessment:** `PASS`

### Q2 — Wiring via sanctioned leg; wall exceptions literal-scoped
**Evidence:** adapter_boundary speaks ONLY the provider-module path; actuator inside
providers/; amended walls both directions with one-file name-literal exceptions;
actuator vocabulary scanned closed; V1 shapes banned even in the actuator.
**Assessment:** `PASS`

### Q3 — Submission / ack / fill engines
**Evidence:** born-complete rows; uq(intent_id) + typed duplicate; fill-identity
SUBSTANTIVE projection anchor (N-O1 law applied); quarantine-as-state; border #2
exercises engines over guarded schema incl. schema-fatal-on-bypass.
**Assessment:** `PASS`

### Q4 — Vault doorway (AM-4)
**Evidence:** AAD-disjoint sealed payload family; masquerade impossible both ways
(coupon-proven); fail-closed arms; repr-blind; no API credential surface
(coupon-scanned); investor law untouched.
**Assessment (code):** `PASS` — **but see Q5.**

### Q5 — The chained writer path (API → lane door → vault resolution)
**Requirement (BO §1.c, premise):** the submit writer passes the PRACTICE lane door
*when armed* — implying the door CAN open with correct posture.
**Evidence:** chained trace:
1. `api_submit_intent` → `practice_credential_state()`;
2. boundary → `resolve_practice_trade_credential()` **called WITHOUT a passphrase**;
3. vault: `if not passphrase: return ABSENT`;
4. ⇒ credential_state is CONSTANT `"absent"` on every API flow, regardless of the
   sealed vault's presence/correctness;
5. ⇒ P3 `practice_posture_absent` fires on EVERY armed attempt via the API;
6. the one full-pass coupon (`test_injection_terminal_unreachable_typed`) INJECTS
   `credential_state="present"` into the fixture — it never traverses the vault;
   border #1 stops at P2, so the P3 failure is never observed field-shaped.
Net: the PRACTICE lane inherits the always-locked behavior LAWFUL for the LIVE lane.
Assets-Del-001 class: green coupons on either side of a border, red path across it.
**Assessment:** `FAIL`
**Finding:** `V2-BE12B-DEL-001`

### Q6 — Migration discipline
**Evidence:** one upgrade line; 84/75/14 tattoo; lxe compver DB==disk recompute;
downgrade exact incl. the compver delete-guard dance; drift gate clean.
**Assessment:** `PASS`

---

# 6. REQUIREMENT TRACEABILITY REVIEW

| Requirement | Evidence | Independent Result | Finding |
|---|---|---|---|
| BO §1.a two-lane + non-commutation | lanes coupons | PASS | — |
| BO §1.b wiring + wall amendments | wall coupon bodies | PASS | — |
| BO §1.c submission chassis + **its premise** | api/locks/vault chained trace | PARTIAL — refusals PASS, armed-pass UNREACHABLE | V2-BE12B-DEL-001 |
| BO §1.d ack/fill + dedupe + quarantine | border #2 + identity anchor coupons | PASS | — |
| BO §1.e vault doorway | boundary_vault coupons | PASS (in isolation) | — |
| BO §1.f injection battery | 8 arms typed | PASS | — |
| BO §1.g migration | migration coupons | PASS | — |
| BO §2 37 coupons incl. LAW-BORDER-01 | suite + 2 border coupons | PASS | — |
| BO §4 jurisdiction (no real-wire act required) | witness note + absence of any such act | PASS | — |

---

# 7. SECURITY REVIEW
No credential material on any API surface; AAD-disjoint payload families; state-only
crossings; terminal vocabulary confined to the sanctioned prefix + the one named
boundary file; investor/read-only law untouched; funded class NONEXISTENT. (The
finding is functional-reachability, not exposure.)

---

# 8. TEST REVIEW
| Test | DA Result | ITRGA Verification | Conclusion |
|---|---|---|---|
| 3 new coupon files (37) | PASS | Confirmed (bodies + suite lines) | valid in isolation |
| LAW-BORDER-01 borders #1/#2 | PASS | Confirmed | valid — and this class is exactly where the finding lives |
| OBS-E fail-first | genuine | Confirmed | valid |
| Armed full-lane pass via API | ABSENT by injection-substitution | — | THE missing witness (§14 R2) |

---

# 9. FINDINGS

| Finding ID | Severity | Requirement | Evidence | Impact | Required Correction |
|---|---|---|---|---|---|
| `V2-BE12B-DEL-001` | HIGH | BO §1.c (premise of an ARMED practice lane) | api→boundary→vault chained trace; constant-ABSENT state reader; pass only via fixture injection | The PRACTICE lane can NEVER pass through the API, even with a perfect sealed vault: 12B's designated actuating lane is built permanently-locked in the one posture where it should unlock — behaviorally indistinguishable from a broken capability and from an over-restrictive one | R1: a LAWFUL passphrase-provisioning law at the doorway (design answer REQUIRED at INT: e.g., env-carried passphrase read ONLY inside vault.py at request time — never module/app state; N4 posture preserved); R2: one armed-pass border coupon (sealed vault + lawful provisioning + injected terminal fake answering `accepted` → full API submit persists one `accepted` row, guards intact); R3: OBS-E-class witness that the old constant-ABSENT behavior is reproduced before the patch |

Also (LOW, observations, non-blocking):
| Observation | Severity | Recommendation |
|---|---|---|
| api.py module docstring + `_actuation_door` comment still narrate the 12A era ('no practice_trade resolves in 12A') | LOW | Refresh to 12B truth in the CR delta |
| `PRACTICE_BASIS_MAX_AGE_HOURS = 24.0` is a design call declared but not register-cited | LOW | Cite in the CR delta's register note |

---

# 10. POSITIVE ASSESSMENT
Two-lane law implemented better than specified (disjoint vocabularies + bidirectional
commutation coupons); wall exception handling exemplary (literal-scoped, not-vacuous
arms); the N-O1 substantive-projection law applied to fill identity correctly; a
delivery report whose disclosures are all honest (incl. the compver-column first
draft lesson and the wall catching its own import).

---

# 11. GOVERNANCE STATE
```text
Implementation: CORRECTION REQUIRED (one reachability defect)
Tests: 1,239 GREEN in isolation-grade; ONE chained-armed-pass witness missing
Evidence: SUFFICIENT for diagnosis (delta re-delivery expected)
Requirement compliance: 8/9 PASS, 1 PARTIAL-FAIL
Governance approval: WITHHELD pending correction review
Production certification: NOT APPLICABLE (capability-before-activation; REQ R-1.4)
```

---

# 12. DETERMINATION
### CORRECTION REQUIRED — finding `V2-BE12B-DEL-001` must close before acceptance.

---

# 13. REQUIRED ACTIONS

| Action | Requirement | Owner | Re-review Evidence |
|---|---|---|---|
| R1: passphrase-provisioning law at the practice doorway (design answer; N4-safe; e.g., env read confined to vault.py; never app/module state) | BO §1.e + §1.c premise | DA | patched vault/boundary bodies |
| R2: armed-pass border coupon: sealed practice vault + lawful provisioning + injected fake terminal `accepted` → full API submit persists ONE row, terminal_state accepted, guards intact; and WITHOUT the vault, the P3 refusal still types | BO §1.c/§2 | DA | new coupon body + suite run 1,240 |
| R3: OBS-E-class pre-patch repro of the constant-ABSENT chain | OBS discipline | DA | witness transcript |

---

# 14. NEXT AUTHORIZED ACTION
```text
No next Build Order (12C) until the v1.0.1 correction review closes ACCEPT.
```

---

# 16. ITRGA SIGN-OFF
> Independent governance assessment on the evidence above. It authorizes only the
> state explicitly stated.

**ITRGA Determination:** `CORRECTION REQUIRED (single chained-path finding; the seat
again reads two lanes at once — this time across the wire, not the suite)`

**END OF ITRGA REVIEW**
