# BUILD ORDER W6-U02 — AMENDMENT 1

## R6-2 identity FK target: `operators` (not `users`) — Option A AUTHORIZED

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Amends:** `BUILD_ORDER_W6-U02.md` — every reference to the "`users`" identity table in R6-2 and §5(d). All other requirements stand unchanged.
**Trigger:** `uploads/ITRGA_SUBMISSION_W6-U02_OPERATOR_ID_USERS_TABLE_CLARIFICATION.md` (DA paused before construction — correct posture).
**Date:** 2026-07-17
**Governance Gate:** CLOSED (unchanged). **Motto:** *We don't guess. We prove.*

---

## 1. Finding — the DA is correct

Verified against evidence in my possession (not accepted on assertion):
- A **W0-U06** delivery report records: *"Schema | `operators` — migration `20260710_0003`"* — the operators identity table has existed since Wave 0.
- The corpus consistently references `operators` / `bcrypt-hashed operators` / `operator_repository` / `CurrentOperatorDep` / "authenticated operator sessions." **No `users` table exists anywhere in AXIOM.**

My R6-2 wording ("FK to the existing **users** table") used a generic term. AXIOM's canonical authenticated-identity table is **`operators`**. This is a defect in my Build Order wording, and I own it. The **intent** of R6-2 is unchanged: `operator_id` is research-attribution to the existing authenticated operator identity, and must **never** be, alias, or join to any broker/trading account.

---

## 2. Decision — Option A AUTHORIZED

**Option A is authorized.** Read every "`users`" in R6-2 and W6-U02 §5(d) as **`operators`**:

- `simulated_execution_runs.operator_id` is a **research-attribution FK to `operators.id`** (and likewise `simulated_fill_events` via its `run_id` lineage; if any fill/ledger table carries `operator_id` directly, it too FKs `operators.id`).
- `operator_id` remains an AXIOM operator identity ONLY — never a broker account, trading account, real account id, position id, balance, margin, or capital reference.
- **No new `users` table. No identity alias/view. No extra migration.** W6-U02 stays within its two authorized migrations `20260717_0028` (runs) and `20260717_0029` (fills).

**Option B (create a `users` table or `operators→users` alias/view) is REJECTED** — it would widen identity architecture and schema surface during the first Wave-6 persisted-artifact unit, for no benefit.

This ruling is unambiguous (the DA's recommendation matches the verified schema fact), so it is issued directly without further operator arbitration.

---

## 3. Amended §5(d) evidence — no-orphan identity JOIN (replaces the `users` join)

Deliver, inline, the R6-2 no-orphan identity JOIN against **`operators`**:

```sql
SELECT COUNT(*) AS orphan_operator_count
FROM simulated_execution_runs ser
LEFT JOIN operators o ON o.id = ser.operator_id
WHERE o.id IS NULL;
```
Expected: `orphan_operator_count = 0`.

(All other §5(d) persistence-capture items are unchanged: committing script; raw `psql SELECT ≥1 row` from `simulated_execution_runs` and `simulated_fill_events` showing `SIMULATED`/disclaimer/`simulation_policy_version`/`fill_model_version`; and the **no-orphan audit JOIN against `audit_events` for EACH table** → `orphan_count 0`.)

---

## 4. Binding condition (consistency)

The **forbidden-field / no-broker-account** contract (R6-2 second sentence) is unchanged and still binding: the identity FK proves attribution to `operators` ONLY. The §2/§5(e) forbidden-column proof must still show `broker_account_id`, `account_id`, `real_account_balance`, `margin`, `capital`, `live_position_id`, `broker_endpoint`, `broker_credentials`, `order_payload`, `order_intent`, `execution_status_as_live` are **absent** — i.e., `operator_id → operators.id` is the ONLY identity linkage, and it is not any account/broker reference.

---

## 5. Unchanged

Everything else in `BUILD_ORDER_W6-U02.md` stands: tables + migrations `0028`/`0029`; deterministic fill model; read-only API + write-safe create; R6-3 (no-real-P&L/dimensionless-units), R6-4 (Gate-closed line), R6-6 (immutable versions), R6-8 (create-path bright-line grep); nine named tests + broker suite; determinism proof; forbidden-column absence; CI exit 0; no UI. Acceptance §6 unchanged, reading "`users`" as "`operators`" throughout.

---

## 6. Note on posture

Second consecutive clean pause on a genuine correctness issue in my Build Order wording (W6-U01 audit-column, now W6-U02 identity-table) — the DA did not silently reinterpret, did not create a schema alias, did not omit the evidence. Exactly the posture this project demands. **Proceed on Option A.**

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
