# AXIOM — DA DELIVERY REPORT

# BE-12A — LIVE-EXEC INTENTS, ELIGIBILITY, PRE-TRADE RISK, LOCK-ORDER

**Delivery Report ID:** `AXIOM-V2-BE-12A-DR-001`
**Version:** `v1.0.1` (re-stamped after CR-1; supersedes v1.0.0 md5 `db4544f45ae78c71b5bb7dd7b2c8aafa`; first delivery on the adopted house template)
**Date:** `2026-09-08`
**Development Authority:** `DA`
**Build Order:** `BO-V2-BE12A-001`
**Design Record / Approved Plan:** `DR-V2-BE-12-001 (adopted as amended)`
**Repository Commit / Head:** `git HEAD 9c78afa (frozen; custody Operator-only); alembic chain head on DA test chains: 20260909_0053; fielded lineage: 20260909_0052 (untouched)`
**Status:** `DELIVERED — AWAITING ITRGA CORRECTION REVIEW (v1.0.1 delta per ITRGA-REV-V2-BE12A-001 §14)`

---

# 1. PURPOSE

Implement BO-V2-BE12A-001: the 12A chapter of the Controlled Live Execution
Gateway — package birth + wall law, intent engine, eligibility + pre-trade
risk, the LOCK-ORDER chokepoint, standing-law amendments AM-1..AM-4,
migration `20260909_0053`, coupon battery 30–40, register line as evidence
shape. Execution authority: NONE (capability-before-activation;
LIVE = REGISTERED_LOCKED; funded account: NONE).

**v1.0.1 delta purpose:** close finding `V2-BE12A-DEL-001`
(ITRGA-REV-V2-BE12A-001 §9) by executing required actions R1/R2/R3.

---

# 2. AUTHORITY AND SCOPE

## 2.1 Governing Inputs

| Artifact | ID / Version | Role |
|---|---|---|
| Requirement | `REQ-V2-BE-12-001` (adopted + amendments) | Defines required outcome |
| Design Record | `DR-V2-BE-12-001` (adopted as amended; DR-F1/LOCK-ORDER laws) | Defines approved architecture |
| Build Order | `BO-V2-BE12A-001` | Authorizes implementation |
| Review | `ITRGA-REV-V2-BE12A-001` (CORRECTION REQUIRED; R1–R3) | Directs this v1.0.1 delta |
| Adjudication | Operator Adjudication 2026-09-08 | ADOPT + amendments absorbed |

## 2.2 Implemented Scope

BO §1.a–§1.g complete (v1.0.0) + CR-1 correction (v1.0.1): R1 writer-path
repair, R2 border coupon, R3 pre-patch defect witness.

## 2.3 Not Implemented

12B (submission/fills/practice actuator wiring), 12C (cancel-modify),
12D (activation instrument + kill-switch tables), 12E (reconciliation +
incident) — all later sub-BOs by the R-6.1 ordering law. No compver row
(BO §1.g). No console act (the 0053 apply is a separate sanctioned act).
Excluded work is excluded by order, not defect.

---

# 3. IMPLEMENTATION SUMMARY

