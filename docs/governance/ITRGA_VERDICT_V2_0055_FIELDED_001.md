# ITRGA VERDICT — V2 FIELDED HEAD 20260909_0055: **FIELDED**
**BE-12C (LIVE-EXEC CANCEL/MODIFY + EXPANDED UNKNOWN-STATE) — FIELDED**

**Verdict ID:** `ITRGA-VERDICT-V2-0055-FIELDED-001`
**Date:** `2026-09-09`
**Authority:** ITRGA · BO-V2-BE12C-001 SS1.g · ITRGA-REV-V2-BE12C-CR-001 (APPROVED; suite floor 1,265)
**Card:** ITRGA-V2-0055-FIELD-APPLY-CARD-20260909 (+ ERRATUM E-0055-A10.3)
**Witnesses received:** `0055-APPLY-RUN-V1-20260909120822` (apply run; A0–A10.2 PASS, halt at A10.3 pin-form only) + `0055-CLOSE-RUN-V1-20260909133559` (closing witness; 34/34 gates PASS) + `0055-APPLY-FINAL-STATE.txt` (VERDICT PASS)

---

## 1. THE ACT AND ITS PROOF (what the two witnesses jointly establish)

- **The mutation was exactly one and exactly once:** `Running upgrade 20260909_0054 -> 20260909_0055` — one line, zero bad tokens, on the fielded `axiom_dev.db`, from anchor-verified head 0054. Never re-run.
- **Reversibility was proven BEFORE the apply** on a byte-copy: upgrade→downgrade exact (86/77/15 down to 84/75/14; `lxe-1.1.0` removed, `lxe-1.0.0` preserved; delete-guard danced and re-established).
- **Fielded terminal state, verified twice (apply run + close run, pin-identical):** revision `20260909_0055 (head)`; tattoo **86/77/15**; eight immutable guard names exact; six 12B+12C indexes exact; `v2_live_exec_modify_event` present and EMPTY; 12B pair standing empty; two 12C permission rows content-exact (`modify.write` SAL-4, `modifies.read` SAL-2).
- **Append-only registry law in the field:** compver holds BOTH rows content-exact — `lxe-1.0.0` (`b060f435…`, BO-V2-BE12B-001, untouched) and `lxe-1.1.0` (`d09306f1…` == **disk recompute**, BO-V2-BE12C-001). The apply moved zero source bytes (6/8-file hashes re-proven post-mutation).
- **Guard/CHECK witness at the field:** modify guard pair refuse exact + rolled back; **all four closed CHECK vocabularies visible in the DB's own DDLL** (printed at C3.0: `ck_v2_live_exec_modify_event_ck_v2_lxmod_{verb,outcome,election,data_class}`) with the election (`auto_recovery`) and verb (`close`) probes typing the rendered names; compver refusals carry the ORIGINAL `registry` literals (upgrade never touched those guards).
- **Append-only lineage preserved:** the 12A wire-proofed intent (`7ac49b2873c3…`, 1 row) byte-standing; no armed act of any kind (submissions/fills/modifies all 0 in the field); no TD/PRACTICE variable at act start or end.
- **Drift: ITEMIZED pass** — the printed operations are exactly the 9 inherited V1 tokens; zero `v2_`/`live_exec`/`lxmod`/`modify_event`.

## 2. THE ERRATUM, ADJUDICATED WITHIN THE RECORD

**E-0055-A10.3** (pin-form correction, second of its class after E-0054-A11.4): the A10.3 halt was structural-correct with an over-tightened ITRDA pin — the CHECK refusals fired as law requires, under rendered names (`ck_<table>_<short>`). Adjudicated: no state defect, no re-mutation; the close run's C3.0 DDL print is the erratum's own field evidence. Standing drafting rule amended for 12D-era cards: refusal-text pins are taken from the rendered DDL, pre-verified on rehearsal render before the field act.

## 3. VERDICT AND REGISTER LINE

```text
BE-12C FIELDED. 12A OPERATING. 12B FIELDED. LIVE REGISTERED_LOCKED.
Register line, in force:
BE-12A OPERATING | BE-12B ACCEPTED+FIELDED | BE-12C ACCEPTED+FIELDED (PRACTICE=WIRED) | LIVE=REGISTERED_LOCKED | funded account: NONE | suite floor 1,265 | fielded head 20260909_0055
```

- **CARD-0055 CLOSED.** The rehearsal copy `axiom_dev.db.rehearsal-0055-*.db` may now be deleted (witness acknowledged); the anchor `axiom_dev.db.pre-0055-20260909120822.bak` is RETAINED per rollback-discipline.
- **Ordering law satisfied for the next rung:** 12C is ACCEPTED + FIELDED — **the 12D build order (activation instrument + kill-switch) is now legally authorable.** It will be drafted on operator direction, per DR-1: 12D = the activation instrument + kill-switch chapter, with the 12E consolidations (DR-F2 conversion law, honesty pair, counterfeit-witness scan, compver rows with last build) carried on the register until their band.
- LOW-2 (SELECT-then-insert duplicate pattern) remains register-logged for 12E.

> Independent governance determination on the two field witnesses above; authorizes only the state explicitly stated. **ITRGA.**
> **We don't guess. We prove.**

**END OF VERDICT**
