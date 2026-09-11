# ITRGA RULING — UI-007-P06 R-6 Audit-Window Evidence Correction

**In response to:** `ITRGA_REQUEST_UI-007-P06_R6_AUDIT_WINDOW_CORRECTION.md` (DA)

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Unit | UI-007-P06 — Completion Checkpoint |
| Trigger | CA-P06-1 (`ITRGA_REVIEW_UI-007-P06.md`) |
| **DISPOSITION** | ✅ **REMEDY 1 AUTHORIZED** (preferred remedy, as constrained below) |
| Determination status | UI-007-P06 remains **Corrective Actions Required** until the evidence lands |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Ruling

**The preferred remedy is AUTHORIZED.** The Audit Explorer may read, merge, de-duplicate and newest-sort the responses of:

```text
GET /api/v1/persistence/audit-events?limit=50
GET /api/v1/persistence/audit-events?category=SECURITY&limit=200
```

Options 2 and 3 are declined — see §4 and §5.

---

## 2. Independent verification (performed before ruling — R1)

I do not authorize on the strength of a request. I verified the technical claim against the governing corpus:

| Claim | Independent check | Result |
|---|---|---|
| `category` is an **existing** query parameter | `UI-007_ENGINEERING_DESIGN_PLAN.md` §2.1, accepted at design-plan review: `GET /api/v1/persistence/audit-events?category=<optional>&limit=<1..200>` | ✅ **Pre-existing contract** |
| `limit` supports up to 200 | Same line — `limit=<1..200>` | ✅ Within contract |
| Response shape unchanged | `response_model=list[AuditEventRead]`; source table `audit_events` | ✅ |
| Explorer currently loads a 50-row newest-first window | Transcript + browser: *"In-memory only: showing 50 of 50 audit rows"* | ✅ Confirmed |
| Refusal row falls outside that window | psql `created_at 2026-07-18 22:59:07`; explorer detail pane shows `2026-07-28` rows | ✅ Confirmed |
| In-memory filter cannot reach an unfetched row | Architecturally necessary — the client filters what it received | ✅ Sound |

**The diagnosis is correct and the remedy uses no new capability.** Supplying `category=SECURITY` to an endpoint that already documents `category` as an optional parameter is **use of the existing contract**, not an expansion of it. This is materially different from adding a parameter, a route, or a backend lookup — none of which are authorized.

I also note the DA is **not** asking to widen the window arbitrarily. Its own §4 rejects "increase only general limit to 200" as non-deterministic once the corpus exceeds 200 rows. That reasoning is correct: a category-scoped read is deterministic; a bigger blind window is a guess. **The DA rejected the guess and asked for the provable method.**

---

## 3. Constraints (binding — all carried from the request, adopted verbatim)

The authorization is limited to:

- **Existing endpoint only** — `GET /api/v1/persistence/audit-events`. No new route, endpoint, or backend change.
- **GET / read-only only.** No audit write, create, edit, delete, redact, replay, or mark-reviewed.
- **No new query parameter** — `category` and `limit` are pre-existing per §2.1.
- **No** new schema, table, migration, dependency, persistence, saved filter, UI field, filter control, or action.
- **No** score, inference, reclassification, summary, or reason-code reinterpretation. `*_REFUSED` renders **verbatim as stored**, with no inference that refusal implies an authorization path.
- **No** change to Gate, certification, production, execution, broker, account, or operations posture.
- **Merge/de-duplicate/sort only** — presentation-layer assembly of two existing read responses. De-duplication must be by audit `id`, and must not drop, collapse, or summarise distinct rows.
- **No audit event may be created** to make the refusal recent. Chronology is not to be altered. *(The DA already refused all of these — recorded with approval.)*

**Any deviation is scope expansion (R16) and will be treated as a finding.**

---

## 4. Why option 2 (an alternative evidence method) is declined

There isn't a better one. I examined the alternatives:

- **A wider blind window** — non-deterministic, as the DA correctly argued.
- **DevTools/network override** — not ordinary served-UI evidence; not independently reproducible. The DA rejected this itself.
- **Accepting the P03 screenshot as carry-over** — P03 proved the property *then*. R-6 mandates re-proof at **P06** precisely because the completion checkpoint tests the surface as it stands at the end. A ten-day-old proof of a different build does not discharge a completion gate.
- **A backend lookup endpoint** — prohibited by G-7 and unnecessary.

