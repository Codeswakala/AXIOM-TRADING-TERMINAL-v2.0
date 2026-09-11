# Plan Report — AXIOM V2 BE-3 P2 Design Plan Submission

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-P2-PR-001 |
| Plan | AXIOM-V2-BE-3-P2-DA-PLAN-001 **v3.0.0** (`docs/plans/V2_BE-3_P2_DESIGN_PLAN.md`) |
| Responds to | ITRGA-REQ-V2-BE-3-P2-PLAN-001; ITRGA-REV-V2-BE-3-P2-PLAN-001; ITRGA-REV-V2-BE-3-P2-PLAN-002 |
| Author | Development Authority (DA) |
| Date | 2026-08-25 |
| Status | RESUBMITTED FOR ITRGA REVIEW — design only |

---

## 1. Change summary

v3.0.0 — closes ITRGA-REV-V2-BE-3-P2-PLAN-002 findings PLAN-005…008
(PLAN-001…004 confirmed closed by that review):

| Finding | v3.0.0 correction |
|---|---|
| PLAN-005 (High) | Impossible atomicity claim removed. **Durable pre-call audit gate**: `call_started` committed before any network call (no durable start = no call); `call_completed` after; completion-audit failure → immediate hard stop + independent fail-safe incident channel (SECURITY log + evidence-directory marker, not the failed DB path) + mandatory reconciliation of durable start records before resumption. Call states `completed / refused-before-call / indeterminate-after-start` defined; timeout/cancel/process-loss reported as indeterminate, never absent. |
| PLAN-006 (Medium) | **Run-scoped server-side AttemptBudget token mechanism** (init 35; debit before EVERY attempt incl. auth probes and retries; atomic refusal at zero; attempt_number/budget_remaining/call_state added to the E.5 evidence schema; worst-case accounting table shows retry storms bounded to 35 by the gate; boundary tests specified). |
| PLAN-007 (Medium) | Entitlement migration defined per dialect: PostgreSQL trigger/function AND SQLite dual-trigger drop→update→re-create table with identical post-state; SQLite lifecycle + direct mutation-refusal tests in DA workspace PLUS Operator PostgreSQL fresh verification; per-dialect matrix in §J. |
| PLAN-008 (Low) | Footer corrected to v3.0.0; all version references now consistent. |

v2.0.0 — closed ITRGA-REV-V2-BE-3-P2-PLAN-001 findings PLAN-001…004:

| Finding | v2.0.0 correction |
|---|---|
| PLAN-001 (High) | **No provider payload body — raw, partial, encrypted, or otherwise — is persisted in P2, in any environment, Operator's included.** Bodies are transient process-memory values discarded after schema validation + hashing. All retention provisions removed from E.5/F/H/K. Exhaustive E.5 evidence schema enumerates the only persistable artifacts (request class, redacted URL, status, body hash, verdict, error category, latency, timestamps, run metadata). |
| PLAN-002 (High) | Post-determination promotion migration removed from requested authorities (L.3) and declared a P2 non-goal (L.2). P2's sole registry mutation is the entitlement-recording migration. Promotion requires: Operator review of final determination → separate transition design plan → ITRGA review → separate transition Build Order → fresh PostgreSQL evidence (I.2/A.2). |
| PLAN-003 (Medium) | **Full-universe option adopted**: SYMBOL-SWEEP request class added — every one of the 12 canonical instruments is individually live-exercised; budget revised to ≤35 calls (16 planned); A.1 claim and E.1 matrix now use identical scope language. |
| PLAN-004 (Medium) | **Option 1 adopted**: authenticated admin-authorized API endpoint is the ONLY invocation surface; unauthenticated/local CLI forbidden (import-boundary enforced); audit-append failure → fail-closed abort; identity/permission/correlation/audit tests added to the J matrix. |

The P1 approved state remains unchanged; no implementation exists or is
proposed to exist under this submission.

## 2. Assumptions (all labeled)

| Assumption | Status |
|---|---|
| Twelve Data API endpoint families (`time_series`, `quote`), auth model (apikey), and error shapes | **Unverified candidate documentation** (Level III) — proven only by a future contract test |
| Any tier/limit/coverage/price/licensing/data-rights value | **NOT PROVEN** — requires Operator entitlement evidence; never a runtime assumption (plan §B.2) |
| Operator will open an account | **Not assumed** — the plan designs the gate (§B.1); a negative Operator decision simply leaves P1 as the end state |
| PostgreSQL remains the production-equivalent dialect | Per existing programme record |

## 3. Requirement-to-design traceability

| ITRGA-REQ §4 item | Plan section |
|---|---|
| 1 Purpose/bounded question | Part A |
| 2 Account/entitlement gate | Part B |
| 3 Credential architecture (incl. mandatory vault revisit) | Part C |
| 4 Network authorization boundary | Part D |
| 5 Contract-test scope | Part E |
| 6 Data/provenance boundary | Part F |
| 7 Audit/accountability | Part G |
| 8 SAL/security design | Part H |
| 9 State-machine/database implications (P1 guards intact) | Part I |
| 10 Test/evidence matrix (Level I/II/III + negatives + abort) | Part J |
| 11 Rollback/revocation/incident | Part K |
| 12 Acceptance criteria + non-goals | Part L.1/L.2 |

§5 submission items: document ID/version (header), change summary (§1),
labeled assumptions (§2), traceability (§3), requested future authorities
(plan §L.3), preparation confirmations (§4 below and plan §L.4).

## 4. Preparation confirmations

While producing the plan the DA performed:

- no account/credential creation, use, request, storage, or exposure;
- no `AXIOM_TD_API_KEY` or provider-secret environment read;
- no DNS, socket, HTTP, REST, WebSocket, streaming, or provider-network
  activity of any kind;
- no provider endpoint call, payload use, or persistence;
- no `live:provider:twelvedata` activation, status promotion, guard
  modification, or transition-writer creation;
- no P2 implementation or provider-reaching test;
- no Paper/Live, broker, execution, AI, frontend, production, or
  **Git/GitHub** operation.

The workspace source tree is byte-identical to the BE-3 P1 approved state;
this submission adds only the two plan documents.

## 5. Requested future authorities (summary; detail in plan §L.3)

Secret-resolver + allowlisted transport modules; admin contract-test
permission + authenticated API endpoint; entitlement-recording migration
(contingent on Operator entitlement evidence); Operator-environment
contract-test run. **Nothing else — expressly not any status promotion,
transition migration, or history append.**

**End of Plan Report**
