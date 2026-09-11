# BUILD ORDER W6-U01 — AMENDMENT 1

## Refusal-audit evidence: `audit_events.details` JSON (no migration) — Option A AUTHORIZED

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Amends:** `BUILD_ORDER_W6-U01.md` §5(c) evidence query only. All other requirements of W6-U01 stand unchanged.
**Trigger:** `uploads/ITRGA_CLARIFICATION_REQUEST_W6-U01_AUDIT_REASON_CODE.md` (DA paused before construction — correct posture).
**Date:** 2026-07-17
**Governance Gate:** CLOSED (unchanged).
**Motto:** *We don't guess. We prove.*

---

## 1. Finding — the DA is correct

The DA raised a genuine defect in the Build Order. I verified it against the evidence in my possession rather than accepting the assertion:

- A prior **Wave-5** operator pack ran, verbatim:
  ```
  psql ... -c "SELECT details->>'refusal_reason' AS refusal_reason, COUNT(*) AS refusal_count
               FROM audit_events WHERE resource_type='assistant_response'
               AND action='assistant.refused'
               GROUP BY details->>'refusal_reason' ORDER BY refusal_reason;"
  ```
- This confirms the **established, proven** AXIOM convention: refusal reason codes live in the **`audit_events.details` JSON field** (queried `details->>'...'`), and there is **no top-level `audit_events.reason_code` column.**

Therefore the §5(c) SQL as written in `BUILD_ORDER_W6-U01.md` **cannot succeed on the current schema** and would force a migration — which directly contradicts W6-U01's own **no-schema / no-migration** safety scope. **This is a defect in my Build Order, and I own it.** The fix is not to widen the unit; it is to align the evidence query to the existing schema.

---

## 2. Decision — Option A AUTHORIZED (no migration)

**Option A is authorized.** W6-U01 shall store and query refusal reason codes via the existing `audit_events.details` JSON field. **No migration. Alembic head remains `20260717_0027`.** Option B (adding a `reason_code` column) is **REJECTED** — it broadens a safety-foundation unit beyond its stated no-schema scope and is the worse constitutional posture for Wave 6's first unit.

This ruling is unambiguous (the DA's recommendation matches the verified established pattern), so it is issued directly without further operator arbitration.

---

## 3. Amended §5(c) — refusal AUDIT proof (replaces the top-level-column query)

Deliver, inline, this raw `psql` evidence:

```sql
SELECT
  details->>'reason_code' AS reason_code,
  COUNT(*)               AS refusal_count
FROM audit_events
WHERE details->>'reason_code' IN (
  'GATE_CLOSED_CONNECT_REFUSED',
  'GATE_CLOSED_EXECUTE_REFUSED'
)
GROUP BY details->>'reason_code'
ORDER BY reason_code;
```

Expected (each row `refusal_count ≥ 1`, produced by the refusal tests):

```
reason_code                  | refusal_count
-----------------------------+--------------
GATE_CLOSED_CONNECT_REFUSED  | >= 1
GATE_CLOSED_EXECUTE_REFUSED  | >= 1
```

A blank/errored result is a non-result (R7) — show the command **and** its output.

---

## 4. Binding conditions on the details contract (so the audit corpus stays consistent & greppable)

The DA's proposed `details` payload is accepted with these **binding** conditions:

1. **Reason codes stay SCREAMING_SNAKE `*_REFUSED`** (`GATE_CLOSED_CONNECT_REFUSED`, `GATE_CLOSED_EXECUTE_REFUSED`). ✔ as proposed.
2. **Corpus-join discriminators required.** Each refusal row must ALSO set the standard top-level audit discriminators used across the existing corpus — i.e. a stable `action` and `resource_type` (e.g. `action='broker.connect.refused'` / `action='broker.execute.refused'`, `resource_type='broker_integration'` — DA may choose the exact strings but they MUST be stable and stated in the delivery report). This keeps the row joinable to the immutable `audit_events` corpus the same way Wave-5 refusals were (`action='assistant.refused'`, `resource_type='assistant_response'`).
3. **Gate-state proof in payload.** `details` must include `"gate_state": "CLOSED"` and the DA's proposed `"simulation_only": true` + the `live_broker_connection_attempted:false` / `live_order_attempted:false` flags, so the audit row itself proves no live attempt occurred.
4. **Immutability preserved.** Rows are append-only into the existing immutable `audit_events` table; no update path.
5. **Evidence disclosure.** The delivery report §5(c) must state the exact `action` / `resource_type` / `details` keys used, so I can verify the query targets the CORRECT rows (not an unrelated audit row).

---

## 5. What is unchanged

Everything else in `BUILD_ORDER_W6-U01.md` stands: no new table, no UI, no dependency, no migration; the six named tests + standing broker suite green; containment grep (d); bright-line grep (e); no-dep diff (f); `alembic current = 20260717_0027` (g); Git-Bash CI exit 0 (h); Gate-closed proof (R6-4). Acceptance criteria in §6 unchanged, now reading §5(c) as amended here.

---

## 6. Note on posture

The DA paused, did not self-authorize a schema change, did not reinterpret the Build Order silently, and brought a verifiable conflict with a recommended resolution and an alternative. **This is exactly the posture this project demands** — "high grade project, no room for error." Proceed on Option A.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
