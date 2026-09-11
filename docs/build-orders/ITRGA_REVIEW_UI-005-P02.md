# ITRGA DETERMINATION — UI-005-P02

**Signal Investigation Lineage & Related Evidence**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P02** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P02.md` |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P02), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 44f/191t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report header | `# DELIVERY REPORT — UI-005-P02` · Phase `**UI-005-P02**` — OF the unit |
| Delivery report length | 404 lines — single-phase |
| Operator transcript | Same PowerShell session; opens by grepping `DELIVERY_REPORT_UI-005-P02.md` + `BUILD_ORDER_UI-005-P02.md` — OF the unit |
| Transcript length | 2059 lines |
| Predecessor referenced | `ITRGA_REVIEW_UI-005-P01.md` (Approved-w-Obs) |

**Pack confirmed OF UI-005-P02.** No stale / wrong-phase / concatenated pack.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | Isolated run → **5 passed (5)** (L117–124): renders_existing_signal_lineage_read_only / uses_stored_confidence_validation_and_economic_values_verbatim / links_related_reports_without_recompute / contains_no_signal_generation_or_actuation / accessibility_and_brand_markers_hold | ✅ PASS |
| E-2 | 🔴 R-6 no-recompute grep CLEAN | full spine grep → no output (L150) | ✅ PASS |
| E-3 | 🔴 External-AI grep CLEAN | `openai\|gpt\|external_llm\|llm_summary\|ai_summary` → no output (L151) | ✅ PASS |
| E-4 | 🔴 Verbatim lineage (as-stored) | Source: Signal id / Model / Model version / Experiment (`{signal.experiment_id}`) / Feature set / Input hash in `.mono`; browser shows lineage + `50.0% calibrated` (not raw score) + guardrails + `economically_usable`; state badges EMITTED/EXPIRED/WITHHELD/WARNING as-stored; named test #2 passed | ✅ PASS |
| E-5 | 🔴 Related-reports-without-recompute | Related links are plain `<a href="/intelligence">`/`/signals`/`/charts` — navigation/disclosure to existing viewers, no browser aggregate/derivation; named test #3 passed | ✅ PASS |
| E-6 | 🔴 Whole-surface no-actuation grep CLEAN (B-1 expanded) | `…\|position\|balance\|margin\|capital\|allocation\|real_pnl\|open_gate\|allow_execution` → no output (L579) | ✅ PASS |
| E-7 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L593) | ✅ PASS |
| E-8 | No-drift: deps / endpoint / persistence | package grep = `lightweight-charts@^4.2.0` only; no `/api/v1/investigation-planning`, no CREATE TABLE / createWorkspacePreference / `investigation-planning-workspace-v1` | ✅ PASS |
| E-9 | No registry / route change (R-1) | `investigate.signal_investigation` / `/investigate` only; **no `/investigation-planning`** (L613) | ✅ PASS |
| E-10 | No persistence (R-2 — P02 persists nothing) | no `operator_workspace_preferences` write, no key | ✅ PASS |
| E-11 | Regression ≥44f/191t, no test lost | **Gated** `FRONTEND_VITEST_EXIT_CODE: 0` (L880) → **45 files / 196 tests passed** (L855–856; evidence file L289) +1 file/+5 tests | ✅ PASS |
| E-12 | Backend ≥414 | `pytest -q` → **414 passed** (two runs) | ✅ PASS |
| E-13 | Doc-16 brand B-1…B-7 (never color alone) | monospace ids/hashes/model version; ARIA sections; institutional copy; named test #5 + browser | ✅ PASS |
| E-14 | Browser served-session | `/investigate` frame (GATE CLOSED/RESEARCH-ONLY) + selected signal detail with verbatim lineage/guardrails/`economically_usable`/`50.0% calibrated` + "does not change this signal / rerun the model / alter guardrails / create an instruction" + LINKED VALIDATION AND REPORT IDS | ✅ PASS (see OBS-P02-1) |
| E-15 | Networked CI / npm audit | See §4 — CI exit-1 is the tracked **TD-UI-POSTCSS-HIGH** (real advisory correctly reported, NOT the env-flake), operator-dispositioned under the standing P06 rule | ⚠️ §4 |

