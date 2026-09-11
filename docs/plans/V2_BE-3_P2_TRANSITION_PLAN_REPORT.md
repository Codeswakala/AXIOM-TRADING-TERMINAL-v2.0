# Plan Report — BE-3 P2 Status Transition Design Plan Submission

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-P2-TRANS-PR-001 |
| Plan | AXIOM-V2-BE-3-P2-TRANS-PLAN-001 **v1.1.0** (`docs/plans/V2_BE-3_P2_TRANSITION_DESIGN_PLAN.md`) |
| Responds to | ITRGA-INT-V2-BE-3-P2-TRANSITION-001; ITRGA-REV-V2-BE-3-P2-TRANS-PLAN-001 |
| Initiating decision | AXIOM-V2-OD-BE-3-P2-003 |
| Author | Development Authority (DA) |
| Date | 2026-08-29 |
| Status | RESUBMITTED FOR ITRGA REVIEW — design only |

---

## 1. Change summary

v1.1.0 — closes ITRGA-REV-V2-BE-3-P2-TRANS-PLAN-001 findings TR-001…TR-004
(all LOW; no design defects found; review verified the mechanism against the
accepted P2 source and gate records):

| Finding | v1.1.0 correction |
|---|---|
| TR-001 | Already-applied re-run pinned as a **clean audited no-op** (ITRGA-recommended): `start`+`complete` with `no_op: "already-applied"`, no refusal event, history unchanged, exit 0 — consistent across §1/§3.3/§4(P-2)/§6/§8 |
| TR-002 | §9 rewritten as a boundary table annotating the authority variable per step: SET for the 0042 upgrade; **STILL SET** for the re-upgrade attempt (P-1 passes → **P-5 is the proven refusal**); NOT required for downgrade; UNSET as the recorded final step |
| TR-003 | Refusal-audit insert failure → distinct `REFUSAL AUDIT WRITE FAILED: <precondition-name>` error; precondition preserved in error + SECURITY line; fault-injected test added to §8 |
| TR-004 | §9 revision string corrected to `20260825_0041` |

v1.0.0 — first version. Designs the single governed transition
`architecture_candidate → contract_tested` for `twelvedata`, per the
Operator-initiated chain. Central mechanism decision: **one-shot governed
migration** (0041-proven guard-handling pattern) — a runtime transition
writer is explicitly rejected so the codebase retains zero application
write paths to provider status.

## 2. Intake-requirement traceability

| Intake §2 item | Plan section |
|---|---|
| 1 Authorization basis / one-shot / exclusions | Part 1 |
| 2 Mechanism + atomicity + no permanent weakening | Part 2 |
| 3 Invocation surface (migration gate + Operator confirmation + idempotent re-run) | Part 3 |
| 4 Preconditions (default-deny; durable refusal audit under rollback semantics) | Part 4 |
| 5 History semantics + explicit downgrade choice with rationale | Part 5 |
| 6 Audit actions per `provider.*` convention | Part 6 |
| 7 Post-transition invariants (proven) | Part 7 |
| 8 Test matrix (precondition/immutability/atomicity/idempotence/downgrade/interruption) | Part 8 |
| 9 Fresh PostgreSQL verification (full chain, boundaries echoed) | Part 9 |
| 10 Provenance and delivery | Part 10 |
| §3 out-of-scope mirror | Part 11 |

## 3. Key design choices flagged for review

1. **Migration over runtime writer** (Part 2.1) — preserves the binary
   "refuse all" guard; no standing status-mutation machinery.
2. **Refusal audits via independent durable connection** (Part 4) — a
   rolled-back migration cannot erase its own refusal record; DEL-001's
   durable-unit principle applied to the migration context.
3. **Downgrade = reversal append, never history deletion** (Part 5.2) —
   append-only history outranks downgrade symmetry; post-reversal
   re-transition intentionally requires a fresh governed chain (P-5).
4. **Already-applied re-run = audited no-op** (Part 3.3) — deterministic
   head without weakening one-shot semantics.

## 4. Assumptions (labeled)

| Assumption | Status |
|---|---|
| Final determination ID and run correlation as cited in the intake | Taken as recorded governance facts (basis, not re-derived) |
| Transition Build Order ID (used as the authority-ref gate value) | Placeholder until the Build Order exists |
| PostgreSQL remains the production-equivalent dialect | Per programme record |

## 5. Preparation confirmations

While producing this plan the DA performed: no implementation, no migration,
no source change, no status/history/entitlement change, no network activity,
no credential access, no frontend work, and **no Git/GitHub operation**.
The workspace source tree is unchanged from the accepted P2 state; this
submission adds only the two plan documents.

**End of Plan Report**
