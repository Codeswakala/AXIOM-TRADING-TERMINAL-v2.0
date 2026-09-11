# ITRGA CLARIFICATION REQUEST — W6-U01 Audit Reason-Code Evidence

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Reviewing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-07-17 |
| Related design review | `docs/build-orders/ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` |
| Related Build Order | `docs/build-orders/BUILD_ORDER_W6-U01.md` |
| Unit | W6-U01 — Execution Research Safety Foundation: Gate-Closed Simulation Envelope |
| Platform of record | v0.46.0 |
| Current Alembic head | `20260717_0027` |
| DA implementation status | **Paused — clarification required before construction** |
| Governance Gate | **CLOSED** |

---

## 1. Purpose of this request

DA requests ITRGA clarification before implementing W6-U01 because the Build Order contains a conflict between:

1. W6-U01's explicit **no schema / no migration** requirement; and
2. W6-U01's required PostgreSQL audit query, which references a top-level `audit_events.reason_code` column that does not currently exist in the AXIOM schema.

DA has not started W6-U01 construction.

---

## 2. Build Order requirements in tension

### 2.1 No schema / no migration requirement

The W6-U01 Build Order states:

```text
This unit adds NO new table (R6-1) and NO UI.
```

and:

```text
No schema, no migration — head stays 20260717_0027.
```

### 2.2 Required audit SQL references a non-existent column

The same Build Order requires this refusal audit proof:

```sql
SELECT reason_code, COUNT(*) FROM audit_events
WHERE reason_code IN ('GATE_CLOSED_CONNECT_REFUSED','GATE_CLOSED_EXECUTE_REFUSED')
GROUP BY reason_code ORDER BY reason_code;
```

However, the current `audit_events` model does not have a top-level `reason_code` column. It has the existing structured JSON field:

```text
audit_events.details
```

Existing AXIOM audit patterns store reason codes and refusal metadata in `details`, e.g. assistant refusal evidence uses `details->>'refusal_reason'`.

---

## 3. Impact

As written, the required SQL cannot succeed on the current schema without adding a migration.

Adding a migration would contradict W6-U01's explicit no-schema/no-migration requirement.

Proceeding without clarification would create one of two unacceptable outcomes:

1. DA preserves no-migration but cannot satisfy the Build Order's exact SQL; or
2. DA adds a schema migration but violates the Build Order's no-migration constraint.

Because this is Wave 6's first and highest-risk safety unit, DA is pausing before implementation rather than guessing.

---

## 4. DA recommended resolution — Option A

DA recommends ITRGA authorize use of the existing `audit_events.details` JSON field for W6-U01 reason-code evidence, with no schema migration.

### 4.1 Proposed audit details contract

W6-U01 refusal audit rows would include:

```json
{
  "reason_code": "GATE_CLOSED_CONNECT_REFUSED",
  "gate_state": "CLOSED",
  "simulation_only": true,
  "live_broker_connection_attempted": false
}
```

and:

```json
{
  "reason_code": "GATE_CLOSED_EXECUTE_REFUSED",
  "gate_state": "CLOSED",
  "simulation_only": true,
  "live_order_attempted": false
}
```

Reason codes remain SCREAMING_SNAKE and `*_REFUSED`, satisfying the Build Order's semantic requirement.

### 4.2 Proposed PostgreSQL evidence query

Replace the top-level-column query with this JSON-field query:

```sql
SELECT
  details->>'reason_code' AS reason_code,
  COUNT(*) AS refusal_count
FROM audit_events
WHERE details->>'reason_code' IN (
  'GATE_CLOSED_CONNECT_REFUSED',
  'GATE_CLOSED_EXECUTE_REFUSED'
)
GROUP BY details->>'reason_code'
ORDER BY reason_code;
```

Expected output:

```text
reason_code                  | refusal_count
-----------------------------+--------------
GATE_CLOSED_CONNECT_REFUSED  | >= 1
GATE_CLOSED_EXECUTE_REFUSED  | >= 1
```

### 4.3 Why Option A preserves the Build Order intent

Option A preserves all W6-U01 safety goals:

- no new table;
- no migration;
- Alembic head remains `20260717_0027`;
- raw `psql` evidence still proves refusal reason codes;
- refusal evidence still lives in immutable `audit_events`;
- Gate-closed refusal rows remain auditable;
- W6-U01 remains a safety-foundation proof unit only.

This aligns with established AXIOM audit practice from Wave 5, where refusal reason codes are stored and queried from `audit_events.details`.

---

## 5. Alternative resolution — Option B

If ITRGA requires a top-level `audit_events.reason_code` column, then ITRGA should explicitly amend W6-U01 to authorize a schema migration and revise the no-migration requirement.

That would require:

```text
backend/alembic/versions/<new_revision>_w6_u01_audit_reason_code.py
```

and W6-U01 evidence would need to advance Alembic head beyond `20260717_0027`.

DA does **not** recommend Option B because it broadens W6-U01 beyond the stated no-schema safety-foundation scope.

---

## 6. Requested ITRGA decision

Please confirm one of the following:

### Option A — no migration, JSON reason-code evidence

Authorize W6-U01 to store refusal reason codes in `audit_events.details->>'reason_code'` and use the JSON-field `GROUP BY` query shown above.

### Option B — migration authorized

Authorize a W6-U01 schema migration adding `audit_events.reason_code`, and explicitly revise the Build Order's no-schema/no-migration requirement.

---

## 7. DA posture pending clarification

Until ITRGA clarifies this conflict, DA will not implement W6-U01.

DA does not self-authorize a schema change, does not reinterpret the Build Order silently, does not open the Governance Gate, does not add broker connectivity, does not add execution/order/account paths, and does not begin any Wave-6 feature work.

The Constitutional Governance Gate remains **CLOSED**.

---

**End of ITRGA_CLARIFICATION_REQUEST_W6-U01_AUDIT_REASON_CODE.md**