| Area | Implemented Artifact | Description |
|---|---|---|
| Package | `app/v2/live_exec/` (7 modules) | Fourth package family; wall law both directions; adapter boundary POSTURE-STUB refusing every submission-shaped call typed |
| Chokepoint | `app/v2/live_exec/locks.py` | `require_actuation()` — ONE door, pinned LOCK_ORDER L1→L6, first-failure-typed; L1 from mode contract ONLY; L6 proxies sub_* first-class |
| Intent engine | `app/v2/live_exec/intents.py` | uuid chassis; idempotency (schema-uq + typed refusal); N-O13 digest (`pxs-1.0.0`,`lxe-1.0.0`); step-up shape law (second FACTOR, V2-TD-29 line). **v1.0.1 R1: `step_up_ref` is a constructor kwarg — rows born complete, no UPDATE path exists** |
| Eligibility/Risk | `eligibility.py` / `risk.py` | Typed refusals (BOP law: absent basis refuses); money-units sizing (BE-11 flat-account law); typed declines + positive-reason pair |
| API | `app/v2/live_exec/api.py` | POST intents / POST evaluate / GET intents; register line on every envelope; actuation door's typed refusal carried (capability witnessed, activation refused). **v1.0.1 R1: validate-then-birth; post-flush mutation DELETED** |
| Database | `alembic/versions/20260909_0053_v2_be12a_live_exec_intents.py` | +1 table `v2_live_exec_intent` (zero-UPDATE; guard pair; CHECKs; idempotency unique index); +3 perms (SAL-4/4/2); NO compver; ONE upgrade line; tattoo 80/72/13. **Byte-still through CR-1** (`55663465d6ede38b…` — the writer moved to obey the law, not the law to excuse the writer) |
| Security (AM-1..4) | `permissions.py` / `mode/contract.py` / `paper_trading/contracts.py` / `broker_read/vault.py` | Fourth marker exemption `v2.live_exec.`; `REGISTERED_LOCKED_MODES` with tuples byte-identical (DR-F1 law); registry 2 keys live→boundary; `practice_trade` class fail-closed ABSENT stub + hygiene proof |
| Tests | `tests/test_v2_be12a_{locks,engines,migration_walls}.py` | 38 coupons (v1.0.0) + **1 border coupon (v1.0.1 R2) = 39** |

---

# 4. FILE CHANGE INVENTORY

Full v1.0.0 inventory (20 files, literal bodies + SHA-256): REM-001
`docs/evidence/V2_BE-12A_SOURCE_TRANSCRIPT.md`. **CR-1 bounded diff —
exactly THREE files** (literal bodies + SHA-256:
`docs/evidence/V2_BE-12A_CR1_SOURCE_SUPPLEMENT.md`):

| File | Change Type | Purpose | SHA-256 |
|---|---|---|---|
| `app/v2/live_exec/intents.py` | Modified (R1) | `step_up_ref` constructor kwarg; row born complete before flush | in CR1 supplement §1 |
| `app/v2/live_exec/api.py` | Modified (R1) | validate-then-birth; post-flush assignment deleted | in CR1 supplement §1 |
| `tests/test_v2_be12a_migration_walls.py` | Modified (R2) | +`test_api_writer_persists_under_alembic_guards` (the border coupon) | in CR1 supplement §1 |

Byte-still recitals at CR-1: `tests/test_v2_be9_boundaries.py` ==
`9ba9fd82…f91f` (BE-11 pin) · migration 0053 == `55663465…` · pbr ==
`4c243435…178b`.

---

# 5. REQUIREMENT TRACEABILITY

| Requirement | Implementation | Evidence | Result |
|---|---|---|---|
| BO §1.a package + walls | live_exec package + wall coupons | wall/import scans | PASS |
| BO §1.b intent chassis | intents.py | engine coupons + digest ×3 | PASS |
| BO §1.c eligibility/risk | eligibility.py / risk.py | typed-arm coupons | PASS |
| BO §1.d chokepoint | locks.py | 17 lock coupons incl. order fixtures + promenades | PASS |
| BO §1.e AM-1..AM-4 | amendment surfaces | supersession-by-citation coupons | PASS |
| BO §1.g migration | 20260909_0053 | migration coupons; tattoo 80/72/13 | PASS |
| **BO §4 fielded writer under guards** | **R1 patch + R2 border coupon** | **CR1 defect witness + border coupon + 1,202 run** | **PASS (was FAIL: V2-BE12A-DEL-001)** |
| BO §2 coupon range | 39 total (38 + 1 border) | collect count | PASS (range law: the +1 is review-ordered) |
| BO §6 register move | AC12A line | campaign register (custody disclosure stands) | PASS |

---

# 6. TEST AND VERIFICATION RESULTS

## 6.1 Unit/Integration (full suite, one world)

