# ITRGA DETERMINATION — UI-006-P04 (attempt-3) — CORRECTIVE CLOSED

**Collections & Memberships Organization Mutation — FIRST MUTATION PHASE**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P04 (attempt-3 — corrective closed)** |
| Corrective response | `operator results.md` (285 lines, attempt-3 membership capture) + 3 served screenshots |
| Predecessor determinations | `ITRGA_REVIEW_UI-006-P04.md` (Corrective) · `ITRGA_REVIEW_UI-006-P04_ATTEMPT2.md` (Corrective-partial, CA-P04-1 closed) |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §5, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-4/R-5/**R-7** + M-1…M-3), Doc 16 |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 52f/231t |
| **DETERMINATION** | ✅ **APPROVED — UI-006-P04 corrective CLOSED** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF the UI-006-P04 attempt-3 corrective (references `ITRGA_REVIEW_UI-006-P04_ATTEMPT2.md`; single consistent collection `UI006 P04 CA3 Collection 20260726182333`). No stale/wrong-phase/concatenated pack.

---

## 2. Corrective-action closure (raw psql, this attempt)

| CA | Requirement | attempt-3 raw psql evidence | Verdict |
|---|---|---|---|
| **CA-P04-1** | Collection-create raw psql ≥1 row + no-orphan JOIN | `research_collections` **`(1 row)`** — `collection_id 8464cefc-8ecb-432a-81f4-9ebf8551ad5f` / operator_id = joined_operator_id / `research_status research_only`; `collection_rows_ca3` = 1 (L85–100) | ✅ CLOSED (re-proven) |
| **CA-P04-2** | Membership-add raw psql ≥1 row (refs only) + no-orphan | `UI006_P04_CA3_MEMBER_ID: aec53d0a-b312-4d0a-a243-a5cc968bddef`; membership `SELECT` **`(1 row)`** — member_id / `collection_id 8464cefc-…` (**SAME collection UI wrote**) / `artifact_type scenario_report` / `artifact_id 41e96c26-…` / operator_id = **joined_operator_id** (no-orphan) / audit_correlation_id; `member_rows_after_add_ca3` = **1** (L165–175). References only, no source payload | ✅ **CLOSED** |
| **CA-P04-3** | Removal before=1 → after=0 | `member_before_remove_ca3` = **1** (L243), removal executed, source artifact re-checked unchanged after remove | ✅ CLOSED |
| **CA-P04-4** | Report/transcript reconciliation | attempt-3 transcript IS the source of truth; all sentinels populated (no blank member id, no `(0 rows)`) | ✅ CLOSED |

**The persistence-capture that failed twice is now genuinely proven** — the served membership add and the raw psql query targeted the **same** collection (`8464cefc-…`), and the `SELECT` returned a populated row with the operator no-orphan JOIN. A UI panel was not relied upon; raw psql carried the proof.

---

## 3. Mutation-boundary reconfirmed (M-1…M-3)

| Control | Evidence | Verdict |
|---|---|---|
| **M-1/M-2 no-underlying-artifact-mutation** | Scenario `41e96c26-…` fingerprint **byte-identical at all THREE checkpoints** — before add (L40), after add (L234), after remove (L260): `research_only\|w7u08-18d1ce40…\|{"verdict":"not_assessed"}\|{"method":"closeout_seed","sample_count":3}\|["research_only"]`; `SOURCE_ARTIFACT_UNCHANGED` confirmed after add AND after remove | ✅ HELD |
| **M-3 schema audit** | `research_collections` (8) + `research_collection_members` (7) = 15 org columns; **`forbidden_org_column_count_ca3` = 0** against an EXPANDED pattern incl. `verdict\|confidence\|validation\|economic\|source_artifact_content` | ✅ HELD (stricter) |
| No-drift / no new migration | `alembic current 20260717_0037` (L220) | ✅ HELD |

Organizing/tagging an artifact provably does **not** touch the underlying artifact or its stored verdict/confidence/validation/economic/lineage values. The constitutional mutation boundary is proven at the database level.

---

## 4. Clean items carried from attempt-1 (ITRGA-confirmed)

5 named tests displayed passing (incl. forbidden-field-rejection + no-underlying-artifact-mutation); gated frontend **53f/236t** with `FRONTEND_VITEST_EXIT_CODE: 0`; backend **414**; Doc-16 brand + served organization-only UI (no order/account/execution/verdict field; "Removal detaches the reference row only; it does not alter the source artifact"); empty-collection delete correctly out of scope; TD-W6-CI-AUDIT env-flake waived after substantive gates green.

---

## 5. Determination

**UI-006-P04 is APPROVED (corrective closed).** The FIRST mutation phase of the programme now carries complete raw psql persistence-capture (collection create + membership add + membership remove, all on the same collection with operator no-orphan JOIN), organization-only mutation-boundary proven at the DB level (M-1/M-2 source-unchanged across add+remove; M-3 forbidden-column count 0), no new table/migration, and full regression. The two prior corrective cycles were evidence-orchestration failures (query/UI collection-id mismatch), not substantive constitutional defects — the constitutional line held throughout.

**Baseline advances to: v0.62.0 · head `20260717_0037` · backend 414 · frontend 53f/236t** (the +5 P04 tests are now adopted, confirmed on the attempt-1 gated `FRONTEND_VITEST_EXIT_CODE: 0` run and this proven persistence).

This authorizes issuance of the next Build Order (**UI-006-P05 — Tags Organization Mutation**) upon operator "authorized" — carrying the identical mutation discipline (organization-only, persistence-capture control, no-underlying-artifact-mutation + forbidden-field-rejection named tests).

Carried residuals unchanged: TD-UI-POSTCSS-HIGH (remediation Build Order due at/before UI-006-P06), TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
