# BUILD ORDER INTAKE — UI-007-P05

**Platform Health, System Readiness, Version & API Posture** — *(Read-Only)*

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P05.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-007-P04_FINAL.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 59 files / 266 tests |
| Intake status | Accepted under ITRGA Build Order; implementation confined to P05 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

P04 is approved with observations. P05 is authorized only as a read-only extension of the existing protected `/governance` workspace.

The defining constraint is accepted without qualification:

```text
Runtime liveness/readiness is operational evidence.
Runtime liveness/readiness is NOT production certification.
Production remains NOT CERTIFIED under Doc 11.
```

---

## 2. Requirements accepted

P05 will reuse only existing read seams:

```text
GET /health
GET /ready
GET /api/v1/metrics
GET /api/v1/persistence/stats
GET /api/v1/system/info
GET /api/v1/institutional-platform/route-inventory
GET /api/v1/institutional-platform/rbac/permissions
GET /api/v1/institutional-platform/api-catalogue
GET /api/v1/institutional-platform/plugin-contracts
```

Required presentation outcomes:

- health, readiness, metrics, persistence statistics, system/version, route/RBAC/API/plugin posture shown as returned;
- runtime evidence and **Production NOT CERTIFIED / Doc 11 HELD** displayed together without conflation;
- W7-U07 readiness dispositions and every named standing residual rendered honestly;
- no secret, PII, hostname, credential, token, or connection-string exposure;
- no operations or governance action surface;
- five named P05 tests and P05 evidence pack.

---

## 3. Alternatives evaluated

| Alternative | Decision | Reason |
|---|---|---|
| Add a consolidated health/certification backend endpoint | Rejected | Prohibited by G-7/R-2/R-4; certification is out-of-band Doc 11 governance. |
| Render arbitrary full JSON payloads | Rejected | Could expose unapproved operational data; conflicts with H-4. |
| Use whitelisted direct fields from existing redacted read responses | **Selected** | Preserves as-returned operational values while preventing secret/PII/hostname exposure. |
| Mark ready/healthy as a master production status | Rejected | Violates H-1/G-3; production certification must remain NOT CERTIFIED. |
| Add runtime refresh/restart/reset operations | Rejected | Explicitly prohibited; P05 is evidence, never an operations console. |

---

## 4. Implementation plan

1. Extend the TypeScript client with types/wrappers for existing metrics, persistence stats, route inventory, RBAC vocabulary, API catalogue, and plugin-contract read endpoints.
2. Add a read-only P05 operations-evidence bundle loader in the Governance page; no backend code, schema, route, registry, dependency, or persistence change.
3. Add panels for operational evidence, explicit runtime-versus-certification separation, readiness dispositions, residual honesty, and API/plugin posture.
4. Display safe, direct fields only from existing redacted responses; do not compute scores, readiness verdicts, certification results, or capability inferences.
5. Add exactly the five required named P05 tests.
6. Prepare a P05 operator evidence command pack using the accepted non-halting evidence pattern and no baseline-diff requirement.

---

## 5. Explicit non-authorizations

P05 does not authorize:

- a completion checkpoint;
- new backend endpoint/service/schema/table/migration/dependency/route/registry/persistence;
- certification endpoint or production-ready label;
- restart, redeploy, drain, flush, metric reset, cache clear, migration rerun, or health-check trigger;
- governance, audit, Gate, certification, validation, readiness, or residual mutation;
- external AI/LLM, recompute, inference, reclassification, or derived operational score;
- saved views/filters;
- order, broker, account, live-money, or production deployment capability;
- remediation of `TD-AXIOM-GIT-PROVENANCE` or `TD-UI005-COMPLETION-TIMEOUT`.

---

## 6. Risk assessment

| Risk | Severity | Planned mitigation |
|---|---|---|
| Runtime ready shown as production approval | Critical | Same-surface permanent NOT CERTIFIED / Doc 11 HELD boundary; dedicated named test. |
| Green-only residual presentation | High | Render all listed residuals, including TD-AXIOM-GIT-PROVENANCE, as stored. |
| Sensitive operational values exposed | Critical | Existing backend-redacted endpoints plus frontend safe-field rendering and secret-marker test. |
| P05 becomes an operations console | Critical | No operation controls; structural/source tests and grep proof. |
| P05 adds architectural drift | High | Existing read APIs only; no backend/schema/dependency/route/registry changes. |

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
