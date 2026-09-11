# ITRGA DETERMINATION — UI-006-P02

**Unified Artifact Catalog & Metadata Detail (Read-Only)**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P02** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P02.md` |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P02), `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering phase | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 50f/221t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-006-P02` · Phase `**UI-006-P02**` (445 lines) — OF the unit |
| Operator transcript | Same session; greps `DELIVERY_REPORT_UI-006-P02.md` + `BUILD_ORDER_UI-006-P02.md` (1831 lines) — OF the unit |
| Predecessor | `ITRGA_REVIEW_UI-006-P01.md` (Approved-w-Obs) |

**Pack confirmed OF UI-006-P02.** No stale / wrong-phase / concatenated pack.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | Isolated run → **5 passed (5)** (L80–81): catalog_lists_existing_artifacts_across_families_read_only / metadata_detail_renders_stored_fields_verbatim_without_recompute / catalog_preserves_no_cherry_picking_scope_sample_and_limitations / catalog_contains_no_mutation_actuation_or_gate_path / catalog_accessibility_and_doc16_brand_markers_hold | ✅ PASS |
| E-2 | 🔴 R-2/R-4 read-only proof | `UI006_P02_NO_MUTATION_CONTROL_SOURCE_GREP_CLEAN` (L137); browser "ORGANIZATION CHANGES: Deferred"; named test #4 | ✅ PASS |
| E-3 | 🔴 R-6 verbatim + no-recompute grep | `UI006_P02_R6_NO_RECOMPUTE_GREP_CLEAN` (L151); metadata rendered as-stored ("limitations, ids, and hashes are not altered"); named test #2 | ✅ PASS |
| E-4 | 🔴 No-cherry-picking | scope/sample/uncertainty/limitations rendered per-family from stored reports (source L52–510); named test #3 | ✅ PASS |
| E-5 | 🔴 Whole-surface no-actuation grep (M-4 expanded) | `UI006_P02_NO_ACTUATION_GREP_CLEAN` (L211; throws on any hit) | ✅ PASS |
| E-6 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L867) | ✅ PASS |
| E-7 | No-drift: deps / endpoint / persistence | no new dep; no `/api/v1/artifacts`; no persistence key | ✅ PASS |
| E-8 | No registry / route change (R-1) | `/research-management` only; `$badRouteHits` for `/artifacts`/`/artifact-explorer` empty | ✅ PASS |
| E-9 | Regression ≥50f/221t, no test lost, GATED exit 0 | **`FRONTEND_VITEST_EXIT_CODE: 0`** (L1314) → **Test Files 51 passed (51) / Tests 226 passed (226)** (L1264–1265; evidence file L331–332); no vitest failure | ✅ PASS |
| E-10 | Backend ≥414 | `pytest -q` → **414 passed** (L833) | ✅ PASS |
| E-11 | Doc-16 brand B-1…B-7 | monospace ids/hashes/sample counts; ARIA; institutional copy; named test #5 + browser | ✅ PASS |
| E-12 | Browser served-session | logged-out `/login`; `/research-management` unified catalog (65 catalog artifacts) + metadata detail rendering verbatim stored fields (Artifact id/Status `emitted`/Stored verdict `economically_usable`/Stored confidence `50.0%`/Uncertainty `calibrated`/Report hash/Source ids/Lineage) with "Stored metadata is rendered verbatim from existing read responses"; full 9-family GOVERNED DATA-SOURCE INVENTORY; "ORGANIZATION CHANGES: Deferred" / "ARTIFACT TRUTH: Verbatim" / GATE CLOSED / RESEARCH-ONLY | ✅ PASS |
| E-13 | Networked CI | `LOCAL_CI_EXIT_CODE: 1` = TD-W6-CI-AUDIT env-flake — see §3 | ✅ (waived) |

---

## 3. npm audit posture — TD-W6-CI-AUDIT env-flake (operator-waived)

`LOCAL_CI_EXIT_CODE: 1` (L846) arose solely from the offline npm-audit step hitting `getaddrinfo ENOTFOUND registry.npmjs.org` (L842) — the audit endpoint never returned — **AFTER** all substantive gates ran green (full frontend **51f/226t** with `FRONTEND_VITEST_EXIT_CODE: 0`, backend **414**, tsc/build clean). This is the standing **TD-W6-CI-AUDIT** offline env-flake (network failure, no advisory data). **Waived by operator.** (No postcss report this turn because the audit did not reach the registry; TD-UI-POSTCSS-HIGH remains OPEN.)

---

## 4. Constitutional line — read-only P02 held

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Mutation (collection/tag/membership create/update/delete) | NONE — read-only; grep clean; mutation deferred to P04/P05 (R-2/R-4) |
| Actuation | NONE (M-4 expanded grep clean) |
| Recompute / inference / external AI / analytics engine | NONE (grep clean) |
| Verbatim metadata | HELD — catalog/detail render stored fields as-stored; "limitations, ids, and hashes are not altered" |
| No-cherry-picking | HELD — scope/sample/uncertainty/limitations visible |
| New table / migration / dependency / registry / route / persistence | NONE (R-1/R-3 held; head unchanged) |

---

## 5. Observations (non-blocking)

- **OBS-P02-1 (TD-W6-CI-AUDIT):** offline npm-audit CI env-flake (`getaddrinfo ENOTFOUND`) after substantive gates green — waived. A networked CI run at a subsequent phase remains preferable (will surface TD-UI-POSTCSS-HIGH under its standing disposition).
- **OBS-P02-2 (informational):** TD-UI-POSTCSS-HIGH remains OPEN; dependency-remediation Build Order due at/before UI-006-P06 (OBS-DP-1).

---

## 6. Carried standing residuals

- TD-UI-POSTCSS-HIGH (Path-B accepted pre-cert; remediation Build Order due at/before UI-006-P06)
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — occurred this turn; waived)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-006-P02 is APPROVED WITH OBSERVATIONS.** The unified catalog and verbatim metadata detail are read-only and constitutionally clean. This authorizes issuance of the next Build Order (**UI-006-P03 — Lineage, Relationships & Advanced Filtering, read-only**) upon operator "authorized". P03 remains **read-only (R-2)**; mutation is still held to P04 (collections) / P05 (tags) under the persistence-capture + no-underlying-artifact-mutation + forbidden-field-rejection discipline.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 51f/226t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
