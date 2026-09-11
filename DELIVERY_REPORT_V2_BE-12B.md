# AXIOM — DA DELIVERY REPORT

# BE-12B — LIVE-EXEC SUBMISSION, ACK/FILL PROCESSING, PRACTICE ACTUATOR WIRING

**Delivery Report ID:** `AXIOM-V2-BE-12B-DR-001`
**Version:** `v1.0.1` (re-stamped after CR-1; supersedes v1.0.0 md5 `2bf0578e41bd74e9acbaa40bb831c5fb`)
**Date:** `2026-09-08`
**Development Authority:** `DA`
**Build Order:** `BO-V2-BE12B-001` (filed md5 `5b23d5438df1121f7014b266e4d0b8f8` · sha256 `13174653…2203`)
**Design Record / Approved Plan:** `DR-V2-BE-12-001 (as adopted; sub-ladder 12B)`
**Repository Commit / Head:** `git HEAD 9c78afa (frozen; custody Operator-only); alembic chain head on DA test chains: 20260909_0054; fielded lineage: 20260909_0052 (untouched)`
**Status:** `DELIVERED — AWAITING ITRGA CORRECTION REVIEW (v1.0.1 delta per ITRGA-REV-V2-BE12B-001 §14)`

---

# 1. PURPOSE

Implement BO-V2-BE12B-001: the two-lane chokepoint (LIVE lane = 12A door
unchanged; PRACTICE lane with its own closed vocabulary; refusals never
commute), the adapter boundary moved `posture_stub` → `practice_wired` by
cited edit, the submission chassis + ack/fill processing with dedupe and
quarantine laws, the AM-4 practice_trade vault doorway, migration
`20260909_0054`, and the LAW-BORDER-01 border coupons for both new gated
writers. Execution authority: NONE except the practice world under the
sealed practice leg, inside coupons/witnesses only. Funded account: NONE.

---

# 2. AUTHORITY AND SCOPE

## 2.1 Governing Inputs

| Artifact | ID / Version | Role |
|---|---|---|
| Requirement | `REQ-V2-BE-12-001` (R-1.1, R-3.2/3.3, R-2, R-6.1) | Defines required outcome |
| Design Record | `DR-V2-BE-12-001` (12B; DR-0.75; DR-2; DR-3) | Defines approved architecture |
| Build Order | `BO-V2-BE12B-001` | Authorizes implementation |
| Standing law | `LAW-BORDER-01` (ITRGA-REV-V2-BE12A-CR-001 §7) | Border coupons per gated writer |
| Direction | `DIRECTION-POSTBE11-001 §1/§7` | No practice trading activity at this stage (BO §4 jurisdiction note honored) |

## 2.2 Implemented Scope

BO §1.a–§1.g complete: two-lane chokepoint · boundary wiring via the
sanctioned BE-9 provider leg · submission chassis + submit verb ·
ack/fill processing with dedupe + quarantine · vault doorway ·
refusal-injection battery · migration 0054 with census re-tattoo.

## 2.3 Not Implemented

12C (cancel/modify + unknown-state handling beyond the quarantine
transition), 12D (activation instrument + kill-switch tables), 12E
(reconciliation + incident; DR-F2 conversion law rides there). No
real-wire demo submission (BO §4 jurisdiction note: separate operator
authorization if ever desired — the evidence plan does not lean on it).
No console act. Excluded by order, not defect.

---

# 3. IMPLEMENTATION SUMMARY

