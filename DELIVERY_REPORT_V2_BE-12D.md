# AXIOM — DA DELIVERY REPORT

# BE-12D — ACTIVATION INSTRUMENT + KILL-SWITCH

**Delivery Report ID:** `AXIOM-V2-BE-12D-DR-001`
**Version:** `v1.0.0`
**Date:** `2026-09-09`
**Development Authority:** `DA`
**Build Order:** `BO-V2-BE12D-001` (filed md5 `74d50754e5f856c149da68a78684c02c` · sha256 `acea9f9a…def2`)
**Design Record / Approved Plan:** `DR-V2-BE-12-001 (as adopted; sub-ladder 12D; DR-2 L3/L5)`
**Repository Commit / Head:** `git HEAD 9c78afa (frozen; custody Operator-only); alembic chain head on DA test chains: 20260909_0056; fielded lineage: 20260909_0055 (untouched)`
**Status:** `DELIVERED — AWAITING ITRGA REVIEW`

---

# 1. PURPOSE

Implement BO-V2-BE12D-001: the activation instrument (the table IS the
force switch; the template NOT-IN-FORCE on its face; NO writer route)
and the kill-switch (singleton, closed lifecycle, THE sanctioned valve,
re-arm blocked until cleared), with L3/L5 moved to table-backed fact
readers under an UNCHANGED lock order, migration `20260909_0056`, and
the governor-cycle border with counter-arms. **FORCE IS NEVER TAKEN: no
force-verb exists; the activation table is zero-row in every world's
end state.** Execution authority: NONE. Funded account: NONE.

---

# 2. AUTHORITY AND SCOPE

## 2.1 Governing Inputs

| Artifact | ID / Version | Role |
|---|---|---|
| Requirement | `REQ-V2-BE-12-001` (R-1.2/R-3.4/R-3.6; adopted R-6.2 wording) | Defines required outcome |
| Design Record | `DR-V2-BE-12-001` (12D; DR-2 L3/L5; DR-4 floor) | Defines approved architecture |
| Build Order | `BO-V2-BE12D-001` | Authorizes implementation |
| Standing laws | ACTIVATE-NOTHING (N4/N-O11) · DEL-001 defense · LAW-BORDER-01 (ext. §1.f) · E-0054-A11.4 itemized drift · E-0055-A10.3 rendered-DDL pins · C-2 | Binding disciplines |

## 2.2 Implemented Scope

BO §1.a–§1.g complete. **No force-verb built, ever** (§1.a premise lock
honored structurally: absence coupons + surface enumeration).

## 2.3 Not Implemented

Taking force (a future operator register act under a future build
order — the template's own face says so) · 12E (reconciliation +
incident; the carry-list rides: DR-F2 conversion law, honesty pair,
counterfeit-witness scan, LOW-2) · any real-network act. Excluded by
order, not defect.

---

# 3. IMPLEMENTATION SUMMARY

