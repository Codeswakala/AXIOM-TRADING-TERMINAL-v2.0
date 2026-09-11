# BUILD ORDER — UI-007-P04

**Evidence Viewer & Validation Summary Panels** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P04** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-007-P03.md` — ✅ Approved with Observations (carries OBS-P03-1/-2) |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-5)/§8 (P04), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8, esp. R-3 evidence-viewer depth), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **58f/261t** (per P03 report; re-confirmed by the completed transcript this phase) |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Add the **evidence viewer** and **validation summary panels** — rendering existing evidence records and validation summaries **verbatim as-stored**. **G-5 (verbatim disclosure, no AI-summary / no recompute / no cherry-picking) is the spine.** Read-only display; no governance/audit/verdict mutation.

**IN scope:**
1. Evidence viewer — a **manifest/index + stored fields** for existing evidence/validation records (id/type/status-verdict-as-stored/method-version/sample count/scope/uncertainty/limitations/source ids/lineage/audit references/report hash/dates), rendered verbatim (R-3). Static first-party bundled markdown excerpts are acceptable ONLY if no backend file-listing API is added and no new dependency (no markdown lib without a spike); otherwise index + stored-field disclosure only.
2. Validation summary panels — existing validation summaries shown as-stored; scope/sample/uncertainty/limitations visible; no-cherry-picking.

**OUT of scope (do NOT build):**
- Health/readiness/version (P05), completion (P06).
- **AI-generated summaries, recomputed validation verdicts, stronger labels than source, hidden-scope aggregate claims, cherry-picked filtered results presented as complete** (G-5).
- Any governance/audit/Gate/certification/validation-verdict mutation (G-1…G-4); actuation (G-6/M-4); external AI/LLM; recompute/inference/reclassification.
- Any new backend endpoint / service / table / migration / dependency (incl. a markdown-rendering lib) / governance-state persistence (G-7); saved-view persistence.
- A backend evidence file-listing/certification endpoint (R-2/R-4 — canonical records / existing read APIs only).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/governance`; no new route; 14-field registry contract unchanged.
- **R-3** — Evidence viewer = **manifest/index + verbatim stored fields**; static first-party markdown excerpts only if no file-listing API + no new dependency; else index + stored fields.
- **R-6 (SPINE)** — G-5 verbatim; no AI-summary/recompute/reclassify; no-cherry-picking (scope/sample/uncertainty/limitations visible).
- **R-7** — G-5 read-only; mandatory named test `test_ui007_evidence_viewer_contains_no_governance_mutation_gate_or_certification_control`; G-2 grep + M-4 no-actuation grep + no-recompute/external-AI grep.
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost, gated exit 0; networked CI exit 0.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui007_evidence_viewer_renders_existing_records_verbatim_no_ai_summary`
2. `test_ui007_validation_summaries_preserve_scope_sample_uncertainty_and_limitations_no_cherry_picking`
3. `test_ui007_evidence_viewer_no_recomputed_or_stronger_verdicts_than_source`
4. `test_ui007_evidence_viewer_contains_no_governance_mutation_gate_or_certification_control`
5. `test_ui007_evidence_viewer_accessibility_and_doc16_brand_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL creds standard.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-007-P04.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 G-5 verbatim proof** — evidence/validation fields rendered as-stored; no AI-generated summary; no recomputed/stronger verdict than source (grep for `openai|gpt|external_llm|llm_summary|ai_summary` + `recompute|recalculat|deriveConfidence|reclassif|new .*Engine` CLEAN); named tests #1/#3.
- (d) **🔴 No-cherry-picking** — validation summaries show scope/sample/uncertainty/limitations; filtered views never claim complete/full-scope truth unless the stored record declares it; named test #2.
- (e) **🔴 G-4/G-1 read-only + G-2 governance-control grep CLEAN** — no evidence/validation/verdict mutation control; `open_gate|allow_execution|gate.*toggle|certify|mark_ready|approve_production|waive|risk_accept` → no output; named test #4.
- (f) **🔴 M-4 whole-surface no-actuation grep CLEAN**.
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (**no new dependency — specifically no markdown-rendering lib**); no new endpoint grep (no evidence file-listing/certification endpoint); no registry/route change; no persistence.
- (h) **🔴🔴 OBS-P03-1 CLOSURE (MANDATORY) — completed regression transcript:** a **clean gated `FRONTEND_VITEST_EXIT_CODE: 0`** full-suite run (frontend **≥58f/261t**, no test lost; verify FULL total; print the sentinel) + backend `pytest -q` **≥414 passed** + `alembic current 20260717_0037` + networked CI — the operator-run evidence the P03 transcript halted before producing. **A report-only regression claim again ⇒ Corrective.**
- (i) **🔴 OBS-P03-2 CLOSURE** — the no-new-endpoint evidence grep is fixed so `/governance` no longer false-trips the pre-existing `governance_gate.py` (exclude that path / anchor to route-endpoint declarations); the evidence run completes without a false-positive halt.
- (j) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics (evidence/validation ids/hashes/sample counts) / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (k) **Browser served-session screenshots** — logged-in `/governance` evidence viewer (index + verbatim stored fields) + validation summary panels (scope/sample/uncertainty/limitations visible); **no AI summary, no mutation control**; logged-out `/login` block.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel (achievable — postcss remediated, keep `@rolldown` file-lock resolved); OR documented TD-W6-CI-AUDIT env-flake after substantive gates green → waiver. **An EPERM/127, a red gated run, or a halted evidence transcript is a finding.**

---

## 5. Determination rule

A single CRITICAL, an AI-generated summary, a recomputed/stronger-than-source verdict, cherry-picked full-scope claims, any evidence/validation mutation control, a new dependency (incl. markdown lib) or endpoint, a report-only regression (OBS-P03-1 unmet), a halted/false-positive evidence transcript (OBS-P03-2 unmet), or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-007-P05 — Platform Health, System Readiness, Version & API Posture).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
