# ITRGA DETERMINATION — UI-006-P01

**Explorer Frame · Existing Route Posture · Data-Source Inventory · Guardrails (Read-Only)**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P01** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P01.md` |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P01), `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering phase | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 49f/216t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-006-P01` · Phase `**UI-006-P01**` (443 lines) — OF the unit |
| Operator transcript | Same session; greps `DELIVERY_REPORT_UI-006-P01.md` + `BUILD_ORDER_UI-006-P01.md` (1868 lines) — OF the unit |
| Predecessor | `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (Approved-w-Obs + R-1…R-8) |

**Pack confirmed OF UI-006-P01.** No stale / wrong-phase / concatenated pack.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | Isolated run → **5 passed (5)** (L110–117): explorer_mounts_inside_single_ui001_shell / explorer_uses_existing_route_and_registry_only / explorer_maps_every_artifact_family_to_existing_sources / explorer_contains_no_mutation_actuation_or_gate_path / explorer_preserves_research_only_verbatim_and_doc16_branding | ✅ PASS |
| E-2 | 🔴 R-2/R-4 read-only proof | `UI006_P01_NO_MUTATION_CONTROL_SOURCE_GREP_CLEAN` (L175); browser "ORGANIZATION CHANGES: Deferred"; named test #4 | ✅ PASS |
| E-3 | 🔴 R-6 no-recompute + external-AI grep | `UI006_P01_R6_NO_RECOMPUTE_GREP_CLEAN` (L189, incl. AI pattern) | ✅ PASS |
| E-4 | 🔴 Whole-surface no-actuation grep (M-4 expanded) | `UI006_P01_NO_ACTUATION_GREP_CLEAN` (L197; script throws on any hit) | ✅ PASS |
| E-5 | Data-source inventory — every family → existing read seam | `ResearchManagementPage.tsx` maps advisory/intelligence/scenario/portfolio/journal/execution-research/collections/tags to `fetchAdvisorySignals`/`fetchInstitutionalIntelligenceBundle`/`fetchScenarioReports`/`fetchPortfolioResearchDashboard`/`fetchJournalEntries`/`fetchExecutionResearchBundle`/`fetchResearchManagementBundle`/`fetchResearchCollections`/`fetchResearchTags` (L264–278); named test #3 | ✅ PASS |
| E-6 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L304) | ✅ PASS |
| E-7 | No-drift: deps / endpoint / persistence | no new dep; no `/api/v1/artifacts`; no persistence key | ✅ PASS |
| E-8 | No registry / route change (R-1) | `/research-management` only; `$badRouteHits` for `/artifacts`/`/artifact-explorer` empty | ✅ PASS |
| E-9 | Regression ≥49f/216t, no test lost, GATED exit 0 | **`FRONTEND_VITEST_EXIT_CODE: 0`** (L715) → **Test Files 50 passed (50) / Tests 221 passed (221)** (L682–683; evidence file L322–323); no vitest failure | ✅ PASS |
| E-10 | Backend ≥414 | `pytest -q` → **414 passed** (L1356) | ✅ PASS |
| E-11 | Doc-16 brand B-1…B-7 | monospace ids; ARIA; institutional copy; named test #5 + browser | ✅ PASS |
| E-12 | Browser served-session | logged-out `/login`; `/research-management` explorer frame with source counts, GOVERNED DATA-SOURCE INVENTORY, EXISTING RESEARCH ORGANIZATION RECORDS (read-only), artifact preview; "ORGANIZATION CHANGES: Deferred" / "ARTIFACT TRUTH: Verbatim" / GATE CLOSED / RESEARCH-ONLY | ✅ PASS |
| E-13 | Networked CI | `LOCAL_CI_EXIT_CODE: 1` = TD-W6-CI-AUDIT env-flake — see §3 | ✅ (waived) |

---

## 3. npm audit posture — TD-W6-CI-AUDIT env-flake (operator-waived)

`LOCAL_CI_EXIT_CODE: 1` (L1369) arose solely from the offline npm-audit step hitting `read ECONNRESET` (L1364) — the audit endpoint never returned — **AFTER** all substantive gates ran green (full frontend **50f/221t** with `FRONTEND_VITEST_EXIT_CODE: 0`, backend **414**, tsc/build clean). This is the standing **TD-W6-CI-AUDIT** offline env-flake (network failure, no advisory data returned) — distinct from a real advisory report and from any test failure. **Waived by operator.** (Note: because the audit did not reach the registry this turn, no postcss advisory was reported here; TD-UI-POSTCSS-HIGH remains OPEN regardless.)

---

## 4. Constitutional line — read-only P01 held

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Mutation (collection/tag/membership create/update/delete) | NONE — read-only; `NO_MUTATION_CONTROL_SOURCE_GREP_CLEAN`; mutation deferred to P04/P05 (R-2/R-4) |
| Actuation (order/broker/account/live/execute/Gate) | NONE (M-4 expanded grep clean) |
| Recompute / inference / external AI / analytics engine | NONE (grep clean) |
| Verbatim artifact truth | HELD — "ARTIFACT TRUTH: Verbatim"; stored statuses/verdicts/confidence/uncertainty/limitations/ids/hashes not altered |
| New table / migration / dependency / registry / route / persistence | NONE (R-1/R-3 held; head unchanged) |

The mutation-deferral guardrail is established BEFORE any read-detail or mutation work — exactly the P01 intent for the first mutation-bearing workstream.

---

## 5. Observations (non-blocking)

- **OBS-P01-1 (TD-W6-CI-AUDIT):** offline npm-audit CI env-flake (`read ECONNRESET`) after substantive gates green — waived. Prefer a networked CI run at subsequent phases so the audit gate is meaningful (and note that a networked run will surface TD-UI-POSTCSS-HIGH, handled under its standing disposition).
- **OBS-P01-2 (informational):** TD-UI-POSTCSS-HIGH remains OPEN; per OBS-DP-1 (design-plan review) a dependency-remediation Build Order should be scheduled at/before UI-006-P06.

---

## 6. Carried standing residuals

- TD-UI-POSTCSS-HIGH (Path-B accepted pre-cert; remediation Build Order due at/before UI-006-P06)
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — occurred this turn; waived)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-006-P01 is APPROVED WITH OBSERVATIONS.** The read-only explorer frame, existing-route posture, data-source inventory, and mutation-deferral guardrail are established cleanly. This authorizes issuance of the next Build Order (**UI-006-P02 — Unified Artifact Catalog & Metadata Detail, read-only**) upon operator "authorized". P02 remains **read-only (R-2)**; mutation is still held to P04 (collections) / P05 (tags) under the persistence-capture + no-underlying-artifact-mutation + forbidden-field-rejection discipline.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 50f/221t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