---

## 3. Constitutional line

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Live broker/order/account/position/balance/margin/capital/allocation/real-P&L path | NONE (expanded no-actuation grep clean) |
| External LLM / AI-summary | NONE (external-AI grep clean) |
| Signal recompute / model rerun / guardrail override / confidence derivation / reclassification / signal generation | NONE (no-recompute grep + named tests + explicit UI copy) |
| Verbatim lineage/confidence/economic | HELD — as-stored; `50.0% calibrated` not raw score; state badges not upgraded |
| Related-reports | Disclosure/navigation only, no recompute |
| Persistence / new table / registry / route | NONE (R-1/R-2 held; head unchanged) |

Investigation is read-only disclosure of persisted evidence — the browser copy itself states it "does not change this signal, rerun the model, alter guardrails, or create an instruction."

---

## 4. npm audit posture — TD-UI-POSTCSS-HIGH reproduced on target (operator-adjudicated)

This turn the networked npm audit **reached the registry** (no ECONNRESET/ENOTFOUND) and correctly reported the **real** advisory set: **`3 vulnerabilities (2 moderate, 1 high)`** — the high being **`postcss <=8.5.17` GHSA-r28c-9q8g-f849** (in both the standalone audit L677–699 and the CI audit L1530–1561) → `NPM_AUDIT_HIGH_EXIT_CODE: 1` / `LOCAL_CI_EXIT_CODE: 1` / `LOCAL_CI_NONZERO_REVIEW_REQUIRED: 1`.

- **This is NOT the TD-W6-CI-AUDIT env-flake** (which is a network failure). It is the already-registered **TD-UI-POSTCSS-HIGH** residual (opened at UI-004-P06) reproducing on target. The DA surfaced it and did **not** relabel green — correct discipline.
- **All substantive gates ran green** (`FRONTEND_VITEST_EXIT_CODE: 0` → 45f/196t, backend 414, tsc/build clean) **before** the audit step.
- **Operator disposition (this review): proceed under the standing P06 disposition.** No dependency change is in UI-005-P02 scope; the presentation-only phase is not gated by the transitive advisory. **TD-UI-POSTCSS-HIGH remains OPEN and MUST be remediated or formally accepted before Production Readiness Certification (Doc 11).** A separately-authorized dependency-remediation Build Order will address it (unchanged from P06).

---

## 5. Observations (non-blocking)

- **OBS-P02-1 (browser evidence — minor):** Only 2 served screenshots this turn (`/investigate` frame + investigation detail). **No logged-out `/login` block shot** was supplied (Build-Order item (j)). Non-blocking: P02 adds no route/auth change and logged-out protection was proven at P01 and is unchanged. Include a logged-out shot at P03 for continuity.
- **OBS-P02-2 (evidence-form — CLOSED from OBS-P01-2):** The standalone `FRONTEND_VITEST_EXIT_CODE: 0` sentinel was printed this turn alongside the full 45f/196t total — OBS-P01-2 continuity request satisfied.

---

## 6. Carried standing residuals

- **TD-UI-POSTCSS-HIGH** — high-severity transitive advisory `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) — **reproduced on target this turn**; OPEN; requires a separately-authorized dependency-remediation Build Order; MUST be remediated/accepted before Production Readiness Certification.
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — did NOT occur this turn; audit was networked)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-005-P02 is APPROVED WITH OBSERVATIONS.** This authorizes issuance of the next Build Order (**UI-005-P03 — Scenario Comparison & Portfolio Research Context**, per confirmed R-5 mapping) upon operator "authorized". P03 carries R-1…R-7 and the design-plan P03 named-test anchors (scenarios render existing hypothetical reports only; portfolio remains hypothetical no real account/P&L; comparison preserves assumptions/uncertainty/limitations/scope; no generation/execution path; a11y/brand) — and should include a logged-out shot (OBS-P02-1).

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 45f/196t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
