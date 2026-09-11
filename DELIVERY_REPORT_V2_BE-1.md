# DELIVERY REPORT — AXIOM V2 BE-1: Core Domain, Audit, and Mode Framework

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-1-DR-004 |
| Build Order | BO-V2-BE-1-001 |
| Date | 2026-08-24 |
| Author | Replacement Development Authority (DA) |
| Status | **SUBMITTED FOR ITRGA FINAL DETERMINATION** |
| Authorization for this correction cycle | ITRGA-ACC-V2-BE-1-INTAKE-001 (accepted intake AXIOM-V2-BE-1-DA-INTAKE-001) |
| Parent Commit | `9ab91e76b3ac5f6a42c3066f022700489c214a29` |
| V1 Alembic Head | `20260717_0037` |
| BE-1 Alembic Head | `20260823_0038` (byte-identical to accepted intake manifest) |
| Prior Versions | DR-001…DR-003 — historical claims, superseded; nothing inherited without direct verification |

---

## 1. Identity and Executive Summary

This report is produced by the replacement DA after the ITRGA-accepted intake
reconciliation and completes corrective actions **CA-01 through CA-07** for
defects **DEF-BE1-01 through DEF-BE1-07**.

DA verification result: **630 tests executed, 630 passed, 0 failed** —
552 V1 regression + 78 distinct V2 tests under a single non-duplicating
collection. All BE-1 security acceptance paths are now exercised by genuine
async database/API integration tests. This is a submission for review, not an
approval.

## 2. Scope

### Delivered in this correction cycle

| CA | Defect | Delivered |
|---|---|---|
| CA-01 | DEF-BE1-01 | Two-operator DB/API isolation tests (list, artifact lookup, audit list); admin `read_all` privilege + denial tests. Source fix was already present at intake and is retained unchanged. |
| CA-02 | DEF-BE1-02 | `tests/test_v2_integration.py` fully rewritten: 18 genuine integration tests using real `Operator` rows, real login, `httpx.AsyncClient(ASGITransport)` against the live app/DB, and a real Alembic migration-lifecycle test on a dedicated SQLite database. Static checks relocated to unit files; non-duplicated accounting adopted. |
| CA-03 | DEF-BE1-03 | Write-time policy per ITRGA R-9.4 determination: `secret`/unknown classifications refused (`AuditWriteRejectedError`); value-borne secrets redacted before storage; key-borne (unredactable) secrets refused; refusals never echo the value. Read-path clearance filtering proven at API level (operator sees `_redacted`, admin sees details). |
| CA-04 | DEF-BE1-04 | Internal denial log enriched with route, method, correlation ID, and decision; public response remains generic `Permission denied`. API test proves no permission vocabulary in denial bodies across 7 routes. |
| CA-05 | DEF-BE1-05 | V2-path-scoped internal-error containment middleware added: unhandled exceptions on `/v2` / `/api/v1/v2` paths return the safe structured internal-error contract (`internal.error`, generic detail, correlation, timestamp). Leak-free behaviour proven by API test (no exception text, class name, or traceback in response). V1 error behaviour untouched. |
| CA-06 | DEF-BE1-06 | `V2CapabilityDetailResponse` Pydantic envelope added and bound via `response_model`; all V2 endpoints assert mode/correlation/timestamp presence by test. |
| CA-07 | DEF-BE1-07 | Migration, V2 ORM models, metadata imports, and `alembic/env.py` are byte-identical to the accepted intake manifest — the R-9.3 PostgreSQL re-gate is therefore not triggered, and existing Operator PostgreSQL 18.4 rerun evidence remains valid. SQLite lifecycle re-verified with literal evidence: upgrade, tables, triggers, seeds (23 capabilities / 12 permissions), UPDATE/DELETE refusal on both immutable tables, drift gate (zero V2 operations), downgrade removal, re-upgrade. |

Additional bounded work: `ruff --fix` mechanical lint cleanup limited to V2
files and V2 tests (import sorting/unused imports/two line wraps); V2 scope now
lint-clean. Two pre-existing `app/main.py` findings are inherited V1 debt and
remain recorded.

### Explicitly not delivered / out of scope

Paper/Live modes; providers, brokers, exchanges, real market data; accounts,
balances, positions, orders, fills, execution, reconciliation; external AI;
frontend; production deployment or certification; Git/GitHub operations; any
new table, endpoint, or permission.

## 3. Implementation

### Files materially changed (9)

