# ITRGA SUBMISSION — W6-U02 Clarification Request

## `operator_id` Research-Attribution FK Target: `users` vs `operators`

| Field | Value |
|---|---|
| Submitting authority | AXIOM Development Authority (DA) |
| Reviewing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-07-17 |
| Unit | W6-U02 — Simulated Execution Runs & Fill Events |
| Related Build Order | `docs/build-orders/BUILD_ORDER_W6-U02.md` |
| Related final verdict | `docs/build-orders/ITRGA_VERDICT_W6-U01_FINAL.md` |
| Current platform of record | v0.47.0 |
| Current Alembic head | `20260717_0027` |
| DA implementation status | **Paused — clarification required before construction** |
| Governance Gate | **CLOSED** |

---

## 1. Reason for submission

DA requests ITRGA clarification before implementing W6-U02 because the Build Order applies R6-2 using the term **`users` table**, while the current AXIOM schema uses **`operators`** as the canonical authenticated operator identity table.

DA has not started W6-U02 construction.

No W6-U02 code, migration, table, API, service, UI, test, or implementation documentation has been created beyond the Build Order intake and this clarification request.

---

## 2. Build Order language requiring clarification

W6-U02 applies R6-2:

```text
R6-2 — operator_id is research-attribution only.
Where operator_id appears (`simulated_execution_runs`, `simulated_paper_ledger_entries`, etc.) it must be a FK to the existing users table for research attribution ONLY. It must never be, alias, or join to any broker/trading account. Each such table's first submission owes the no-orphan audit JOIN against users (`orphan_count 0`), in addition to the run/fill lineage joins.
```

W6-U02 also requires the new `simulated_execution_runs` table to include:

```text
operator_id
```

and mandatory evidence includes:

```text
no-orphan JOIN of operator_id against users (R6-2) → orphan_count 0
```

---

## 3. Current AXIOM schema fact pattern

AXIOM currently has no `users` table.

The canonical authenticated identity table is:

```text
operators
```

Defined at:

```text
backend/app/db/models/operator.py
```

with:

```python
__tablename__ = "operators"
```

The authentication dependency returns:

```text
app.db.models.operator.Operator
```

Existing authenticated APIs use:

```text
app.auth.dependencies.CurrentOperatorDep
```

Existing Wave-5 collaboration artifacts use operator/actor attribution but do not reference a `users` table.

---

## 4. Why DA is pausing

As written, DA cannot satisfy this exact W6-U02 evidence requirement:

```sql
... JOIN users ...
```

because `users` does not exist in the current schema.

Proceeding without clarification would create one of three unacceptable outcomes:

1. **Silent reinterpretation** — DA substitutes `operators` for `users` without ITRGA authorization.
2. **Unauthorized schema expansion** — DA creates a new `users` table or view/alias, widening identity architecture beyond the stated W6-U02 migrations.
3. **Incomplete evidence** — DA omits the R6-2 no-orphan identity join, leaving a named acceptance criterion unproven.

Because W6-U02 is the first persisted-artifact unit in the highest-risk wave, DA is pausing before implementation.

---

## 5. DA recommended resolution — Option A

DA recommends ITRGA authorize interpreting R6-2’s `users` reference as AXIOM’s existing `operators` table.

Under Option A:

- `simulated_execution_runs.operator_id` is a research-attribution FK to `operators.id`.
- `operator_id` remains an AXIOM operator identity only.
- `operator_id` is never a broker account, trading account, real account id, position id, balance, margin, or capital reference.
- No new `users` table is created.
- No identity alias/view is created.
- W6-U02 remains within the two authorized migrations:
  - `20260717_0028` — `simulated_execution_runs`
  - `20260717_0029` — `simulated_fill_events`

Proposed schema relationship:

```text
simulated_execution_runs.operator_id -> operators.id
```

Proposed no-orphan evidence query:

```sql
SELECT COUNT(*) AS orphan_operator_count
FROM simulated_execution_runs ser
LEFT JOIN operators o
  ON o.id = ser.operator_id
WHERE o.id IS NULL;
```

Expected result:

```text
orphan_operator_count = 0
```

This preserves the intent of R6-2: research attribution only, with no broker/trading account linkage.

---

## 6. Alternative resolution — Option B

If ITRGA intended a distinct `users` table, then W6-U02 should be amended to explicitly authorize one of:

1. a new `users` table and migration; or
2. a database view/alias mapping `operators` to `users`.

DA does **not** recommend Option B because it broadens identity architecture and schema surface during the first Wave-6 persisted-artifact unit.

Option B would also require revising the W6-U02 migration/evidence plan beyond the two named migrations in the Build Order.

---

## 7. Requested ITRGA decision

Please confirm one of the following:

### Option A — recommended

Authorize interpreting R6-2’s `users` reference as AXIOM’s existing `operators` table, with:

```text
simulated_execution_runs.operator_id -> operators.id
```

and no-orphan evidence joined against `operators`.

### Option B

Authorize a new `users` table or alias/view and revise W6-U02 migrations/evidence accordingly.

---

## 8. DA posture pending clarification

Until ITRGA clarifies this identity-table reference, DA will not implement W6-U02.

DA does not self-authorize schema changes, does not reinterpret `users` silently, does not create simulated execution tables, does not open the Governance Gate, does not add broker connectivity, does not add execution/order/account paths, and does not begin W6-U02 feature work.

The Constitutional Governance Gate remains **CLOSED**.

---

**End of ITRGA_SUBMISSION_W6-U02_OPERATOR_ID_USERS_TABLE_CLARIFICATION.md**
