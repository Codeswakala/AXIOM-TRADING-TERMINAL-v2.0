# ITRGA-DET-V2-BE-6-FINAL-001 — DETERMINATION: Band BE-6 (BO-V2-BE-6-001), Level-I/II full-verify

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Delivery of record | `AXIOM-V2-BE-6-DR-001` **v1.0.1** + Rev-2 evidence (API/testrun/source Rev 2; annex Rev 1 unchanged) |
| Governing chain | `ITRGA-CN-V2-BE-6-001` → `ITRGA-REQ-V2-BE-6-PLAN-001` → plan PRV (ACCEPTED, zero corrections) → **BO-V2-BE-6-001** → DR intake (`ITRGA_INT_V2_BE-6_DR_001`, C-1) → this determination |
| Review depth | **Full-depth** on both evidence planes, corrections closed on executed proofs |

## 1. Verdict

**C — PASS: full-verify.** Terminal state T-1…T-12 complete with executed, independently-reproduced evidence; Pins P-1…P-7 honored structurally. Correction chain: **C-1 CLOSED** (cluster 1 + cluster 2, route (a)); **C-2 RECORDED, deferred-class** (§5).

## 2. Terminal state — gate map (evidence, not assertion)

| T | Proof inspected/executed |
|---|---|
| T-1 | Head `20260903_0046` on DA chains, single head; literal-revision upgrades; models registered same-unit |
| T-2 | Both tables exact to plan §1.2: three CHECK vocabularies each (incl. single-value `basis` / `basis_label`); `uq_v2_pfdef_id_seq` refused a duplicate behaviorally; determinism anchor exercised by idempotency; the two single-value CHECKs refused `real`/`live_account`/`account-state` in executed probes |
| T-3 | 32-trigger census (28+4) asserted in tests; 4 guard messages byte-exact against the plan literals (verified against my plan copy) |
| T-4 | 41 permissions; 6 grants content/SAL exact (admin 4, operator 2); forbidden-marker guard green; no account/order/position/broker vocabulary in any of the 41 |
| T-5 | compver 6; `portfolio_risk_engine = pre-1.0.0`; hash recipe (path-NUL-bytes rolling digest over the 4 U-2 files) reproducible — the 0046 application act re-pins against REM literals |
| T-6 | **9 distinct tokens = the verified inherited V1 set, zero BE-6/V2 tokens** — direct run at the 0046 head, itemized identically to the BE-5-era verified set (table `audit_write_failure_records` + its 2 indexes added; 6 V1 indexes removed) |
| T-7 | No-touch: BE-3 provider + BE-4/BE-5 compver rows content-identical across 0046 (test-executed census) |
| T-8 | Six states schema-reachable/executed as designed; typed `insufficient` (value None, never fabricated); `historical_real` define-refusal executed; 400/403/404/409 refusal classes executed **with durable domain audits** (post C-1) |
| T-9 | Level I transcript 15/15 ASSERTs; suite **911/911** (= 856 + 55; module itemization 17+7+14+17 proven in both transcripts); REM-001 Rev-2 manifest re-hashed **15/15 exact by the ITRGA**; annex P-7 recomputed and equal (§3) |
| T-10 | Registers staged (IMPLEMENTED only; risk +2; debt +2; 30.x serialization) |
| T-11 | Construction-token scan (no recommendation/rebalance/hedge/action); no preview/export surface; RESEARCH-only writers; socket guard every test |
| T-12 | No credential anywhere; no Git operations by DA or ITRGA; full-depth review posture |

## 3. Independent ITRGA verifications (this review, executed in this workspace)

1. Artifact identity: all 4 DR table hashes byte-matched on receipt (twice: Rev 1 and Rev 2).
2. Manifest recursion: REM-001 literals extracted and re-hashed **15/15 exact** in both revisions.
3. **P-7 executed without the engine**: annex pinned values reproduced to ≤1e-12 (HHI 0.3450; Top-2 0.7500; gross/net 1/1; MaxDD −0.0388349515; scenario −0.1750), and the un-stated anchors (volatility `0.034494498661…`; VaR-hist `0.020202707318…`; VaR-param `0.053454090…`) match the formulas both the engine and the tests implement; runtime sample (−0.12 = 0.4×−0.3) consistent.
4. V1 immutability: all 5 attestation pins (4 reuse files + `validation/service.py`) byte-matched against the frozen review clone.
5. C-1 fix-class review: `_audit_compute_refusal` appends then **commits before raising** (durability survives request rollback; no in-session state is staged at any of the 5 call sites — premature-commit risk verified absent); cluster-2 probe deletes a registry row pre-compute and proves 409 + audit naming `credited_weight: 0.4` + **zero report rows**.
6. Bookkeeping: PASSED-line count `911` == summary; per-module executed counts equal the DR itemization; api module grew 9→14 exactly by the 5 probes.