| Area | Implemented Artifact | Description |
|---|---|---|
| Chokepoint | `app/v2/live_exec/locks.py` | PRACTICE lane added: `require_practice_actuation()`, pinned `PRACTICE_LOCK_ORDER` (lane→mode→posture→boundary→basis), closed vocabulary `actuation_lane_mismatch / practice_mode_not_armed / practice_posture_absent / practice_boundary_not_wired / basis_stale`; LIVE lane byte-posture unchanged (recital coupons); the two vocabularies provably disjoint (6+5=11, no shared member); NON-COMMUTATION coupon-pinned both directions |
| Boundary | `app/v2/live_exec/adapter_boundary.py` | Stance `posture_stub` → `practice_wired` BY CITED EDIT; the doorway demands a practice-lane pass, then reaches the terminal ONLY via the sanctioned provider leg; state-only credential reader (`practice_credential_state()` — the one vault-naming file; material never crosses); terminal absence → typed `practice_terminal_unavailable` |
| Provider leg | `app/v2/broker_read/providers/practice_actuator.py` | The terminal-speaking body INSIDE the sanctioned prefix (BE-9 allowlist ridden, not re-extended); closed answer vocabulary `accepted/rejected/requote/no_answer`; timeouts/absent retcodes = the `no_answer` STATE, never an exception from the seam |
| Submission | `app/v2/live_exec/submissions.py` | Migrate-gated writer: intent must exist + lane pass; rows born complete (LAW-BORDER-01 lesson structural from birth); `no_answer` → `quarantined_unknown` at persistence (BE-8 S2.4 preimage); `duplicate_submission` typed with standing row cited + uq(intent_id) at schema |
| Ack/Fills | `app/v2/live_exec/ack_fills.py` | Acks captured on the submission record at birth; fill correlation by `server_ack_ref|terminal_order_id` (closed CHECK); DE-DUPE anchored on fill-event identity over SUBSTANTIVE facts (N-O1 projection law — volatile-in-blob cannot flip identities); `duplicate_fill_event` typed + schema-fatal on engine bypass |
| Vault | `app/v2/broker_read/vault.py` | AM-4 doorway BY CITED EDIT: own sealed payload family (salt+nonce+AES-256-GCM, Argon2id; AAD `axiom-v2-be12b-practice` — DISJOINT from the investor AAD, masquerade structurally impossible both directions, coupon-proven); `AXIOM_BROKER_PRACTICE_VAULT_PATH` outside the repo; every absence arm → ABSENT; registration = console records-of-intent (no API credential surface, coupon-scanned) |
| API | `app/v2/live_exec/api.py` | POST `/live-exec/intents/{id}/submit` (SAL-4) + GET `/submissions` + GET `/fills` (SAL-2); register line updated per BO §5: `BE-12B SUBMISSION+FILLS \| PRACTICE=WIRED \| LIVE=REGISTERED_LOCKED \| funded account: NONE` |
| Database | `20260909_0054` | +2 tables with guard pairs (+4 triggers), +3 perms, +1 compver `live_exec_engine\|lxe-1.0.0` (the 12A-deferred row, exactly once, existing-set filtered; rolled hash from disk at apply); ONE upgrade line; tattoo **84/75/14**; downgrade exact (80/72/13 restored; compver delete-guard dance) |
| Tests | `tests/test_v2_be12b_{lanes,boundary_vault,migration_borders}.py` | **37 coupons** (17/14/6) |

---

# 4. FILE CHANGE INVENTORY

Full manifest (18 files, literal bodies + SHA-256): REM-001
`docs/evidence/V2_BE-12B_SOURCE_TRANSCRIPT.md`. Changed files: 5
live_exec modules · 1 provider actuator (new) · vault doorway · 1 model
(new) + registration · permissions (+3 enum members) · migration 0054
(new) · 3 new coupon files · 4 coupon files amended BY CITATION
(`test_v2_be12a_engines.py` [stance + hygiene], 
`test_v2_be12a_migration_walls.py` [wall + verb scans, one-file
exceptions], `test_v2_be8_boundaries.py` [stance arm], 
`test_v2_be9_contract.py` [T-4 mutation-vocabulary scan, actuator
exception with both-ways arms]).