| Area | Implemented Artifact | Description |
|---|---|---|
| Activation table | `app/db/models/v2_live_activation.py` + migration | **THE TABLE IS THE FORCE SWITCH**: zero-row == L3; sole discriminator CHECK ('SOLE') + unique index (at most one row ever); version CHECK ('lai-1.0.0' only); authority-reference columns; **`data_class` CHECK = single member 'live_marker'** — 'simulated' structurally BANNED, no test world can simulate force (schema arm witnessed live); guard pair verbatim |
| Template | `activation/template.py` | READ-ONLY artifact, versioned `lai-1.0.0`, **NOT-IN-FORCE ON ITS FACE** (opening clause: "THIS TEMPLATE CONFERS NO ACTIVATION"; force = future register act needing funded-posture witness + step-up + kill-switch check — pinned substrings coupon-witnessed); hash recomputed from final bytes at every ask (no stored literal) — value at this delivery: `142f87723a63420f…` (full in E-01) |
| Activation reads | `activation/engine.py` + GET `/activation` (SAL-2) + GET `/activation/template` (SAL-3) | Zero-row ⇒ typed not-in-force shape on the envelope face, never an error; hash echoed == recompute; **NO POST/PUT/DELETE route exists** (openapi enumeration coupon: activation routes GET-only) + **NO writer code path** (token scan, definition-form excluded) |
| Kill-switch | `killswitch/engine.py` + `v2_live_kill_switch` | Singleton sole-row; closed cycle armed/pulled/cleared; `data_class` CHECK = 'evidence' only; **THE VALVE** (drop UPDATE guard → ONE transition → recreate → verify restored, hard-fail otherwise — the compver-dance pattern); every cell of the lifecycle law typed: re-arm while engaged ⇒ `killswitch_armed` NON-FIRING; pull-not-armed ⇒ `killswitch_state_invalid`; clear ⇒ THE single sanctioned path (token scan proves no other 'cleared' writer); zero-row read ⇒ `intact`; R-3.4 stamps on every transition |
| Governor verbs | POST `/killswitch/{arm,pull,clear}` (SAL-4 + step-up) + GET `/killswitch` (SAL-2) | Operator-initiated ONLY (activate-nothing scans: no timer/scheduler/background path) |
| L3/L5 wiring | `api._actuation_door` | Both locks read TABLE-BACKED fact readers over the real chain; **LOCK_ORDER byte-recital UNCHANGED** (L1..L6 tuple identical; order law re-proven: L1-and-L3 fixture answers `mode_locked`); L5 truth table all four sole-row states |
| Database | `20260909_0056` | +2 tables +4 guards +6 perms +1 compver INSERT-ONLY `lxe-1.2.0` (13-file set; template.py rides the hash — the artifact is compver-scoped); ONE line; **tattoo 90/83/16**; ZERO seed rows (zero-row IS the law); downgrade exact (86/77/15; both prior lxe rows preserved); **rendered CHECK names enumerated per E-0055-A10.3** (`ck_v2_live_activation_instrument_ck_v2_lai_*`, `ck_v2_live_kill_switch_ck_v2_lks_*` — from the DB's own DDL) |
| Tests | `tests/test_v2_be12d_{locks_lanes,killswitch_engine,migration_borders}.py` | **25 coupons** (10/7/8) |

---

# 4. FILE CHANGE INVENTORY

Full manifest (16 files, literal bodies + SHA-256): REM-001
`docs/evidence/V2_BE-12D_SOURCE_TRANSCRIPT.md`. **Byte-still recitals:**
`tests/test_v2_be9_boundaries.py` == `9ba9fd82…f91f` · migration 0055 ==
`869014e3…` · pbr == `4c243435…178b` · **`locks.py` UNTOUCHED** (the
lock semantics did not move — only their fact inputs; consequence:
lxe-1.1.0's 8-file set intact, its row stands against the same bytes).

**C-2 compver disclosure:** `lxe-1.2.0` expectation measured from final
bytes: `d25c48579def993b…` (full in E-01); `lxe-1.0.0` (`b060f435…`)
and `lxe-1.1.0` (`d09306f1…`) STAND — all three rows coexist on every
0056 chain, witnessed, with the update path guard-refused live.

---

# 5. REQUIREMENT TRACEABILITY

| Requirement | Implementation | Evidence | Result |
|---|---|---|---|
| §1.a activate-nothing | operator verbs only; step-up mandatory; no self-activity | scans + counter-arms | PASS |
| §1.b.1 force switch table | model + migration + CHECKs | schema arms live (simulated banned; singleton) | PASS |
| §1.b.2 template | NOT-IN-FORCE face + hash + no-writer | pinned substrings; recompute; enumeration + scan | PASS |
| §1.b.3 read-only surface | 2 GETs | openapi GET-only coupon | PASS |
| §1.b.4 L3 witness + armature | fact reader + rolled-back armature | order coupons; zero-row after | PASS |
| §1.c.1–.2 valve + lifecycle | engine `_valve` + matrix | every cell typed; inversion coupon | PASS |
| §1.c.3 L5 wiring | fact reader | truth table over real chain | PASS |
| §1.c.4 surface | 3 POSTs + GET | governor border | PASS |
| §1.d lane law | untouched practice lane | armed-switch non-commutation coupon | PASS |
| §1.e vocabularies | GOVERNOR_REFUSALS + F1 | declared-overlap recital (6+5+9+2−1) | PASS |
| §1.f DEL-001 defense | governor cycle border + counter-arms | real-chain border, no injection-only | PASS |
| §1.g migration | 0056 | ONE line; 90/83/16; rendered pins; downgrade exact; itemized drift | PASS |
| §2 coupon range 22–32 | 25 | collect count | PASS |

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
1290 passed, 2 warnings in 708.81s (0:11:48)
```
(= 1,265 + 25 — **inside the BO §2 window 1,287–1,297.** Warnings = the
carried pair.)

**Evidence:** `V2_BE-12D_TESTRUN_TRANSCRIPT.txt` (md5
`1091d349960940c37e532d5b2fee1f2e` · sha256 `3bb2ec42…7764`).

## 6.2 Database / Migration Evidence

Pre 0055 (86/77/15) → ONE line → post 0056 **90/83/16**; all three lxe
rows, 1.2.0 == disk recompute; ZERO rows in both new tables; simulated
class dies at schema in both; rendered CHECK names asserted from the
DB's own DDL; downgrade exact preserving 1.0.0+1.1.0; drift ITEMIZED.

## 6.3 The governor cycle border (§1.f, real chain)

pull-before-arm 409 typed → step-up-absent 409 typed → intact read →
**arm 200 → armed/engaged read → pull 200 → re-arm 409
`killswitch_armed` NON-FIRING → clear 200 → re-arm 200** →
CLEARED→ARMED end state; template hash echoed == recompute; Level-I:
sole row, guard pair verified after every valve pass, direct SQL dies,
singleton schema-fatal. **The activation table zero-row in every end
state — force never taken.** Armature proof: future-lawful shape
in-transaction, lock evaluated in-force (L3 passed → L4 answered),
ROLLED BACK, zero-row witnessed after.

---

# 7. BEHAVIOURAL EVIDENCE

| Scenario | Expected | Observed | Evidence |
|---|---|---|---|
| Activation read, zero-row | typed not-in-force shape | as expected, never error | border |
| Template read | face + hash == recompute | as expected | border |
| Arm from intact / from cleared | 200 armed | as expected | border + matrix |
| Re-arm while armed/pulled | `killswitch_armed`, non-firing | typed, state unchanged | matrix + border |
| Pull not-armed (3 cells) | `killswitch_state_invalid` | typed | matrix |
| Clear (all 4 cells) | intact/cleared shapes; single path | as expected | matrix + token scan |
| Direct SQL transition | guard refusal | dies typed | inversion |
| Practice ask under armed switch | practice vocabulary only; lawful ask passes | as expected | lane coupon |
| Simulated force row | schema-fatal | IntegrityError | schema arm |
| L1-and-L3 fixture | `mode_locked` (order law) | as expected | lock coupons |

---

# 8. SECURITY EVIDENCE

**FACT** — no force-verb exists (surface enumeration: activation routes
GET-only; token scan: no writer path); no self-activity path (scans);
every transition operator-initiated with step-up stamped; 'simulated'
structurally banned from the force table; the kill-switch is
evidence-class, never trade data; credential scan: fixture tokens only.
**ENGINEERING ASSESSMENT** — the force switch's strongest property is
that its OFF state is the absence of a row: there is nothing to toggle,
no flag to flip, no code path to subvert — force requires a future act
that writes a row this band cannot write.
**PROPOSAL** — none this delivery.

---

# 9. GOVERNANCE / AUTHORITY STATE

```text
Implemented: YES (BO §1.a–§1.g complete)
Tests passing: YES (1,290/0)
Delivery submitted: YES
DA self-assessment: ordered scope satisfied; force NEVER taken; zero-row witnessed in every end state
ITRGA determination: PENDING
Governance approval: NOT YET ISSUED
Production certification: NOT APPLICABLE (capability-before-activation; REQ R-1.4)
```

---

# 10. KNOWN FINDINGS

| ID | Finding | Severity | Status | Evidence |
|---|---|---|---|---|
| authoring-note-1 | No-writer scan initially caught the model's class-definition line; needle sharpened (a definition is not a writer) | LOW | CLOSED (disclosed) | witness |
| authoring-note-2 | No-other-clear scan caught the model's CHECK declaration; same sharpening (a declaration is not a writer) | LOW | CLOSED (disclosed) | witness |
| authoring-note-3 | One cross-corpus amendment beyond the BO's named supersession: the 12B structural pin carried `PRACTICE=WIRED` as a LINE invariant; the BO §5 ordered line carries the activation posture — the pin AMENDED BY CITATION to read the fact from its structural home (`BOUNDARY_STANCE`), the fact stands, only its carriage moved. Surfaced by a genuine suite failure at 1,289 and corrected before the seal | LOW | CLOSED (disclosed) | witness + coupon body |

---

# 11. RISKS

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| The valve dance briefly drops the UPDATE guard inside a transaction | A concurrent writer in that window | Singleton-writer house model (LOW-2 12E register item covers the family) | Hard-fail if guard not verified-restored; transaction dies whole | 12E register |

---

# 12. TECHNICAL DEBT

None introduced.

---

# 13. OUT-OF-SCOPE / DEFERRED ITEMS

Taking force (future register act, future BO) · 12E (carry-list:
DR-F2 · honesty pair · counterfeit-witness scan · LOW-2) · 0056
fielded apply (separate sanctioned act) · real-network acts.

---

# 14. EVIDENCE PACKAGE

| Evidence ID | Artifact | Purpose |
|---|---|---|
| E-01 | `V2_BE-12D_SOURCE_TRANSCRIPT.md` (md5 `1b350f380e4b306626f9a2286fd71824` · sha256 `def2a678…91fb`) | REM-001, 16 files + C-2 lxe-1.2.0 + template-hash disclosure |
| E-02 | `V2_BE-12D_TESTRUN_TRANSCRIPT.txt` (md5 `1091d349960940c37e532d5b2fee1f2e` · sha256 `3bb2ec42…7764`) | Full `-v` suite, 1,290 |
| E-03 | `V2_BE-12D_FAILFIRST_WITNESS.txt` (md5 `f6ebf35f6b0804e490fcac5ca73a271f` · sha256 `5e09c242…1c2f`) | OBS-E stash witness (killswitch engine → genuine 6-coupon fan FAIL → byte-identical restore `beccf2a3…`) + per-writer witness note + 3 authoring notes |

---

# 15. DA SELF-ASSESSMENT

> The DA assesses that the implemented scope satisfies the Build Order
> requirements based on the evidence listed; that the three governor
> writers are each witnessed over the real corridor with counter-arms;
> and that FORCE WAS NEVER TAKEN — the activation table stands zero-row
> in every world's end state, and no code path exists that could change
> that under this band. This is a Development Authority assessment only
> and does not constitute ITRGA approval, certification, or production
> authorization.

---

# 16. DELIVERY STATUS

```text
Build Order executed: YES
Implementation complete for ordered scope: YES
Evidence package complete: YES (E-01…E-03)
Known findings disclosed: YES (3 authoring notes)
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
