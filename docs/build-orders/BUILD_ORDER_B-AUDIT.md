# AXIOM — BUILD ORDER BO-B-AUDIT
## Audit-Integrity Fix: Eliminate Silent Audit Loss Under Concurrency

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-AUDIT` |
| Programme | Backend hardening (surfaced by F-00's OBS-F00-1) |
| Authorizing authority | **Operator** (directive of 2026-08-21: proceed with the recommended fixes) |
| Predecessors | B-00 → B-07 + X-01 + F-00 (all APPROVED WITH OBSERVATIONS) |
| Governing documents | `05_SYSTEM_ARCHITECTURE.md` §27 (Audit & Governance Service) · `17_INSTITUTIONAL_SECURITY_STANDARD.md` §5.7 (accountability) · `11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

F-00's capture probe surfaced a **real reliability defect** under concurrent dev load:

```
audit append failed … no such savepoint   (×2)
```

Mechanism (verified in code): `AuditRepository.append()` wraps the audit insert in a `SAVEPOINT` (`session.begin_nested()`) so that audit failure cannot 500 the business endpoint. Under concurrency the savepoint is invalidated, `append()` catches the exception and returns `None`, and **the audit row is silently lost** — while the endpoint still returns 200.

The intent ("audit must never take down the endpoint") is correct and must be preserved. But **silent audit loss is a governance-integrity failure**: the audit trail is the platform's evidence backbone (arch §27; security standard §5.7 accountability). Losing audit rows — even occasionally — breaks the "every significant activity is traceable" guarantee.

**This order makes audit loss either impossible or reliably detectable/retriable, without reintroducing the 500-on-audit-failure defect.**

---

## 1. Objective

1. **Reproduce** the "no such savepoint" failure with a deterministic concurrency test.
2. **Determine the exact root cause** (savepoint lifecycle under the observed transaction state — e.g. savepoint released/rolled back before `begin_nested` exits, or a shared-session interleaving).
3. **Fix** so audit append is durable: the audit row either lands, or the loss is **retried / surfaced as an explicit, queryable failure record** — never silently dropped.
4. **Preserve** the binding invariant: audit failure must never 500 the business endpoint.

---

## 2. Scope

### B-AUDIT.1 — Reproduce
- Write a concurrency test that exercises `issue_ws_ticket` (and other `append()` callers) under interleaved async load and reproduces the "no such savepoint" condition deterministically.
- Capture the exact SQLAlchemy/SQLite sequence that invalidates the savepoint.

### B-AUDIT.2 — Root cause
- Identify precisely why `begin_nested()` fails: (a) savepoint already released; (b) outer transaction rolled back/committed between the authoritative `flush()` and the `append()`; (c) session/connection reuse across tasks; or (d) SQLite-specific savepoint semantics. State the root cause with evidence.

### B-AUDIT.3 — Fix (choose the minimal correct mechanism, state the choice)
Candidate mechanisms (DA selects with justification, not mandated):
- **(a)** Retry the append once on savepoint failure (fresh nested transaction);
- **(b)** Decouple audit from the business transaction — a fire-and-forget/queued audit writer with its own short-lived session, so audit rows are written outside the savepoint that business code can invalidate;
- **(c)** On unrecoverable append failure, **persist a durable failure marker** (e.g. a `audit_write_failures` counter/table or structured log + retry on next read) so the loss is *visible*, never silent.

**Binding constraint:** whatever the mechanism, the endpoint must not 500 on audit failure, AND the audit loss must no longer be silent. "Best-effort" is retained; "silently dropped" is not.

### B-AUDIT.4 — Verification
- A test proving audit rows are **not lost** under the concurrency scenario that previously reproduced the failure (or, if a row genuinely cannot be written, that a durable failure marker is produced).
- A regression test that audit failure still cannot 500 the endpoint.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** change to audit *content/schema* (no new required fields, no re-writing existing rows) beyond the minimal durability mechanism.
- **No** new runtime dependency.
- **No** weakening of the non-actuation, RBAC, rate-limit, or any other invariant.
- **No** frontend changes.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model). **Register rows for this unit MUST ship in the patch** (see §9 — this addresses the OBS-F00-3 register-drift defect directly).

---

## 4. Exact deliverables

1. A reproducing concurrency test (pre-fix) proving the failure is real.
2. A stated root cause with evidence.
3. The fix (mechanism stated + justified).
4. Durability proof: audit rows land (or a durable failure marker is produced) under the concurrency scenario.
5. Regression proof: audit failure cannot 500 the endpoint.
6. Delivery Report (§9) with relay-accurate transmission manifest **including this unit's register rows**.

---

## 5. Dependencies

- **Upstream:** B-00 (provenance protocol) · the existing `AuditRepository` + `AuthService.issue_ws_ticket`.
- **Downstream:** none blocking; this restores the audit backbone for all future units.

---

## 6. Allowed files / components

- `backend/app/repositories/audit_repository.py` (the append path).
- `backend/app/auth/service.py` (only if the ws-ticket audit call site changes).
- `backend/app/db/session.py` (only if a dedicated audit session/writer is introduced).
- `backend/tests/**` (new/churn concurrency + regression tests).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (this unit's rows — **must ship**, §9).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Audit failure must **never** 500 the business endpoint (regression-tested).
- Audit loss must **never** be silent (durability-tested).
- No secrets/credentials; no new external network surface.
- The audit trail must remain append-oriented and immutable (no delete/update of historical rows).

---

## 8. Acceptance criteria

- [ ] Concurrency test reproduces "no such savepoint" pre-fix (evidence).
- [ ] Root cause stated with evidence (the exact invalidation sequence).
- [ ] Fix applied; mechanism chosen and justified.
- [ ] Post-fix: audit rows not lost under the same concurrency scenario (or durable failure marker produced) — test-pinned.
- [ ] Audit failure still cannot 500 the endpoint — regression test-pinned.
- [ ] **Register rows for this unit are included in the patch** (OBS-F00-3 corrective — verified by patch content, not just described).
- [ ] Full backend suite green; new tests executed with output.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding (CA-TRANSMIT-1):** artifacts uploaded and confirmed against the review channel.

**Binding (register-in-patch, OBS-F00-3 corrective):** this unit's `TECHNICAL_DEBT_REGISTER.md` rows must be **in the patch itself** (the patch must modify the register file), not merely described in the report. This begins repairing the register drift; ITRGA will verify the register hunk applies.

| Item | Class | Form |
|------|-------|------|
| Patch artifact (incl. register rows) + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Reproducing-concurrency-test output (pre-fix) | Level II | run transcript |
| Post-fix durability + regression test output | Level II | run transcript |
| Full backend suite output | Level II | run transcript |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Reproducing test (pre-fix evidence)
4. Root cause (with the exact invalidation sequence)
5. Fix mechanism + justification
6. Durability + no-500 regression evidence
7. **Register rows in patch (OBS-F00-3 corrective — confirmed)**
8. Test evidence (executed)
9. Deviations register
10. Transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- The fix is localized to the audit append path; revert = revert patch.
- No schema migration unless the durable-failure-marker mechanism requires one (then it must be disclosed and justified).
- No data produced affects production (Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of BO-B-AUDIT, the **provenance/reconciliation action for OBS-F00-3** is addressed (register-in-patch is now the standard), then **F-01 (assistant input surface)** may be issued.

---

**End of Build Order BO-B-AUDIT**
