# ITRGA DETERMINATION — UI-006-P05

**Tags Organization Mutation (SECOND MUTATION PHASE)**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P05.md` |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §5, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-4/R-5/**R-7** + M-1…M-3), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering phase | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 53f/236t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF UI-006-P05 (delivery report 428 lines, transcript 1808 lines, references BUILD_ORDER_UI-006-P05). No stale/wrong-phase/concatenated pack.

---

## 2. Level-I evidence verification — mutation discipline (raw psql)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing (incl. 2 CRITICAL) | **5 passed (5)** (L99–100): tags_mutate_existing_research_tag_store_only / tags_write_labels_and_artifact_references_not_source_payloads / **tags_reject_order_account_execution_and_verdict_fields** / **tag_mutation_does_not_modify_underlying_artifact_values** / tag_mutation_accessibility_brand_and_operator_scope_hold | ✅ PASS |
| E-2 | 🔴 R-7 tag persistence-capture | `UI006_P05_TAG_ID: 04b37bd0-5087-4b68-9e55-1a59caeb5f1b`; `research_tags SELECT` **`(1 row)`** (L195–198) — tag_id / `artifact_type scenario_report` / `artifact_id 41e96c26-…` / tag label / operator_id = **joined_operator_id** (no-orphan) / audit_correlation_id; **query keyed on the SAME artifact reference the UI wrote** (L167–168); `tag_rows_after_create` = **1** (L203). Tag label + refs only, no source payload | ✅ PASS |
| E-3 | 🔴 M-1/M-2 no-underlying-artifact-mutation | Scenario `41e96c26-…` fingerprint **byte-identical before (L141) and after (L227)** the tag mutation; `UI006_P05_SOURCE_ARTIFACT_UNCHANGED_CONFIRMED` (L234); named test #4 | ✅ PASS |
| E-4 | 🔴 M-3 schema audit | `research_tags` (7 cols) + **`forbidden_tag_column_count: 0`** (L259/L7) | ✅ PASS |
| E-5 | 🔴 Forbidden-field-rejection | named test #3 passed | ✅ PASS |
| E-6 | 🔴 R-5 tag delete gating | Delete **create-only** — explicitly out of scope (report §6; `UI006_P05_TAG_DELETE_OUT_OF_SCOPE_CONFIRMED`) because no frontend tag-delete support introduced | ✅ PASS (correct) |
| E-7 | 🔴 R-6 no-recompute + external-AI grep | `UI006_P05_R6_NO_RECOMPUTE_RELATIONSHIP_INFERENCE_GREP_CLEAN` (L301) + `UI006_P05_EXTERNAL_AI_GREP_CLEAN` | ✅ PASS |
| E-8 | 🔴 Whole-surface no-actuation grep (M-4 expanded) | `UI006_P05_NO_ACTUATION_GREP_CLEAN` (L303; throws on any hit) | ✅ PASS |
| E-9 | No-drift: Alembic head / no migration | `alembic current` → **`20260717_0037 (head)`** (L306) | ✅ PASS |
| E-10 | No-drift: deps / endpoint / route | no new dep; no new endpoint (existing W7 `research_tags`); `/research-management` only (R-1) | ✅ PASS |
| E-11 | Regression ≥53f/236t, no test lost, GATED exit 0 | **`FRONTEND_VITEST_EXIT_CODE: 0`** (L1789) → **Test Files 54 passed (54) / Tests 241 passed (241)** (L1749–1750; evidence L358–359); no vitest failure | ✅ PASS |
| E-12 | Backend ≥414 | `pytest -q` → **414 passed** (L955) | ✅ PASS |
| E-13 | Doc-16 brand + browser | served tag-create organization-only, operator-scoped (no order/account/execution/verdict field); tag persists in TAGS panel; logged-out block | ✅ PASS |
| E-14 | Networked CI | `LOCAL_CI_EXIT_CODE: 1` = TD-W6-CI-AUDIT env-flake — see §3 | ✅ (waived) |

**The P04 lesson landed:** the served tag add and the raw psql query targeted the **same** artifact reference, so persistence was proven first-try (no corrective cycle).

---

## 3. npm audit posture — TD-W6-CI-AUDIT env-flake (operator-waived)

`LOCAL_CI_EXIT_CODE: 1` (L968) arose solely from the offline npm-audit step hitting `getaddrinfo ENOTFOUND registry.npmjs.org` (L964) — **AFTER** all substantive gates ran green (**54f/241t** with `FRONTEND_VITEST_EXIT_CODE: 0`, backend **414**). Standing env-flake; **waived by operator.** (No postcss report this turn; TD-UI-POSTCSS-HIGH remains OPEN.)

---

## 4. Constitutional line — organization-only mutation held

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Tag mutation | Organization-only — tag label + artifact reference (tag_id/artifact_type/artifact_id) only; persisted to existing `research_tags`; no source payload |
| Underlying-artifact / verdict mutation | NONE — scenario source fingerprint unchanged before/after (M-1/M-2) |
| Forbidden columns | NONE — `forbidden_tag_column_count: 0` (M-3) |
| Actuation / recompute / external AI | NONE (greps clean) |
| New table / migration / dependency / route | NONE (R-1/R-3; head unchanged) |
| Tag delete | Out of scope (create-only; R-5 — no unproven-API delete) |

Both mutation phases (P04 collections + memberships, P05 tags) are now proven organization-only at the database level.

---

## 5. Observations (non-blocking)

- **OBS-P05-1 (TD-W6-CI-AUDIT):** offline npm-audit CI env-flake — waived.
- **OBS-P05-2 (P06 gating — carry forward):** UI-006-P06 is the completion checkpoint. Per OBS-DP-1, the **TD-UI-POSTCSS-HIGH dependency-remediation decision is due at/before P06** — the DA must either present remediation or an explicit re-acceptance at the completion checkpoint (carrying it silently past a second workstream completion attracts a Corrective).

---

## 6. Carried standing residuals

- TD-UI-POSTCSS-HIGH (Path-B accepted pre-cert; **remediation/re-acceptance decision due at UI-006-P06**)
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — occurred this turn; waived)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-006-P05 is APPROVED WITH OBSERVATIONS.** Tag organization mutation is proven organization-only with complete raw psql persistence-capture (research_tags 1 row, refs only, operator no-orphan JOIN, keyed on the reference the UI wrote), M-1/M-2 source-unchanged, M-3 forbidden count 0, tag delete correctly out of scope, no new table/migration, full regression. This authorizes issuance of the final Build Order (**UI-006-P06 — Completion Checkpoint**) upon operator "authorized" — which will declare 🏛️ UI-006 COMPLETE on approval and must resolve the TD-UI-POSTCSS-HIGH decision.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 54f/241t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
