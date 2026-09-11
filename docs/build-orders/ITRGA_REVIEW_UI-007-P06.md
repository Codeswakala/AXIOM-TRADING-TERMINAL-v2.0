# ITRGA DETERMINATION — UI-007-P06

**UI-007 Completion Checkpoint** — *(Proof unit)*

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P06 — Completion Checkpoint** |
| Build Order | `BUILD_ORDER_UI-007-P06.md` |
| Pack | `DELIVERY_REPORT_UI-007-P06.md` (180 lines) + `UI-007-P06_OPERATOR_RESULTS.md` (1108 lines) + 10 served screenshots |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 60f/271t |
| **DETERMINATION** | 🟡 **CORRECTIVE ACTIONS REQUIRED — single item (R-6 served-UI match)** |
| Baseline | **UNCHANGED — v0.62.0** |
| UI-007 completion | **NOT DECLARED** (pending the single corrective) |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build identity — ✅ PASS

| Check | Result |
|---|---|
| Transcript | **1108 lines / 130,444 bytes**; **56 P06 references**; `UI007_P06_EVIDENCE_STARTED: 2026-07-28T22:46:17` | ✅ |
| Identity gate | `UI007_P06_BUILD_IDENTITY_CONFIRMED` | ✅ |
| Repo root | `C:\Users\Swakala\.vscode\AXIOM\axiom` | ✅ |
| P05 references (49) | Contextual — the P06 runner **deliberately re-invokes** the proven P05 v2.0.0 regression runner (`UI007_P06_REUSED_P05_RUNNER_EXIT_CODE: 0`). Correct reuse, not a stale pack | ✅ |

**Pack confirmed OF UI-007-P06.** No stale/wrong-phase attachment.

---

## 2. ✅ Proven at Level-I — nearly the whole checkpoint

| # | Item | Evidence | Verdict |
|---|---|---|---|
| (b) | **5 completion tests DISPLAYED passing** | All five by name: `..._governance_audit_evidence_health_and_version_are_discoverable` · `..._all_governance_surfaces_are_read_only_and_inert` · `..._no_actuation_recompute_external_ai_gate_or_certification_control` · `..._verbatim_no_cherry_picking_and_residual_disclosure_hold` · `..._accessibility_doc16_brand_and_ui001_ui002_integration_hold`; `NAMED_VITEST_EXIT_CODE: 0` | ✅ |
| (c) | 🔴 **R-6 raw-psql audit proof** | `UI007_P06_REFUSED_AUDIT_ID: 055e3295-b485-4e84-9771-04c2318bf0b0` — full row: `SECURITY` / `plugin_contract_request.refused` / actor `w7-u05-evidence-operator` / **`PLUGIN_CONTRACT_IMPORT_REFUSED`** / `2026-07-18 22:59:07`; `(1 row)`; `R6_AUDIT_PSQL_EXIT_CODE: 0`. **Existing row — no audit event created** | ✅ **psql half** |
| (d) | 🔴 Whole-surface governance-mutation/Gate/certification grep | `GOVERNANCE_CONTROL_EXIT_CODE: 0` | ✅ |
| (e) | 🔴 Whole-surface no-actuation (M-4 + ops terms) | `NO_ACTUATION_EXIT_CODE: 0` | ✅ |
| (f) | 🔴 No-recompute / no-external-AI | `R6_NO_RECOMPUTE_EXIT_CODE: 0`; `EXTERNAL_AI_EXIT_CODE: 0` | ✅ |
| (g) | 🔴 Verbatim + no-cherry-picking + **residual disclosure** | Browser: all nine residuals rendered incl. **`TD-AXIOM-GIT-PROVENANCE` OPEN·HIGH·PRE-CERTIFICATION BLOCKER** and `TD-UI005-COMPLETION-TIMEOUT` OPEN·LOW; validation panels show scope/uncertainty/limitations verbatim; *"A filtered view is not a full-scope governance claim"* | ✅ |
| (h) | 🔴 **H-1 runtime ≠ certification (carried)** | `FORBIDDEN_RUNTIME_LABEL_EXIT_CODE: 0`; browser shows the callout, `Production NOT CERTIFIED`, `Doc 11 HELD`, and the certification-boundary card | ✅ |
| (i) | No-drift | `alembic current 20260717_0037`; registry delta empty; frontend manifest delta empty; `pyproject.toml` conflict-repair diff displayed; no new endpoint | ✅ |
| (j) | **Full regression** | `FRONTEND_VITEST_EXIT_CODE: 0` · **`Test Files 61 passed` / `Tests 276 passed`** · backend **`414 passed`** with `BACKEND_PYTEST_EXIT_CODE: 0` · ruff · tsc · build | ✅ |
| (k) | Doc 16 B-1…B-7 | Monospace ids/hashes/counts, institutional palette, text labels with status colour; named test #5 | ✅ |
| (l) | UI-001 / UI-002 integration | Single shell; nav dock, breadcrumb, switcher, palette registry-consistent; `/governance` mounts in the UI-001 frame; named test #5 | ✅ |
| (n) | **Networked CI** | **`LOCAL_CI_EXIT_CODE: 0`** — clean, no waiver. `TD-UI005-COMPLETION-TIMEOUT` did **not** recur | ✅ |
| (o) | Docs/registers reconciled | PROJECT_STATE · CHANGELOG · TECHNICAL_DEBT_REGISTER · GOVERNANCE_AMENDMENTS updated | ✅ |
| §6 | **Residual disposition** | All nine dispositioned in report §6, incl. `TD-AXIOM-GIT-PROVENANCE` display-only and **OBS-P05-5 fixed** (URLs now in angle brackets) | ✅ |