| File | Change |
|---|---|
| `backend/app/v2/errors/contract.py` | `AuditWriteRejectedError` (R-9.4) |
| `backend/app/v2/audit/contract.py` | `STORABLE_CLASSIFICATIONS` frozen set |
| `backend/app/v2/audit/repository.py` | Write-time classification/secret refusal with SECURITY logging |
| `backend/app/v2/rbac/dependencies.py` | Denial log: +route/method/correlation/decision |
| `backend/app/v2/models/capability.py` | `V2CapabilityDetailResponse` envelope |
| `backend/app/v2/api/capability.py` | Typed envelope + `response_model` on single-capability route |
| `backend/app/main.py` | V2-scoped internal-error containment middleware |
| `backend/tests/test_v2_integration.py` | Rewritten as genuine integration suite (18 tests) |
| `backend/tests/test_v2_audit.py` | +9 classification/clearance/storable unit tests (relocated + new) |

12 further files: lint-only mechanical changes (full list and hashes in the
delta transcript). Migration/models/metadata: **unchanged** (attested by hash).

Old-hash → new-hash manifest, unchanged-file attestation, and literal contents
of all materially changed files: `docs/evidence/V2_BE-1_REMEDIATION_SOURCE_DELTA.md`.

### Architecture / security impact

- No new persistence objects, endpoints, or permissions.
- Error-containment middleware is strictly V2-path-scoped; V1 semantics
  preserved (552 V1 tests pass unmodified).
- Audit write path is now fail-closed for unsupported classifications and
  unredactable secret material, per the ITRGA R-9.4 determination.

## 4. Verification

| Check | Command | Result |
|---|---|---|
| Full suite | `pytest tests/ -q --tb=short -p no:cacheprovider` | **630 passed, 0 failed** (193–197 s) |
| V2 suite (non-duplicating) | explicit 7-file list, `-q --tb=short` | **78 passed** |
| V2 lint | `ruff check app/v2/ tests/test_v2_*.py` | All checks passed |
| SQLite migration lifecycle | `alembic upgrade head` / `check` / `downgrade 20260717_0037` / re-upgrade on dedicated DB | exit 0 / inherited-V1-drift-only / exit 0 / exit 0 |
| Trigger refusal (direct SQL) | UPDATE/DELETE on `v2_audit_event`, `v2_lineage_record` | REFUSED — "immutable" both paths, both tables |
| Drift gate | `alembic check` output scan | **zero `v2_*` operations**; only documented inherited V1 drift |

Test accounting statement: baseline claim was 89 V2 tests (DR-003). Current
distinct count is **78** — 38 static pseudo-integration checks were replaced by
18 genuine integration tests and 8 clearance checks were relocated to the unit
file (plus 1 new test). Counts were produced by actual execution, not carried
forward. Full per-file breakdown and the literal executed-test-name capture are
in `docs/evidence/V2_BE-1_REMEDIATION_EVIDENCE.md`.

## 5. Known Limitations and Open Items

1. **PostgreSQL runtime evidence** remains Operator-environment work. Because
   migration/models/metadata are byte-identical to the manifest behind the
   successful Operator PostgreSQL 18.4 rerun, no re-gate is triggered under
   R-9.3. If ITRGA nevertheless requires a fresh PostgreSQL pass over the
   remediated tree, the R-9.3 procedure applies unchanged; app-level V2 tests
   can also be run against a PostgreSQL URL where the Operator provides one.
2. Two pre-existing PostgreSQL evidence gaps noted in PG-002 §4 (post-downgrade
   trigger/function absence query, PostgreSQL-native mutation-refusal output)
   remain Operator-run items on the existing command pack.
3. Inherited V1 debt unchanged and carried: Ruff lint/format baseline
   (incl. 2 `app/main.py` findings), V1 model/migration drift baseline,
   dev-baseline evidence ≠ production certification.
4. Dev/test evidence is SQLite; SAL deployment controls remain
   deployment-owned assumptions per the approved plan.

## 6. Handover

| Item | State |
|---|---|
| Workspace | `/home/user/axiom` — remediation complete, suite green |
| Evidence package | `docs/evidence/V2_BE-1_REMEDIATION_SOURCE_DELTA.md` (literal source + hashes), `docs/evidence/V2_BE-1_REMEDIATION_EVIDENCE.md` (literal command outputs, coverage map, closure table) |
| State documents | `V2_CURRENT_STATE.md` v6.0.0, V2 Risk Register, V2 Technical Debt Register updated this cycle |
| Git | No DA Git/GitHub operation performed; publication remains Operator post-approval custody work |
| Required next action | ITRGA final determination on BE-1 |
| BE-2 | Remains NOT AUTHORIZED |

**We don't guess. We prove.**

**End of Delivery Report DR-004**
