# ITRGA DETERMINATION — UI-006-P04 (attempt-2 / Corrective Action Response)

**Collections & Memberships Organization Mutation — R-7 Persistence-Capture Correction**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P04 (attempt-2)** |
| Corrective response | `DELIVERY_REPORT_UI-006-P04_CA_RESPONSE.md` (166 lines) + `operator results.md` (290 lines) |
| Predecessor determination | `docs/ITRGA_REVIEW_UI-006-P04.md` — ⛔ Corrective Actions Required |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §5, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-4/R-5/**R-7** + M-1…M-3), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 52f/231t |
| **DETERMINATION** | ⛔ **CORRECTIVE ACTIONS REQUIRED (partial) — CA-P04-1 closed; CA-P04-2/CA-P04-3 unmet** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF the UI-006-P04 corrective response (references `ITRGA_REVIEW_UI-006-P04.md` and the original Build Order). No stale/wrong-phase/concatenated pack.

---

## 2. Corrective-action status (line-by-line against the four CAs)

| CA | Requirement | attempt-2 raw psql evidence | Verdict |
|---|---|---|---|
| **CA-P04-1** | Collection-create raw psql `SELECT ≥1 row` on `research_collections` + `operator_id → operators.id` no-orphan + alembic head | **`(1 row)`** (L88–91): `collection_id dbe1a74e-a158-4ffe-82f2-6b66b9619da4` / name `UI006 P04 CA Collection 20260726152002` / `operator_id 90264969-…` = **`joined_operator_id 90264969-…`** (JOIN matches, no orphan) / `research_status research_only`; `collection_rows` count=1; `alembic current 20260717_0037` (L204) | ✅ **CLOSED** |
| **CA-P04-2** | Membership-add raw psql `SELECT ≥1 row` on `research_collection_members` (refs only) + no-orphan | `UI006_P04_CA_MEMBER_ID:` **blank**; `research_collection_members SELECT` = **`(0 rows)`** (L147–151); `member_rows_after_add` = 0 | ⛔ **STILL FAILS (disproof)** |
| **CA-P04-3** | Membership remove before=1 → after=0 | `member_before_remove` = **0** (L212), `member_after_remove` = 0 (L223) — no membership ever existed to remove | ⛔ **UNMET** |
| **CA-P04-4** | Report/transcript reconciliation (no over-claim) | Report §6: "does not claim persistence has been proven until the fresh corrective transcript returns populated raw rows"; transcript treated as source of truth | ✅ **CLOSED** (honest posture) |

---

## 3. Root cause of the CA-P04-2 failure (evidence-orchestration mismatch, repeated)

The CA membership query keyed on the **newly-created CA collection `dbe1a74e-…`** (L128–143, `WHERE collection_id = '$collectionId'`), but the operator's served membership **add** (screenshot `152818`) targeted a **different, older** collection — "Target collection = UI006 P04 Evidence Collection 20260726144934" — and the resulting membership appears (screenshot `152832`) under collection **`262eef32-…`**. So **no membership was ever added to the queried collection `dbe1a74e-…`**, and the raw psql correctly returns 0 rows.

This is **not** a proven membership-persistence defect (a membership row for `262eef32-…` is visible in the read-only UI panel), but it is **also not R-7 satisfaction**: there is **no raw psql `SELECT` returning ≥1 row for ANY membership** in the transcript. **A served-UI panel NEVER substitutes for raw psql; `(0 rows)` is disproof.** This is the **second consecutive** attempt where the membership raw-psql proof missed because the evidence script and the served UI targeted different collections.

---

## 4. Clean items — confirmed / carried

| Item | Status |
|---|---|
| CA-P04-1 collection-create persistence | ✅ **PROVEN this attempt** (raw psql 1 row + operator JOIN) |
| M-1/M-2 no-underlying-artifact-mutation | ✅ Re-proven — scenario `41e96c26…` before/after identical `research_only`/`report_hash`/`not_assessed`/uncertainty/limitations (L247–250) |
| M-3 schema audit | ✅ `forbidden_org_column_count: 0` (L195); 15 org columns, none forbidden |
| No-drift / no new migration | ✅ `alembic 20260717_0037` (L204) |
| 5 named tests · 53f/236t · backend 414 · Doc-16 · env-flake waiver | ✅ Carried from attempt-1 (ITRGA-confirmed) |

The constitutional line remains held (no underlying-artifact mutation, no actuation, no new table, Gate CLOSED). The **only** open defect is membership-persistence raw-psql proof.

---

## 5. Required corrective actions (resubmit — attempt-3, membership only)

1. **CA-P04-2 (re-issued):** In ONE served session, create (or select) a single collection, capture its `collection_id`, then **add a membership to THAT SAME collection**, and run the membership raw psql `SELECT` keyed on that **same** `collection_id` — returning **≥1 populated row** from `research_collection_members` (collection_id + artifact_type + artifact_id only, no source payload) + `operator_id → operators.id` no-orphan JOIN. The script's `$collectionId` MUST be the collection the UI wrote to (the prior two attempts keyed on a different collection than the served add).
2. **CA-P04-3 (re-issued, if removal claimed):** on that same proven member row, show before (row_count=1) → after (row_count=0). If removal is not exercised, omit the claim.
3. Re-affirm (reference is sufficient) CA-P04-1 + M-1/M-2 + M-3 + no-drift + 53f/236t + backend 414 (already accepted).

This is narrow: **only the membership raw-psql capture (targeting the correct collection) remains.** Expected to resolve to Approved once the membership `SELECT` returns ≥1 row.

---

## 6. Determination

**UI-006-P04 remains CORRECTIVE ACTIONS REQUIRED (partial).** CA-P04-1 (collection-create persistence) is CLOSED; **CA-P04-2/CA-P04-3 (membership persistence) remain unmet** — raw psql returned 0 rows because the query and the served membership add targeted different collections (repeated evidence-orchestration mismatch). Per the persistence-capture control, a UI panel does not substitute and `(0 rows)` is disproof. **UI-006-P05 is NOT authorized.** Baseline of record remains **v0.62.0 · head `20260717_0037` · backend 414 · frontend 52f/231t.**

Carried residuals unchanged: TD-UI-POSTCSS-HIGH, TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
