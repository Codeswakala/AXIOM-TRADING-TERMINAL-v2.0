# ITRGA DETERMINATION — UI-006-P04

**Collections & Memberships Organization Mutation (FIRST MUTATION PHASE)**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P04.md` |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §5/§10, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-4/R-5/**R-7** + M-1…M-3), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 52f/231t |
| **DETERMINATION** | ⛔ **CORRECTIVE ACTIONS REQUIRED** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF UI-006-P04 (delivery report 435 lines, transcript 1785 lines, predecessor `ITRGA_REVIEW_UI-006-P03.md`). No stale/wrong-phase/concatenated pack. **The failure below is an evidence-completeness failure, not a build-identity or substantive-constitutional defect.**

---

## 2. 🔴 THE BLOCKING FINDING — R-7 persistence-capture NOT satisfied (first mutation phase)

The persistence-capture control is the defining mandatory evidence of a mutation phase: an **INLINE raw psql save→SELECT ≥1 populated row on the CORRECT table**. On this delivery it is **absent for the collection create and DISPROVEN for the membership add**:

| Required (Build-Order §4(c)/(d), R-7) | Transcript reality | Verdict |
|---|---|---|
| Collection create → raw psql `SELECT ≥1 row` on `research_collections` (ids/name/description/operator_id/research_status) | **No standalone save→SELECT on `research_collections` is present.** The only reads of that table are the failed membership sub-query (`WITH target_collection AS (SELECT collection_id … WHERE name='$collectionName')`) and the `information_schema` column audit. No row-content proof of a persisted collection. | ⛔ MISSING |
| Membership add → raw psql `SELECT ≥1 row` on `research_collection_members` (artifact refs only) | **`SELECT` returned NO row** → `UI006_P04_MEMBER_ID:` blank → script threw **`UI006_P04_MEMBER_ROW_NOT_FOUND`** (L1274–1302); the follow-up `member_before_remove` count = **`row_count | 0`** (L1359–1363). | ⛔ **DISPROOF** |
| Membership remove → before row_count=1, after row_count=0 | Report §(L373) **claims** "before=1, after=0"; transcript shows before=**0** (no membership ever proven to exist). | ⛔ REPORT-vs-TRANSCRIPT CONTRADICTION |

**Constitutional rule applied:** "A membership/collection write owes committing script + raw psql `SELECT ≥1 row` on the CORRECT table. An API / in-process read-back NEVER substitutes. **A `(0 rows)` read-back is DISPROOF, not proof.**" The delivery report §"raw PostgreSQL persistence capture" claims `research_collection_members row ≥ 1 after add` and `remove before=1/after=0` — **the operator transcript disproves both.** Per R7, the transcript is credited over the report claims. The 5 passing named tests (in-process) and the served-UI screenshots (which show created collections) **do not substitute** for raw psql persistence proof — this is the exact recurring lesson (UI-003-P02).

This is a single unmet mandatory evidence item on the first mutation phase ⇒ **Corrective Actions Required.**

---

## 3. What IS clean (carries forward — no re-proof needed on resubmit)

| Item | Evidence | Verdict |
|---|---|---|
| 5 named tests displayed passing (in-process) | 5 passed (5) (L55–66) incl. forbidden-field-rejection (#3) + no-underlying-artifact-mutation (#4) | ✅ (but in-process ≠ persistence) |
| **M-1/M-2 no-underlying-artifact-mutation** | Scenario artifact `41e96c26…` before (L110) and after (L1351) the org action: **identical** `research_only` / `report_hash w7u08-…` / `not_assessed` / uncertainty / `["research_only"]` — source UNCHANGED | ✅ PASS |
| **M-3 schema audit** | `research_collections` (8 cols) + `research_collection_members` (7 cols) = 15 rows; **`forbidden_org_column_count: 0`** (L1338) — no order/account/execution/verdict columns | ✅ PASS |
| operator_id → operators.id JOIN structure | JOIN present (L1291–1292) — but returned 0 rows because no membership persisted | ⚠️ n/a (no row) |
| Empty-collection delete gating (R-5) | Report §6: **explicitly out of scope** for P04 (no proven client support) | ✅ Correct |
| No-drift / no new migration (M-3) | `alembic 20260717_0037`; no new dep/endpoint; registry `/research-management` only | ✅ PASS |
| Regression / gated | `FRONTEND_VITEST_EXIT_CODE: 0` → **53f/236t** (L1698–1699, evidence L349–350); backend **414** | ✅ PASS |
| Doc-16 brand + browser | served collection-create + membership-add UI is organization-only, operator-scoped, no order/account/execution/verdict field; "Removal detaches the reference row only; it does not alter the source artifact"; logged-out block | ✅ PASS |
| CI | `LOCAL_CI_EXIT_CODE: 1` = TD-W6-CI-AUDIT `getaddrinfo ENOTFOUND` env-flake after gates green — waivable (not the blocking issue) | ✅ (env-flake) |

The constitutional line held (no underlying-artifact mutation, no actuation, no new table, Gate CLOSED). The defect is purely that **the mutation's persistence is unproven by raw psql — and disproven for membership.**

---

## 4. Required corrective actions (resubmit as UI-006-P04 attempt-2)

1. **CA-P04-1 (collection create):** Provide an INLINE raw psql `SELECT ≥1 row` from `research_collections` for the collection created in the served session (matching the exact created name/id), showing collection_id / name / description / operator_id / research_status, plus `operator_id → operators.id` no-orphan JOIN and `alembic current = 20260717_0037`.
2. **CA-P04-2 (membership add):** Perform a membership add in the served session and provide an INLINE raw psql `SELECT ≥1 row` from `research_collection_members` proving the persisted reference (collection_id + artifact_type + artifact_id only, no source payload) + `operator_id → operators.id` no-orphan JOIN. **The SELECT must return ≥1 populated row on the correct id — fix the evidence script so `$collectionName`/`$memberId` bind to the row the UI actually wrote (the prior run keyed on a mismatched name and returned 0 rows).**
3. **CA-P04-3 (membership remove, if claimed):** If member-reference removal is claimed, show before (row_count=1) → after (row_count=0) raw psql — matching the actual persisted row. If removal is not exercised, remove the claim from the delivery report.
4. **CA-P04-4 (report/transcript reconciliation):** The delivery report's persistence-capture section must reflect the ACTUAL raw psql results (no "row ≥ 1 after add" / "before=1/after=0" claims that the transcript contradicts).

Re-supply with all §3 clean items re-shown (or referenced) + the corrected §4 raw psql. Expected to resolve to Approved / Approved-with-Observations once persistence is genuinely proven.

---

## 5. Determination

**UI-006-P04 is CORRECTIVE ACTIONS REQUIRED.** The first mutation phase does not carry the mandatory raw psql persistence-capture (collection-create SELECT absent; membership-add SELECT returned 0 rows = disproof; report claims contradicted by transcript). **UI-006-P05 is NOT authorized.** Baseline of record remains **v0.62.0 · head `20260717_0037` · backend 414 · frontend 52f/231t** (the P04 +5 tests are not adopted until a clean attempt-2 with proven persistence).

Carried residuals unchanged: TD-UI-POSTCSS-HIGH, TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
