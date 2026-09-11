# ITRGA DETERMINATION — UI-007-P03

**Read-Only Audit Explorer & Refusal Reason-Code Viewer**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P03** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P03.md` |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §2.1/§3 (G-4), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8, esp. R-6), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 57f/256t (vite-8) |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

Pack confirmed OF UI-007-P03 (delivery report 387 lines; `OPERATOR_RESULTS.md` 207 lines references BUILD_ORDER_UI-007-P03 + P02 review). No stale/wrong-phase/concatenated pack. **Note:** the transcript is short (207 lines) because it halted early — see §3.

---

## 2. Level-I evidence verification — G-4 audit read-only + R-6 verbatim (the spine)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | **5 passed (5)** (L55–66): audit_explorer_renders_existing_audit_events_read_only / **audit_reason_codes_and_refusals_render_verbatim_no_inference** / audit_explorer_filter_sort_are_in_memory_no_persistence_or_mutation / audit_explorer_contains_no_governance_mutation_gate_or_certification_control / audit_explorer_accessibility_and_doc16_brand_hold | ✅ PASS |
| E-2 | 🔴 R-6 verbatim audit-render RAW PSQL PROOF | `UI007_P03_REFUSED_AUDIT_ID: 055e3295-…`; `UI007_P03_REFUSED_REASON_CODE: PLUGIN_CONTRACT_IMPORT_REFUSED`; raw psql `(1 row)` — SECURITY / `plugin_contract_request.refused` / actor `w7-u05-evidence-operator` / `PLUGIN_CONTRACT_IMPORT_REFUSED` / created_at — plus 20-row `audit_events` dump; served UI (screenshot) renders same rows/fields verbatim; existing rows only (no audit event created for evidence) | ✅ PASS |
| E-3 | 🔴 No inference on refusals | `*_REFUSED` rendered as stored refusal; refusal reason-code viewer: "does not reinterpret them as an authorization path"; named test #2 | ✅ PASS |
| E-4 | 🔴 G-4 audit read-only | `UI007_P03_AUDIT_READ_ONLY_GREP_CLEAN` (no create/edit/delete/redact/replay/mark-reviewed/acknowledge/persist-filter); in-memory filter/sort; named tests #3/#4 | ✅ PASS |
| E-5 | 🔴 G-2 governance-control + M-4 no-actuation + no-recompute + external-AI greps CLEAN | `UI007_P03_GOVERNANCE_CONTROL_GREP_CLEAN` / `..._NO_ACTUATION_GREP_CLEAN` / `..._R6_NO_RECOMPUTE_RELATIONSHIP_INFERENCE_GREP_CLEAN` / `..._EXTERNAL_AI_GREP_CLEAN` (all throw-guarded) | ✅ PASS |
| E-6 | Existing audit-events API only (no new endpoint) | `fetchAuditEvents` → existing `GET /api/v1/persistence/audit-events` (client.ts L591–595); no new backend endpoint | ✅ PASS (see §3 on the false-positive) |
| E-7 | No-drift: deps / registry / persistence | package manifest displayed no new-phase dep; no registry/route change; no governance-state/saved-filter persistence | ✅ PASS |
| E-8 | **Gated full-suite exit 0 / ≥57f/256t + backend 414 + alembic head + CI** | **NOT in transcript** — run HALTED at ~L207 before these gates; delivery report §12 CLAIMS 58f/261t + backend 414 + alembic head, but no operator-run proof | ⚠️ **OBS-P03-1 (report-claim only; operator-adjudicated)** |

---

## 3. 🔴 Findings — false-positive halt + unproven regression (operator-adjudicated)

- **F-1 (grep false-positive that HALTED the run):** the DA's no-new-endpoint grep pattern included `/governance`, which matched the **pre-existing** `backend\app\external_integration\broker\governance_gate.py` (the constitutional Governance Gate module — "Future changes require roadmap/governance authorization"). This is a **false-positive** — that file is not a new endpoint and the audit UI uses only the existing `/api/v1/persistence/audit-events`. But with `$ErrorActionPreference="Stop"`, the throw **halted the evidence transcript** before the mandatory regression/CI. **Fix required (P04):** exclude `governance_gate.py` / anchor the pattern to actual new-route/endpoint declarations so the evidence run completes.
- **OBS-P03-1 (regression/CI unproven in transcript; operator-adjudicated to Approve-w-Obs):** the mandatory gated full-suite (`FRONTEND_VITEST_EXIT_CODE:0`, ≥57f/256t), backend `pytest 414`, alembic head, and networked CI are **absent from the operator transcript** (halted at F-1). The delivery report §12 asserts **58f/261t + backend 414 + alembic 20260717_0037**, but per Level-IV/R7 a report claim without operator-run evidence does not itself approve. **Operator adjudication:** given the strength of the P03-specific evidence (5 tests, R-6 raw-psql refused-audit verbatim proof, all boundary greps clean, existing API only) and that F-1 is a benign false-positive, **accept the report regression figures for P03 this once** and require a **completed operator transcript** (fixed grep, gated `FRONTEND_VITEST_EXIT_CODE:0` full-suite + backend 414 + CI) at **UI-007-P04**. These gaps are **documented, not relabeled green.**

---

## 4. Governance boundary — held

| Property | State |
|---|---|
| Audit mutation (create/edit/delete/redact/replay/mark-reviewed/acknowledge) | NONE — read-only; grep clean + named tests |
| Reason-code / refusal reinterpretation | NONE — `*_REFUSED` verbatim; "not an authorization path" |
| Governance/Gate/certification control | NONE (G-2 grep clean) |
| Actuation / external AI / recompute | NONE (greps clean) |
| New endpoint / dependency / persistence | NONE — existing audit-events API only; F-1 was a false-positive on a pre-existing Gate file |

The read-only audit explorer renders existing `audit_events` (incl. a genuine `*_REFUSED` reason-code) verbatim with no mutation surface — exactly the G-4 intent, and the `PLUGIN_CONTRACT_IMPORT_REFUSED` row confirms the constitutional refusal audit trail is surfaced honestly.

---

## 5. Observations (mandatory closure at P04)

- **OBS-P03-1 (MANDATORY at P04):** supply a **completed** operator transcript with the gated `FRONTEND_VITEST_EXIT_CODE:0` full-suite (≥ baseline, no test lost) + backend `pytest 414` + `alembic current 20260717_0037` + networked CI — i.e. the evidence the P03 run halted before producing. Non-waivable at P04.
- **OBS-P03-2 (grep hygiene):** fix the no-new-endpoint evidence grep so `/governance` no longer false-trips on the pre-existing `governance_gate.py` (exclude that path or anchor to route/endpoint declarations); a `$ErrorActionPreference=Stop` on a false-positive must not truncate the mandatory evidence again.

---

## 6. Carried standing residuals

- TD-UI-REACTROUTER-MODERATE (moderate, non-blocking) · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b · (TD-UI-POSTCSS-HIGH CLOSED)

---

## 7. Disposition

**UI-007-P03 is APPROVED WITH OBSERVATIONS.** The read-only audit explorer + refusal reason-code viewer are constitutionally clean: G-4 audit read-only, `*_REFUSED` rendered verbatim with no inference, all boundary greps clean, existing audit-events API only, and the R-6 raw-psql verbatim-render proof is genuine (`PLUGIN_CONTRACT_IMPORT_REFUSED`). Two findings are recorded (F-1 false-positive halt; OBS-P03-1 regression/CI unproven in transcript) and folded into UI-007-P04 as mandatory closures — not relabeled green.

This authorizes issuance of the next Build Order (**UI-007-P04 — Evidence Viewer & Validation Summary Panels**) upon operator "authorized", carrying the OBS-P03-1 completed-transcript closure + OBS-P03-2 grep fix.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 58f/261t** (per the report; the gated total to be re-confirmed by the completed transcript at P04).

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
