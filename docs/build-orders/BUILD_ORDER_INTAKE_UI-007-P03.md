# BUILD ORDER INTAKE — UI-007-P03

**Read-Only Audit Explorer & Refusal Reason-Code Viewer**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P03** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P03.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-007-P02.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 57 files / 256 tests · vite-8 toolchain |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P03 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-007-P02 with observations and issued `BUILD_ORDER_UI-007-P03` for a read-only audit explorer and refusal reason-code viewer.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-007-P02.md
docs/build-orders/BUILD_ORDER_UI-007-P03.md
```

---

## 2. Accepted implementation scope

DA accepts only the P03 read-only audit scope:

```text
read existing audit_events through existing GET /api/v1/persistence/audit-events
audit row list and detail
reason-code viewer for details.reason_code and *_REFUSED values
in-memory filter and sort
raw psql operator proof that served rows match stored rows verbatim
```

P03 enhances the existing `/governance` route. It adds no new route.

---

## 3. Explicit non-authorizations

UI-007-P03 does not authorize:

- evidence viewer;
- health/readiness/version API panels;
- completion checkpoint;
- audit record mutation;
- reason-code reinterpretation;
- governance mutation;
- Gate control;
- certification actuation;
- production approval;
- residual disposition action;
- backend/API endpoint, service, schema, table, or migration change;
- dependency change;
- saved-filter persistence;
- recompute/inference/reclassification;
- external AI/LLM;
- order/broker/account/live/real-money path;
- production certification.

---

## 4. Mandatory named tests accepted

```text
test_ui007_audit_explorer_renders_existing_audit_events_read_only
test_ui007_audit_reason_codes_and_refusals_render_verbatim_no_inference
test_ui007_audit_explorer_filter_sort_are_in_memory_no_persistence_or_mutation
test_ui007_audit_explorer_contains_no_governance_mutation_gate_or_certification_control
test_ui007_audit_explorer_accessibility_and_doc16_brand_hold
```

---

## 5. Raw psql evidence obligation accepted

P03 must include raw PostgreSQL read-only proof:

```sql
SELECT id, category, action, actor, resource_type, resource_id,
       details->>'reason_code' AS reason_code, created_at
FROM audit_events
...
```

The raw output must include at least one `*_REFUSED` reason-code row and the served UI must render the same id/category/action/reason-code verbatim. This is read-only verbatim proof, not a save→SELECT mutation capture.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