**Command:**
```text
AXIOM_ENVIRONMENT=testing AXIOM_ALLOW_INSECURE_DEV=true
AXIOM_JWT_SECRET_KEY=*** AXIOM_V2_MODE=RESEARCH
AXIOM_DATABASE_URL=sqlite+aiosqlite:///:memory: python3 -m pytest -v
```

**Result:**
```text
1202 passed, 2 warnings in 660.24s (0:11:00)
```
(= 1,201 + 1, the review's R2 expectation exactly. Warnings = the carried
registered pair.)

**Evidence:** `V2_BE-12A_CR1_TESTRUN_TRANSCRIPT.txt` (md5
`75b95a59ef6caf22e4a76217045e9b89`, sha256 `d6f1ede1…898e`).
Prior v1.0.0 run: `V2_BE-12A_TESTRUN_TRANSCRIPT.txt` (1,201).

## 6.2 Security Tests

RBAC 401/403 posture inherited from the standing battery; AM-4 hygiene
coupon (stub reads no env/file/provider); no-submission-verbs scan; wall
scans. All inside the suite run above.

## 6.3 Database / Migration Evidence

- pre-state: 0052 chain (78/69/13, seeds 5) — rise witnessed
- migration: ONE upgrade line `20260909_0052 -> 20260909_0053` (both
  streams parsed, N-O8)
- post-state: tattoo **80/72/13**; 3 `v2.live_exec.*` rows exact; NO
  compver row (asserted); guard pair verbatim; idempotency-uq +
  posture-CHECK fired live
- downgrade: exact (78 restored; table + perms gone); drift gate at 0053
  clean (zero live_exec tokens; inheritance witness)
- **R2 border evidence: TestClient POST against the alembic-0053-applied
  chain (triggers PRESENT): 200 + persisted row + duplicate → 409 typed;
  post-close Level-I: one row, step_up_ref from birth, guard pair == 2**

---

# 7. BEHAVIOURAL EVIDENCE

| Scenario | Expected | Observed | Evidence |
|---|---|---|---|
| Valid intent (fielded chain) | 200; row born complete; guards silent | 200; Level-I row with step_up_ref from birth | border coupon |
| Pre-patch writer (defect) | — | IntegrityError from own UPDATE guard | CR1 defect witness STEP 1 |
| Duplicate intent | 409 typed `duplicate_intent` | 409 typed | border coupon |
| Missing step-up | typed `step_up_reference_absent` | typed | engine coupons |
| Stale/absent basis | typed `basis_stale` (BOP law) | typed | engine coupons |
| Unauthorized | 401/403, generic denial | 401/403 | rbac battery |
| LIVE mode actuation | `mode_locked` (never posture answer) | `mode_locked`; promenades hold | lock coupons |
| All six locks failing | L1 answers | `mode_locked` | order fixture |

---

# 8. SECURITY EVIDENCE

**FACT** — no submission verb in the package (scan); boundary stub refuses
typed; `practice_trade` resolves ABSENT; repr-blind type reused; funded
class nonexistent; register line on every envelope; BE-11 byte pin
unmoved; credential scan CLEAN-with-classification (class-name vocabulary
+ standing test fixture only).
**ENGINEERING ASSESSMENT** — the R1 shape (born-complete rows) is
structurally stronger than the corrected defect required: no UPDATE
statement can now exist against the intent table from any lawful path.
**PROPOSAL** — adopt the review's §10 observation as standing law: every
new gated table's authorized writer gets one API-level coupon against the
migration-applied chain (the DA supports; ITRGA/Operator to enact).

---

# 9. GOVERNANCE / AUTHORITY STATE

```text
Implemented: YES (BO scope + CR-1 corrections R1/R2/R3)
Tests passing: YES (1,202/0)
Delivery submitted: YES (v1.0.1 delta)
DA self-assessment: ordered scope satisfied; finding V2-BE12A-DEL-001 corrected and witnessed both sides
ITRGA determination: PENDING (delta review per §14)
Governance approval: NOT YET ISSUED (WITHHELD at v1.0.0 per §12)
Production certification: NOT APPLICABLE (capability-before-activation; REQ R-1.4)
```