**Test delta reconciles exactly:** 271 → **276** = +5, precisely the five completion tests. File 61 is `GovernanceEvidenceCompletion.test.tsx`. No test lost.

---

## 3. ❌ CA-P06-1 (the single blocker) — the R-6 served-UI half is not evidenced

R-6 has **two limbs**. The Build Order §4 required both:

> *"Raw `psql SELECT` … ≥1 row, including ≥1 `*_REFUSED` row"* **and** *"the served UI renders the same rows verbatim — screenshot beside the psql output."*

**Limb 1 — psql: ✅ PROVEN.** The `PLUGIN_CONTRACT_IMPORT_REFUSED` row is displayed in full, from an existing row, exit 0.

**Limb 2 — served UI: ❌ NOT PROVEN.** The audit-explorer screenshot shows the detail pane rendering a **different** row:

| Field | psql proof | Browser detail pane |
|---|---|---|
| Audit id | `055e3295-b485-…-04c2318bf0b0` | `48f85735-8d6a-…-1a5ed850494d` |
| Category | `SECURITY` | `GOVERNANCE` |
| Action | `plugin_contract_request.refused` | `operator_workspace_preference.updated` |
| Reason code | `PLUGIN_CONTRACT_IMPORT_REFUSED` | `—` (none) |

The explorer is sorted **Newest first** and shows *"50 of 50 audit rows"*; the refused row is from **2026-07-18**, so it falls outside the visible window. **The refused row is never shown on screen.**

**Why this cannot be waived:** R-6 exists to prove the UI renders the audit trail *verbatim* — specifically that a `*_REFUSED` code is displayed as a stored refusal and **not reinterpreted as an authorization path**. A psql row plus a screenshot of a *different, non-refusal* row does not demonstrate that. The refusal-rendering property is the entire point of the control, and it is precisely what P03 proved and what P06 must re-prove at completion.

**The DA's own harness flagged this.** `UI007_P06_BROWSER_MANIFEST_EXIT_CODE: 1` lists all four named captures as missing, including `UI-007-P06_02_R6_AUDIT_REFUSAL_MATCH.png` — the exact artifact needed. The terminal sentinel reads `EVIDENCE_COMPLETED_WITH_FINDINGS` with *"Do not relabel a nonzero result green."* Report §130 likewise states browser evidence *"remains mandatory Level-I evidence. This report does not claim they were collected."*

**I am agreeing with the DA's own instrument, not overruling it.**

**Note:** the ten supplied screenshots are excellent and cover the whole workspace end-to-end — governance frame, status, certification, residuals, audit explorer, evidence viewer, validation summaries, health/readiness/posture, data-source inventory, and the Incognito `/login` block. Only the refusal-row match is missing.

---

## 4. Findings

