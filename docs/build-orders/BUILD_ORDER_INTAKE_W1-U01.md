# Build Order Intake — W1-U01

| Item | Value |
|------|-------|
| Build Order | W1-U01 — Core Platform: Service Architecture & API Hardening Foundation |
| Date received | 2026-07-12 |
| Authority | ITRGA, following Wave 0 closure |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of:

- `docs/build-orders/ITRGA_WAVE0_CLOSURE.md`
- `docs/build-orders/BUILD_ORDER_W1-U01.md`

Wave 0 is recorded by ITRGA as **CLOSED** and W1-U01 is **ISSUED**. Implementation may proceed within the scope of the Build Order.

## 2. Objective

Mature the Wave-0 foundation into the first Wave-1 Core Platform layer by hardening service boundaries, endpoint authorization breadth, timezone/data correctness, persistence service layering, CI evidence, and register synchronization.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Application Services | Refactor route-level business/data access into service-layer orchestration where currently thinness is weak, especially persistence APIs; document bounded-context role. |
| B API authorization | Classify endpoints and protect operational endpoints. Public surface limited to liveness/readiness/login plus explicitly scoped minimal discovery/refresh-token credential paths. `/ws/status` to require short-lived ticket auth. |
| C Time/data correctness | Normalize API/storage-facing datetimes to timezone-aware UTC and prove via tests. |
| D Persistence service | Introduce a proper persistence application service and move route DB logic behind it. |
| E CI/register | Run available local gate; require Operator/GitHub evidence for true CI/PG if unavailable in DA sandbox; sync technical debt statuses accurately. |
| F Verification | Preserve Wave-0 behavior and add tests for auth breadth, timezone UTC, and persistence service parity. |

## 4. Constraints

- No execution, order, position, broker connection, ML/AI feature, chart feature expansion, or new market feature.
- Preserve single-uvicorn workflow and W0-U08 security hardening.
- No regression of login, ingestion, persistence, live feed, chart, WS ticket auth, or provenance labelling.
- Claims must be supported by evidence.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Locking down formerly public endpoints may break frontend chart/history calls | High | Update frontend API client to send Bearer token for protected data calls; add regression tests. |
| `/ws/status` auth may break dashboard status socket | Medium | Use same short-lived ticket mechanism as live WS. |
| Timezone behavior differs between SQLite and PostgreSQL | Medium | Normalize at service/schema boundaries; request operator/PG evidence where needed. |
| CI run cannot be produced in DA sandbox | Medium | Run local available gates and document missing GitHub/PG evidence honestly. |

## 6. Implementation authorization posture

This Build Order is accepted. The DA will implement minimal-diff hardening and submit a Delivery Report with evidence. DA does not self-approve W1-U01.

---

**End of intake**
