# ITRGA Closure Review — AXIOM V2 BE-1 Corrected Design Plan

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-003 |
| Submission | `AXIOM-V2-BE-1-DA-PLAN-001`, v2.0.0 |
| Prior reviews | `ITRGA-REV-V2-BE-1-001`, `ITRGA-REV-V2-BE-1-002` |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Prior-finding closure

The revised plan closes the prior design findings in substance:

- a single configuration source is selected for Research/Simulation mode;
- the mode database table and mutable mode activation state are removed;
- Paper/Live remain deferred;
- capability registry is read-only seeded with no `enabled` mutation field;
- audit/lineage reads are operator-scoped, with restricted admin `read_all` access;
- DB-level append-only trigger design is proposed;
- V2 paths use `require_utc()` and reject naive datetimes;
- SAL control, resource ownership, retention, sensitive-read, and cross-operator test matrices are added;
- inherited migration drift is explicitly identified.

These are material improvements and align the plan more closely with the V2 Charter and Document 17.

## 2. Remaining blocking findings

### Finding V2-BE1-PLAN-007 — Proposed DB immutability trigger is PostgreSQL-specific but BE-1 must support SQLite development/testing

| Field | Detail |
|---|---|
| Severity | High — implementation/migration feasibility |
| Observed condition | The proposed trigger uses PostgreSQL-specific `CREATE OR REPLACE FUNCTION`, PL/pgSQL, and `RAISE EXCEPTION`. The V1 platform uses SQLite for development/testing and PostgreSQL for production. |
| Impact | The stated migration/test plan cannot apply the proposed trigger unchanged to the development/test database. The plan’s migration tests cannot demonstrate the claimed invariant unless dialect behavior is deliberately designed. |
| Required correction | Define a dialect-aware immutability strategy: PostgreSQL trigger implementation; SQLite-compatible trigger implementation or an explicitly justified test fixture/engine strategy; equivalent application/repository protections; and identical update/delete refusal tests on every supported dialect. Specify migration upgrade/downgrade behavior for each dialect. |
| Closure criterion | The design proves append-only enforcement is testable and equivalent in the supported SQLite development/test and PostgreSQL production environments. |

### Finding V2-BE1-PLAN-008 — SAL-3/4 inherited encryption, backup, monitoring, and alerting controls are asserted without an evidence/ownership boundary

| Field | Detail |
|---|---|
| Severity | High — Security Standard compliance |
| Security-standard basis | Document 17 §4.4 SAL-3/SAL-4 requirements; §8.7 storage protection; §8.13 backup; §9.10 environment separation; §11 security monitoring. |
| Observed condition | The SAL matrix states that PostgreSQL encryption at rest, HTTPS, daily DB backup, and alerting are “inherited from V1 deployment/ops,” while BE-0 evidence establishes only a local SQLite development baseline and explicitly does not establish production readiness. No ownership, validation artifact, or deployment-security source is identified. |
| Impact | Required SAL protections cannot be treated as satisfied by assertion. In particular, local SQLite does not demonstrate encrypted-at-rest SAL-3/4 storage. |
| Required correction | Reclassify these controls as deployment prerequisites/assumptions pending evidence, identify their owner and validation artifact, and define BE-1 development/test compensating controls. The plan must state that a BE-1 implementation is not production/SAL certification evidence. Do not claim inherited encryption/backup/monitoring as verified without supplied evidence. |
| Closure criterion | The plan clearly separates BE-1 application obligations from deployment-owned controls and contains no unsupported security-control claim. |

### Finding V2-BE1-PLAN-009 — Retention and permission records still use ungoverned indefinite retention/mutation semantics

| Field | Detail |
|---|---|
| Severity | Medium — data lifecycle and access-control governance |
| Security-standard basis | Document 17 §8.11 retention; §6.8 ownership; §6.9 administrative access; §6.14 authorization audit. |
| Observed condition | D.10 uses “permanent” retention for capability and permission records despite the Standard’s prohibition on indefinite retention without an approved lifecycle. `v2_permission` is a database table described as “versioned” but has no seed/authoritative source, update/revocation/approval/audit rule, or BE-1 mutation boundary. |
| Required correction | Apply a retention lifecycle or an explicit governance-record preservation/archival policy to capability and permission records. Specify whether `v2_permission` is read-only seeded in BE-1; if so, name its source and prohibit runtime mutation. If future administrative mutation is intended, defer it and define its future SAL-4 approval/audit/revocation design rather than leaving an implicit mutable table. |
| Closure criterion | No BE-1 table has indefinite retention or mutable authorization state without an approved owner, lifecycle, and authority/control model. |

### Finding V2-BE1-PLAN-010 — Migration-drift containment is described but lacks a measurable comparison gate

| Field | Detail |
|---|---|
| Severity | Medium — schema integrity |
| Observed condition | The plan identifies the inherited V1 drift and promises BE-1 adds V2 tables only. It does not define the exact baseline artifact, generated migration/check diff comparison, or pass/fail rule needed to demonstrate that BE-1 adds no additional unapproved drift. |
| Required correction | Define the drift baseline artifact and acceptance gate: capture the V1 `alembic check` operations at the parent baseline; compare BE-1 operations after upgrade; require all additional operations to be explained by the BE-1 migration or treat them as blocking defects. Include PostgreSQL and SQLite treatment. |
| Closure criterion | BE-1 delivery can distinguish inherited V1 drift from new BE-1 drift with direct comparison evidence. |

## 3. Determination

**CORRECTION REQUIRED.** The current plan is close to authorization and substantially improves security posture. The four remaining items are bounded design corrections concerning cross-dialect immutability, deployment-control claims, retention/permission governance, and measurable migration-drift containment. No BE-1 implementation is authorized until they are resolved.