| ID | Severity | Status |
|---|---|---|
| **CA-P06-1** | **HIGH** | ❌ **OPEN** — R-6 served-UI limb: audit explorer must display the `PLUGIN_CONTRACT_IMPORT_REFUSED` row (`055e3295-…`) matching the psql output |
| — | — | ✅ Every other mandatory item proven at Level-I |
| OBS-P05-5 | OBSERVATION | ✅ **CLOSED** — URLs isolated in angle brackets; no recurrence of the trailing-period defect |
| OBS-P06-1 | OBSERVATION (new) | Runner names four required captures but the operator supplied ten differently-named files. Align naming, or have the manifest check accept a supplied-file mapping, so a complete capture set cannot read as missing |
| TD-UI005-COMPLETION-TIMEOUT | TECHNICAL DEBT | Did **not** recur — CI clean at exit 0. Remains open (fixed timeout unchanged) |
| **TD-AXIOM-GIT-PROVENANCE** | TECHNICAL DEBT (HIGH) | Standing pre-certification blocker; correctly displayed, correctly not remediated here |
| — | **COMMENDATION** | The whole-surface proof discipline is exemplary: every boundary grep clean across all six phases, the R-6 psql row drawn from existing data with no manufactured audit event, full regression 61f/276t + backend 414 + **CI exit 0 with no waiver**, all nine residuals dispositioned, and OBS-P05-5 fixed unprompted. The harness again reported its own shortfall rather than concealing it |

---

## 5. Required correction — one screenshot

> **CA-P06-1 —** In the served audit explorer, surface the row `055e3295-b485-4e84-9771-04c2318bf0b0` (filter by `PLUGIN_CONTRACT_IMPORT_REFUSED`, `plugin_contract_request.refused`, or `SECURITY`; the in-memory filter already supports this) and capture the detail pane showing **audit id · category · action · actor · reason code** matching the psql output. Save as `UI-007-P06_02_R6_AUDIT_REFUSAL_MATCH.png`.

**Nothing else is to be re-run.** The five completion tests, all boundary greps, the psql proof, 61f/276t, backend 414, alembic head, CI exit 0, Doc-16, UI-001/UI-002 integration, residual disposition and the logged-out block are **proven and stand**.

---

## 6. Disposition

**UI-007-P06 is CORRECTIVE ACTIONS REQUIRED — one screenshot from completion.**

This is a strong completion pack. The whole-surface proofs hold across all six phases: no governance mutation, no Gate or certification control, no actuation or ops-actuation, no recompute, no external AI. The regression envelope is complete and clean, including a networked CI at exit 0 with no waiver — the second consecutive clean CI. Every residual is disclosed at honest severity, including the HIGH pre-certification blocker ITRGA opened against the repository itself. The refusal row was pulled from existing data with no audit event manufactured for evidence.

What is missing is the second limb of the keystone control. R-6 is not "show a psql row and show the audit UI" — it is "show that **this** refusal row renders **verbatim** in the UI, and is not reinterpreted as an authorization path." The screenshot shows a different, non-refusal row because the explorer sorts newest-first and the refused event is ten days old. The proof of the property that matters was never captured.

I will not declare a workstream complete on a completion gate that is half-proven — least of all this workstream, whose entire thesis is that governance is *visible* without becoming *governable*. The visibility of a constitutional refusal is exactly the thing being certified here.

One filtered screenshot closes it, and UI-007 is complete.

Verification is limited to supplied evidence. Direct validation of the served refusal-row rendering was not possible.

**Baseline does NOT advance — v0.62.0 · head `20260717_0037` · backend 414 · frontend 60f/271t of record** (61f/276t proven and will become the baseline on approval). **UI-007 completion NOT DECLARED.** Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

## 7. Evidence Confidence Statement

- **Evidence reviewed:** `UI-007-P06_OPERATOR_RESULTS.md` (1108 lines, read in full); `DELIVERY_REPORT_UI-007-P06.md` (180 lines); 10 served screenshots (viewed).
- **Confidence:** **HIGH** on every item in §2 — sentinels, totals, greps, psql row and residual disclosure are directly evidenced. **HIGH** that the R-6 served-UI limb is unmet — the audit ids differ on their face and the runner's own manifest check exited 1.
- **Remaining unknowns:** whether the served UI renders the `*_REFUSED` row verbatim (expected to pass, unevidenced).
- **Additional evidence required:** §5 — one filtered screenshot.

---

*Half a keystone is not a keystone. The other half is one filter away.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