---

# 10. KNOWN FINDINGS

| ID | Finding | Severity | Status | Evidence |
|---|---|---|---|---|
| `V2-BE12A-DEL-001` | API writer emitted UPDATE against zero-UPDATE guards (post-flush mutation) | HIGH | **CORRECTED — awaiting ITRGA close** | CR1 defect witness (reproduced pre-patch; clean post-patch; border coupon) |
| Harness note | First post-patch witness script read an expired attribute post-commit (MissingGreenlet) — harness defect, not patch defect; corrected, disclosed | LOW | CLOSED (disclosed) | CR1 defect witness STEP 3 note |

---

# 11. RISKS

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| create_all test worlds mask trigger-boundary defects (the DEL-001 class) | Writer defects invisible until fielded | Recurs per band | §10 observation → standing border-coupon rule | ITRGA/Operator (rule); DA (execution) |

---

# 12. TECHNICAL DEBT

None introduced this delivery. (V2-TD-30/31 closed earlier instruments;
V2-TD-32 standing, environmental.)

---

# 13. OUT-OF-SCOPE / DEFERRED ITEMS

12B/12C/12D/12E per sub-ladder; compver row for `lxe-1.0.0` (arrives with
its assigned sub-band); 0053 fielded apply (separate act); activation
instrument (12D template, NOT-IN-FORCE by design).

---

# 14. EVIDENCE PACKAGE

| Evidence ID | Artifact | Purpose |
|---|---|---|
| E-01 | `V2_BE-12A_SOURCE_TRANSCRIPT.md` (md5 `01f0a3db…`) | v1.0.0 REM-001, 20 files |
| E-02 | `V2_BE-12A_TESTRUN_TRANSCRIPT.txt` (md5 `1b5e1cf0…`) | v1.0.0 suite (1,201) |
| E-03 | `V2_BE-12A_FAILFIRST_WITNESS.txt` (md5 `2c4bd5db…`) | OBS-E fail-first |
| E-04 | `V2_BE-12A_CR1_SOURCE_SUPPLEMENT.md` (md5 `872ff6dd22cd7365836cab4bd4b2b8e0`) | CR-1 REM-001, exactly 3 files |
| E-05 | `V2_BE-12A_CR1_TESTRUN_TRANSCRIPT.txt` (md5 `75b95a59ef6caf22e4a76217045e9b89`) | CR-1 suite (1,202) |
| E-06 | `V2_BE-12A_CR1_DEFECT_WITNESS.txt` (md5 `d030ed88b97a3f461edb6c4d129d490e`) | R3: pre-patch repro + post-patch clean + Level-I |

---

# 15. DA SELF-ASSESSMENT

> The DA assesses that the implemented scope satisfies the Build Order
> requirements and that finding V2-BE12A-DEL-001 is corrected per §14
> R1/R2/R3, based on the evidence listed in this report. The defect was
> real, reproduced exactly as the review described, and its correction
> moved the writer to obey the schema law — the schema law did not move.
> This is a Development Authority assessment only and does not constitute
> ITRGA approval, certification, or production authorization.

---

# 16. DELIVERY STATUS

```text
Build Order executed: YES
Implementation complete for ordered scope: YES
Evidence package complete: YES (E-01…E-06)
Known findings disclosed: YES
Delivery Report submitted: YES (v1.0.1)
ITRGA determination: PENDING (delta review)
Production certification: NOT CERTIFIED
```

---

# 17. DA SIGN-OFF

**Development Authority:** `Replacement Development Authority (DA)`

> This Delivery Report records what was implemented and the evidence
> produced by the Development Authority. It does not constitute an
> independent governance determination or authorization for any
> subsequent phase.

**We don't guess. We prove.**

**END OF DELIVERY REPORT**