## 4. Corrections register

- **C-1 (intake) → CLOSED.** Cluster 1: `portfolio_risk.compute.unknown` emitted on all four compute-refusal classes with typed `refusal_class`, durably audited (4 Level-I probes + 4 suite probes). Cluster 2: silent `continue`-on-unknown-instrument replaced by typed `unknown_instrument` 409 with the dropped weight named; side-effect-free. Suite restated 906→**911**.
- **C-2 (recorded at this determination, deferred-class, per the BE-5 C-2 precedent): editorial consistency of DR v1.0.1.** Despite the Revision line and §3 total (55/911) being correct, three cells were not re-stamped: §2 **T-9** still reads "raw `pytest -v` 906/0 (= 856 + 50)"; §3's heading still reads "856 + 50 = 906"; §2 **T-8**'s cell omits the amended audit enumeration that §4b promises ("the DR §2 T-8 row is amended accordingly" — the amendment lives in §4b, not the cell). **Required action (no re-delivery demanded now):** at the next evidence-channel transmission (0046-application package or the acceptance-sync package, whichever first), the DA ships the DR with those cells re-stamped — floor 911 = 856 + 55, itemization 17/7/14/17, and T-8's text carrying the durable compute-refusal audit enumeration. The register sync references **911** as the floor immediately (capability/state entries cite the executed 911, not the stale cells). Evidence artifacts themselves are correct and hash-pinned; this correction is presentation-class, not substance-class.

## 5. Observations (non-blocking, on the record)

O-1: annex vol/VaR expecteds formula-inline in tests; independence supplied by ITRGA recomputation (executed). O-2: `ix_v2_pfdef_portfolio` additive-benign, not itemized in plan §1.2 DDL — the 0046 application act's schema census verifies the settled set. O-3: 119-obs runtime literals are execution artifacts, not pins. O-4: `stale`/`unknown` producerless-by-design (disclosed; schema-reachable). O-5 (new): the superseded-generation 409 probe appears in §3 of the Level-I transcript and its durable audit in §6 — cross-section referencing; harmless, recorded.

## 6. Two-plane conclusion

- **Level I (executed):** PASS — 911/911 on the certified pin (pytest 8.4.2-era posture noted: the suite ran in the DA environment; operator environment carries the same pin), Level I transcript probed, drift gates at both heads, zero-network, zero-credential.
- **Level II (source):** PASS — all contracts/engines/writers/migration/tests reviewed full-depth; road-map §0 fidelity maintained; V1 surface frozen (pins proven); additive-only modifications to the three enumerated files + disclosed generational scoping of the BE-5 drift gate (PGF-014 precedent).

## 7. Recommendation to the Operator

1. **Acceptance authorization** → maturity rows `Portfolio Research` and `Risk Research` → **COMPLETE** (evidence: this determination + the intake review's verdict map); BO-V2-BE-6-001 closable.
2. Register sync per DR §6 with **911** floor (per C-2 hygiene), risk +2/debt +2 as itemized, state serialization per the 30.x convention.
3. **Working-DB application of 0046** = the next separate sanctioned act. Its instrument inherits the complete 0045 discipline: pre-upgrade pins of ALL delivered files (REM-Rev-2 literals as recompute source), behavioral uniqueness probes (`uniqprobe` pattern), live guard-message refusals, trigger census 32, permission census 41, compver census 6 with engine-hash recomputation from the literals, no-touch content digests of BE-2…BE-5 protected state, itemized drift = 9 tokens, tri-binding rollback anchor, fail-closed design, `sqlite_master` name-scoped introspection only, and simulated-pack validation of every SQL string before production.
4. Corrections register for the band stands: C-1 closed, C-2 (editorial) deferred-open until its appointed transmission. Nothing else is open in BE-6.

**ISCRIVED AND CLOSED as DETERMINATION `ITRGA-DET-V2-BE-6-FINAL-001` — verdict C: full-verify PASS. Awaiting only the Operator's acceptance authorization; no further ITRGA action is pre-authorized beyond this delivery.**

— ITRGA, 2026-09-03. We don't guess. We prove.