**Byte-still recitals (measured at transcript build):**
`tests/test_v2_be9_boundaries.py` == `9ba9fd82…f91f` (the BE-11 byte
pin — NEVER moved) · migration 0053 == `55663465…` · pbr rolled ==
`4c243435…178b`.

---

# 5. REQUIREMENT TRACEABILITY

| Requirement | Implementation | Evidence | Result |
|---|---|---|---|
| BO §1.a two-lane law + non-commutation | locks.py | lane coupons both directions | PASS |
| BO §1.b boundary wiring via provider leg | adapter_boundary + practice_actuator | wall coupons; no terminal token outside the leg | PASS |
| BO §1.c submission chassis | submissions.py + submit verb | border coupon #1; duplicate typed | PASS |
| BO §1.d ack/fills + dedupe + quarantine | ack_fills.py + model CHECKs | border coupon #2; injected-seam battery | PASS |
| BO §1.e vault doorway | vault.py cited edit | seal/resolve/tamper/masquerade arms | PASS |
| BO §1.f refusal-injection battery | 8 injection coupons | all arms typed | PASS |
| BO §1.g migration + census | 0054 | ONE line; 84/75/14; lxe DB==disk; downgrade exact | PASS |
| BO §2 coupon range 35–45 + LAW-BORDER-01 | 37 coupons; 2 border coupons | collect count; §6.1 | PASS |
| BO §3 F1 recitals | closed tuples + enumeration coupon | `test_f1_all_12b_refusals_register_recoverable` | PASS |
| BO §4 jurisdiction note | no real-wire act performed or required | fail-first witness note | PASS |

---

# 6. TEST AND VERIFICATION RESULTS

## 6.1 Full suite (one world)

**Command:**
```text
AXIOM_ENVIRONMENT=testing AXIOM_ALLOW_INSECURE_DEV=true
AXIOM_JWT_SECRET_KEY=*** AXIOM_V2_MODE=RESEARCH
AXIOM_DATABASE_URL=sqlite+aiosqlite:///:memory: python3 -m pytest -v
```