The authorized remedy is the *least invasive* method that actually proves the property.

---

## 5. Why option 3 (close P06 without the served-refusal limb) is declined

The DA itself marked this "not recommended," and I agree — but I want the reason on the record, because it is the point of the whole workstream.

UI-007's thesis is that **governance is visible without becoming governable**. The single most important thing that must be *visible* is a constitutional **refusal** — the system declining an action and recording why. R-6 does not exist to prove the audit explorer renders rows; it exists to prove that a `*_REFUSED` code reaches the operator **as a stored refusal**, unreinterpreted.

Waiving that limb would mean declaring a governance workspace complete without ever showing that its refusal trail is visible. That is precisely the gap the control was written to prevent. **Not waivable.**

---

## 6. A finding this request has surfaced (recorded, non-blocking)

**OBS-P06-2 (new, MEDIUM, carried forward):** The audit explorer's fixed 50-row newest-first window means **older audit events — including constitutional refusals — become progressively unreachable from the UI** as the corpus grows. Today that is an evidence inconvenience. In an operating institutional terminal it is a **governance-visibility limitation**: the refusal record most worth inspecting is often not the most recent one.

The authorized merge mitigates this for `SECURITY`, but does not solve it generally. **To close:** a future authorized enhancement giving the explorer deterministic reach to older audit events (server-side filtering, pagination, or date-range selection) — each requiring its own Build Order. **Do not attempt in P06.** Disclose it on the governance surface as a tracked residual if the DA wishes; it should be listed in the P06 residual table.

This is the second time the completion checkpoint has produced a genuine institutional finding rather than a paperwork one. That is what a proof unit is for.

---

## 7. Required evidence to close CA-P06-1

1. Implement the authorized merge (existing endpoint, both reads, de-dup by `id`, newest-sort).
2. **Served-UI capture:** the Audit Explorer detail pane rendering audit id **`055e3295-b485-4e84-9771-04c2318bf0b0`** — `SECURITY` / `plugin_contract_request.refused` / actor `w7-u05-evidence-operator` / **`PLUGIN_CONTRACT_IMPORT_REFUSED`** / `2026-07-18 22:59:07` — **matching the psql output field-for-field**. Save as `UI-007-P06_02_R6_AUDIT_REFUSAL_MATCH.png`.
3. **Re-run the boundary greps** after the source change (governance-control · no-actuation · no-recompute · external-AI · route-declarations) — a source edit invalidates the prior clean greps (R12).
4. **Re-run the frontend suite** — confirm **≥61f/276t, no test lost**, gated `FRONTEND_VITEST_EXIT_CODE: 0`. Backend/alembic/CI need **not** be re-run; this is a frontend-only presentation change.
5. Confirm **no new dependency, route, registry change, endpoint, or persistence** (`alembic current 20260717_0037` unchanged).

Items 3 and 4 are required because the remedy touches product source. Everything else from the P06 pack stands proven.

---

## 8. Disposition

**Remedy 1 authorized under the §3 constraints. UI-007-P06 remains Corrective Actions Required until the §7 evidence is supplied.**

The DA identified a real evidence limitation, diagnosed it correctly, refused every shortcut available to it — fabricating a screenshot, creating an audit row, altering chronology, substituting a different row — and asked for authorization rather than proceeding. Under this project's constitution the DA may not self-authorize, and it did not. That is the separation of authorities working exactly as `03_AXIOM_SPEC` intends.

I am authorizing the narrowest remedy that proves the property, and recording the underlying limitation as a finding that outlives this phase.

On receipt of the §7 evidence, ITRGA expects to apply the eight-item constitutional validation and declare **🏛️ UI-007 — GOVERNANCE & EVIDENCE WORKSPACE COMPLETE**, advancing the baseline to **v0.62.0 · head `20260717_0037` · backend 414 · frontend 61f/276t**.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

*The refusal record is the one thing a governance workspace must never fail to show. Widen the window — honestly, through the door that already exists.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
