# ITRGA REQUEST — UI-007-P06 R-6 Audit-Window Evidence Correction

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority |
| Programme | Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Current unit | UI-007-P06 — Completion Checkpoint |
| Trigger | `ITRGA_REVIEW_UI-007-P06.md` CA-P06-1 |
| Request type | Narrow evidence-conformance authorization request |
| Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Evidence limitation discovered

The mandated raw PostgreSQL R-6 row is available and proven:

```text
id:          055e3295-b485-4e84-9771-04c2318bf0b0
category:    SECURITY
action:      plugin_contract_request.refused
actor:       w7-u05-evidence-operator
reason_code: PLUGIN_CONTRACT_IMPORT_REFUSED
created_at:  2026-07-18 22:59:07
```

The existing browser Audit Explorer currently calls the existing endpoint with a newest-first window of 50 rows:

```text
fetchAuditEvents({ limit: 50 })
```

The R-6 refusal row predates that currently loaded window. The Audit Explorer’s existing filter is browser-local/in-memory; it cannot filter a row which the client never received. This is why filtering by the required audit id or `PLUGIN_CONTRACT_IMPORT_REFUSED` produces no row.

No audit row may be created or mutated to make the refusal recent.

---

## 2. Why the current P06 correction cannot be completed honestly

The ITRGA correctly requires the served UI to render the same stored refusal row proven by psql. A screenshot of another newer row is not a substitute. The refusal is absent from the client-side window, so an in-memory filter does not make the required row discoverable.

The DA will not fabricate a screenshot, create an audit event, alter database chronology, or claim that the row is rendered when it is not loaded.

---

## 3. Requested narrow authorization

Authorize one of the following **read-only evidence-conformance remedies**, limited to the existing Audit Explorer data-loading seam:

### Preferred remedy — merge existing security audit read window

Permit the frontend to read, merge, de-duplicate, and newest-sort only these already-existing API responses:

```text
GET /api/v1/persistence/audit-events?limit=50
GET /api/v1/persistence/audit-events?category=SECURITY&limit=200
```

The existing Audit Explorer and its existing in-memory filter/detail viewer would then render all received rows unchanged. This makes the existing `SECURITY` refusal record discoverable for R-6 evidence.

### Constraints

The authorization must remain limited to:

- existing endpoint only;
- GET/read-only only;
- no new route, backend change, query parameter, schema, table, migration, dependency, persistence, saved filter, UI field, filter control, action, or audit write;
- no score, inference, reclassification, summary, or reason-code reinterpretation;
- no change to Gate, certification, production, execution, broker, account, or operations posture.

---

## 4. Alternatives rejected

| Alternative | Rejected reason |
|---|---|
| Create a new refusal audit row | Forbidden by R-6; manufactures evidence. |
| Change audit timestamps or seed data | Violates audit integrity and chronology. |
| Capture another audit row | Does not prove the required refusal rendering property. |
| Use browser DevTools/network override | Not ordinary served-UI evidence and not independently reproducible. |
| Increase only general limit to 200 | Not guaranteed to reach the older refusal row when the audit corpus exceeds 200; category-scoped existing read is deterministic. |
| Alter backend or add a dedicated lookup endpoint | Prohibited by P06 and unnecessary; existing read API supports category and limit. |

---

## 5. Required ITRGA disposition

The DA requests one of:

1. **Authorize the preferred read-only evidence-conformance remedy** under a narrow corrective Build Order/amendment; or
2. Provide another evidence method that proves the row is rendered by the ordinary served UI without changing product source; or
3. Confirm that P06 may close without the served refusal-row limb (not recommended by the present R-6 requirement).

Until ITRGA disposition, P06 remains Corrective Actions Required and the DA will not modify the Audit Explorer fetch window.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**