**Result:**
```text
v1.0.0: 1239 passed, 2 warnings in 654.63s (0:10:54)
CR-1  : 1240 passed, 2 warnings in 667.39s (0:11:07)
```
(v1.0.0 = 1,202 + 37, inside the BO §2 window 1,237–1,247; CR-1 = +1,
the review's R2 expectation exactly. Warnings = the carried pair.)

**Evidence:** `V2_BE-12B_TESTRUN_TRANSCRIPT.txt` (md5
`c3a21baa4649952a192de429151b088f` · sha256 `da9d3e79…7fc1`).

## 6.2 Database / Migration Evidence

- pre-state: 0053 chain (80/72/13) — rise witnessed
- migration: ONE upgrade line `0053 -> 0054` (both streams, N-O8)
- post-state: tattoo **84/75/14**; 3 new perm rows exact; **lxe compver
  row DB == fresh disk recompute** (recomputed at the gate, not
  re-typed); 4 guard triggers verbatim
- downgrade: exact — 80/72/13 restored, both tables gone, compver
  delete-guard dance restoration asserted
- drift gate at 0054: zero band tokens; inheritance witness

## 6.3 LAW-BORDER-01 (both new gated writers, alembic-applied chain)

- **Border #1 (submit writer, API level):** TestClient on the 0054
  chain — intent-absent → 404 typed; registered intent + submit under
  RESEARCH → 409 `practice_mode_not_armed` (the lawful outcome on this
  world); Level-I after close: ZERO submission rows (refusals persist
  nothing), 1 intent row, guards intact
- **Border #2 (persistence engines, guarded schema):** quarantine
  transition (`no_answer` → `quarantined_unknown`) witnessed on the
  file; `duplicate_submission` + `duplicate_fill_event` typed; identity
  uq schema-fatal on engine bypass; all 4 UPDATE/DELETE guards fired

---

# 7. BEHAVIOURAL EVIDENCE

| Scenario | Expected | Observed | Evidence |
|---|---|---|---|
| Practice ask, all armed (no terminal on station) | typed `practice_terminal_unavailable` | typed, at the boundary seam | injection battery |
| Practice ask, mode RESEARCH | `practice_mode_not_armed` | typed 409, nothing persisted | border #1 |
| LIVE-lane ask at the practice door | `actuation_lane_mismatch` | typed | lane coupons |
| LIVE door under any practice degradation | 12A vocabulary ONLY | `mode_locked`/`posture_mismatch` | non-commutation coupons |
| Terminal timeout / absent retcode | `no_answer` STATE record | STATE record; quarantined at persistence | injected-seam battery |
| Duplicate submission | typed + standing row cited | typed; uq at schema | border #2 |
| Second sighting of same fill | `duplicate_fill_event` + standing id | typed; schema-fatal on bypass | border #2 |
| Investor payload at practice doorway | ABSENT (AAD disjoint) | ABSENT | masquerade coupons (both directions) |
| Wrong passphrase / tamper / no env | ABSENT, no exception | ABSENT | vault arms |

---

# 8. SECURITY EVIDENCE

**FACT** — no credential material on any API surface (coupon-scanned);
the boundary forwards a STATE string only; AAD-disjoint payload families
(masquerade impossible both ways, witnessed); terminal vocabulary exists
ONLY inside the sanctioned provider prefix + the one named boundary file
(amended walls, both directions, exceptions name-literal); investor
class + read-only operating law untouched; funded class NONEXISTENT;
credential scan on the package: class-vocabulary and module names only —
CLEAN-with-classification.
**ENGINEERING ASSESSMENT** — the non-commutation law makes lane confusion
structurally detectable: any future code path that answers across lanes
fails a standing coupon, not a review.
**PROPOSAL** — none this delivery.

---

# 9. GOVERNANCE / AUTHORITY STATE

```text
Implemented: YES (BO §1.a–§1.g complete)
Tests passing: YES (1,239/0)
Delivery submitted: YES
DA self-assessment: ordered scope satisfied on the listed evidence
ITRGA determination: PENDING
Governance approval: NOT YET ISSUED
Production certification: NOT CERTIFIED (capability-before-activation; REQ R-1.4)
```

---

# 10. KNOWN FINDINGS

| ID | Finding | Severity | Status | Evidence |
|---|---|---|---|---|
| `V2-BE12B-DEL-001` | API→boundary→vault chain called the doorway passphrase-less; the vault's fail-closed first arm answered constant-ABSENT; P3 fired on every armed attempt — the PRACTICE lane unreachable through the API even with a perfect sealed vault. Green coupons on either side of the border; the reviewer walked the wire | HIGH | **CORRECTED (CR-1) — awaiting ITRGA close.** R1: passphrase-provisioning law (`AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE`, request-time read INSIDE vault.py only, never module/app state; N4 preserved; operator provisions by console act, file-fed per THE CREDENTIAL LAW). R2: armed-pass border coupon (sealed vault + provisioning + injected fake terminal `accepted` → full API submit persists ONE accepted row on the 0054 chain; duplicate arm typed; vault-removed counter-arm → P3 typed). R3: pre-patch constant-ABSENT reproduced + post-patch flip witnessed. Full re-run **1,240** = 1,239+1 exactly. Both §9 LOW observations discharged same delta (docstring truth refresh; `PRACTICE_BASIS_MAX_AGE_HOURS` register citation). **Compver disclosure (C-2):** locks.py ∈ `_LXE_FILES` — the citation edit moves the lxe rolling hash; new expectation measured from final bytes `b060f435c7c339fb…` (CR1 supplement §1), prior `18ac0bac…` VOID; migration recomputes from landed bytes, coupon re-derives from disk — no stale literal either side. CR1 pack: supplement md5 `000651b5feeb7f0813fcc3d025b1bdcb` · testrun md5 `9eede37a2fae23e9d2842c7a99abd225` · defect witness md5 `7bd44e8f45916de8f64674ba895e3cf9` (E-04…E-06) | CR1 defect witness |
| build-note-1 | First 0054 draft misnamed compver columns (`created_at` vs the true `evidence_ref/registered_at`); probe-SQL law failed it CLOSED on the scratch chain; corrected from the 0051 precedent bytes before any coupon ran | LOW | CLOSED (disclosed) | this table |
| build-note-2 | My own 12A wall coupon caught api.py importing the vault directly — the wall was right; the state-read moved into the boundary (the one doorway) and the wall exception was amended narrowly with a not-vacuous arm | LOW | CLOSED (disclosed) | wall coupon body |

---

# 11. RISKS

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| Practice-wire liveness proven at the typed seam only on this station (no MT5 package) | Real-terminal retcode behavior unproven here | By construction | Injected-terminal battery covers retcode arms; the E-ENV-1 seam is the tested contract; any real-wire witness = separate operator register act (BO §4) | Operator election |

---

# 12. TECHNICAL DEBT

None introduced.

---

# 13. OUT-OF-SCOPE / DEFERRED ITEMS

12C/12D/12E per the ladder · DR-F2 conversion law (12E) · real-wire demo
(separate register act if ever) · 0053/0054 fielded applies (separate
sanctioned acts) · activation instrument (12D, NOT-IN-FORCE template).

---

# 14. EVIDENCE PACKAGE

| Evidence ID | Artifact | Purpose |
|---|---|---|
| E-01 | `V2_BE-12B_SOURCE_TRANSCRIPT.md` (md5 `4bd1ed795f8511aa4cba92fad3bded4c` · sha256 `9b3db32a…c126`) | REM-001, 18 files, literal bodies |
| E-02 | `V2_BE-12B_TESTRUN_TRANSCRIPT.txt` (md5 `c3a21baa4649952a192de429151b088f` · sha256 `da9d3e79…7fc1`) | Full `-v` suite, 1,239 |
| E-03 | `V2_BE-12B_FAILFIRST_WITNESS.txt` (md5 `d094d12458b411e2f2c3e1ef6d112729` · sha256 `db24be47…4fa0`) | OBS-E stash witness (submissions.py → genuine FAIL → byte-identical restore `766a9921…`) + practice-wire witness note |
| E-04 | `V2_BE-12B_CR1_SOURCE_SUPPLEMENT.md` (md5 `000651b5feeb7f0813fcc3d025b1bdcb` · sha256 `fb8fc18c…d41e`) | CR-1 REM-001, exactly 4 files + lxe compver disclosure |
| E-05 | `V2_BE-12B_CR1_TESTRUN_TRANSCRIPT.txt` (md5 `9eede37a2fae23e9d2842c7a99abd225` · sha256 `394e276f…d3c1`) | CR-1 full suite (1,240) |
| E-06 | `V2_BE-12B_CR1_DEFECT_WITNESS.txt` (md5 `7bd44e8f45916de8f64674ba895e3cf9` · sha256 `25ab34f7…6f9f`) | R3: pre-patch constant-ABSENT repro + post-patch flip + armed-pass Level-I |

---

# 15. DA SELF-ASSESSMENT

> The DA assesses that the implemented scope satisfies the Build Order
> requirements based on the evidence listed in this report, with the
> practice-wire liveness witnessed at the typed seam per the BO §4
> jurisdiction note (no real-wire act performed or required). This is a
> Development Authority assessment only and does not constitute ITRGA
> approval, certification, or production authorization.

---

# 16. DELIVERY STATUS

```text
Build Order executed: YES
Implementation complete for ordered scope: YES
Evidence package complete: YES (E-01…E-03)
Known findings disclosed: YES (2 build notes)
Delivery Report submitted: YES
ITRGA determination: PENDING
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
