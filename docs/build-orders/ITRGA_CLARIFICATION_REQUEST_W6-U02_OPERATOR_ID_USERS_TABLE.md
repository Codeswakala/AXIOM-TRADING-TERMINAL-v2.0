# ITRGA CLARIFICATION REQUEST — W6-U02 `operator_id` FK Target (`users` vs `operators`)

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Reviewing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-07-17 |
| Related Build Order | `docs/build-orders/BUILD_ORDER_W6-U02.md` |
| Related final verdict | `docs/build-orders/ITRGA_VERDICT_W6-U01_FINAL.md` |
| Unit | W6-U02 — Simulated Execution Runs & Fill Events |
| Platform of record | v0.47.0 |
| Current Alembic head | `20260717_0027` |
| DA implementation status | **Paused — clarification required before construction** |
| Governance Gate | **CLOSED** |

---

## 1. Purpose of this request

DA requests ITRGA clarification before implementing W6-U02 because the Build Order's R6-2 identity/FK requirement references an existing `users` table, but the current AXIOM schema uses `operators` as the canonical authenticated operator identity table.

DA has not started W6-U02 construction.

---

## 2. Build Order requirement requiring clarification

W6-U02 applies R6-2:

```text
R6-2 — operator_id is research-attribution only.
Where operator_id appears (`simulated_execution_runs`, `simulated_paper_ledger_entries`, etc.) it must be a FK to the existing users table for research attribution ONLY. It must never be, alias, or join to any broker/trading account. Each such table's first submission owes the no-orphan audit JOIN against users (`orphan_count 0`), in addition to the run/fill lineage joins.
```

W6-U02 field contract includes:

```text
simulated_execution_runs.operator_id
```

and the mandatory evidence requires:

```text
no-orphan JOIN of operator_id against users (R6-2) → orphan_count 0
```

---

## 3. Current AXIOM schema reality

There is no `users` table in the current AXIOM database model or Alembic history.

The canonical authenticated identity table is:

```text
backend/app/db/models/operator.py
__tablename__ = "operators"
```

The authentication dependency returns:

```text
app.db.models.operator.Operator
```

Existing authenticated APIs use the current operator from:

```text
app.auth.dependencies.CurrentOperatorDep
```

Existing Wave-5 collaboration artifacts also use operator/actor fields as research attribution and do not reference a `users` table.

---

## 4. Impact

As written, DA cannot satisfy the exact W6-U02 evidence requirement:

```sql
... JOIN users ...
```

because `users` does not exist.

Proceeding without clarification would create one of several unacceptable outcomes:

1. DA silently substitutes `operators` for `users`, changing the Build Order requirement without ITRGA approval.
2. DA creates a new `users` table or alias, widening the identity model and schema beyond the Build Order's two named migrations (`20260717_0028` and `20260717_0029`).
3. DA omits the R6-2 no-orphan identity join, leaving a named acceptance criterion unproven.

Because W6-U02 is the first Wave-6 persisted artifact unit, DA is pausing before implementation rather than guessing.

---

## 5. DA recommended resolution — Option A

DA recommends ITRGA authorize `operators` as the canonical identity table for R6-2 in this codebase.

Under Option A:

- `simulated_execution_runs.operator_id` is a research-attribution FK to `operators.id`.
- `operator_id` is never a broker/trading account id.
- Evidence uses a no-orphan join against `operators`, not `users`.
- No new `users` table is created.
- W6-U02 remains within its two authorized migrations:
  - `20260717_0028` — `simulated_execution_runs`
  - `20260717_0029` — `simulated_fill_events`

Proposed schema relationship:

```text
simulated_execution_runs.operator_id -> operators.id
```

Proposed evidence query:

```sql
SELECT COUNT(*) AS orphan_operator_count
FROM simulated_execution_runs ser
LEFT JOIN operators o
  ON o.id = ser.operator_id
WHERE o.id IS NULL;
```

Expected:

```text
orphan_operator_count = 0
```

This preserves the intent of R6-2: operator attribution only, never broker/trading account linkage.

---

## 6. Alternative resolution — Option B

If ITRGA intended a distinct `users` table, then W6-U02 must be amended to explicitly authorize one of:

1. a new `users` table and its migration; or
2. a database view/alias from `operators` to `users`.

DA does **not** recommend Option B because it broadens identity architecture and schema surface during the first Wave-6 persisted-artifact unit.

---

## 7. Requested ITRGA decision

Please confirm one of the following:

### Option A — recommended

Authorize interpreting R6-2's `users` reference as AXIOM's existing `operators` table, with `operator_id` as a research-attribution FK to `operators.id` and no-orphan evidence joined against `operators`.

### Option B

Authorize a new `users` table or alias/view and revise W6-U02 migrations/evidence accordingly.

---

## 8. DA posture pending clarification

Until ITRGA clarifies this identity-table reference, DA will not implement W6-U02.

DA does not self-authorize schema changes, does not reinterpret `users` silently, does not create simulated execution tables, does not open the Governance Gate, does not add broker connectivity, does not add execution/order/account paths, and does not begin W6-U02 feature work.

The Constitutional Governance Gate remains **CLOSED**.

---

**End of ITRGA_CLARIFICATION_REQUEST_W6-U02_OPERATOR_ID_USERS_TABLE.md**
