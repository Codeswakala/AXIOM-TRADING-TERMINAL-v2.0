# ITRGA REVIEW — UI-007 ENGINEERING DESIGN PLAN

**Governance & Evidence Workspace**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-007 — Governance & Evidence Workspace** (NEW) |
| Document reviewed | `UI-007_ENGINEERING_DESIGN_PLAN.md` (858 lines) |
| Cover report | `DELIVERY_REPORT_UI-007_DESIGN_PLAN.md` (262 lines) |
| ITRGA request | `docs/ITRGA_REQUEST_UI-007_DESIGN_PLAN.md`; intake hold `ITRGA_INTAKE_UI-007_DESIGN_PLAN_AWAITING_PLAN_FILE.md` (now resolved) |
| Governing docs | Doc 12 §9, Doc 13, completed UI-001…UI-006, Doc 16 Part XIV, constitutional corpus Docs 00–11 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 55f/246t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-8** |
| Authorizes | Issuance of `BUILD_ORDER_UI-007-P01` (on operator "authorized") — NOT implementation |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Plan header | `# UI-007 Engineering Design Plan — Governance & Evidence Workspace`; "pre-Build-Order; no implementation authorization" — OF the workstream |
| Plan length | 858 lines — the actual deliverable (the prior on-hold gap is now closed) |
| References request + baseline + residual | Yes (`ITRGA_REQUEST_UI-007_DESIGN_PLAN.md`, UI-006 COMPLETE, 55f/246t, TD-UI-POSTCSS-HIGH non-waivable pre-cert blocker in header) |

**Pack confirmed OF the UI-007 Design Plan document** (not a cover summary). The intake hold is resolved.

---

## 2. Assessment against the governance boundary (G-1…G-7) — the defining risk

| Line | Plan coverage (§3) | Verdict |
|---|---|---|
| **G-1 read-only display** | Forbids create/update/delete/approve governance status, waive residual, accept risk, certify production, mark ready, open/close/toggle Gate, edit/delete/redact/replay audit, change validation/readiness verdict; required per-phase test | ✅ Met (exemplary) |
| **G-2 Gate CLOSED inert** | Rendered as read-only constitutional fact; must NOT be button/switch/checkbox/select/input/form/palette-action/menu-action/API-mutation/workflow-step; grep incl. `open_gate\|allow_execution\|gate.*toggle\|certify\|mark_ready\|approve_production\|waive\|risk_accept` | ✅ Met (exceeds request) |
| **G-3 certification display not actuation** | Doc-11 outcomes (CERTIFIED/…/NOT CERTIFIED) shown as-stored; no certification workflow/approval/waiver/sign-off/readiness mutation | ✅ Met |
| **G-4 audit explorer read-only** | `audit_events` verbatim; permitted view/in-memory-filter/sort; forbidden create/edit/delete/redact/replay/mark-reviewed/acknowledge-as-approval/persist-filter-as-state | ✅ Met |
| **G-5 evidence verbatim** | as-stored fields; forbidden AI summaries/recomputed verdicts/stronger labels/hidden-scope/cherry-picking | ✅ Met |
| **G-6 no actuation/external-AI/recompute** | full expanded grep lists (M-4 + AI + recompute/inferRelationship) | ✅ Met |
| **G-7 read-only reuse** | no new endpoint/service/table/migration/dependency/governance-state-persistence | ✅ Met |

**§2.1 audit read-API confirmed** (`GET /api/v1/persistence/audit-events` → `list[AuditEventRead]` from `audit_events`; reason-code `details.reason_code`/`*_REFUSED` verbatim, "No inference that refusal implies an authorization path"). **§2.2 certification honesty** (no backend certify endpoint; canonical records only). **§4.3 forbidden naming** pre-empts control-shaped routes/labels (`/admin`, `/gate`, `Governance Control`, `Open Gate`, `Approve Production`). This is the strongest possible governance-boundary treatment.

---

## 3. Adjudication of the DA's six open questions → binding refinements

- **R-1 — Route/registry (Q1):** ACCEPT a single protected **`/governance`** route in P01, under the 14-field Workspace Registry contract with `requiresAuth:true` + `noActuation:true`, `Govern` category. Prove the contract is unchanged and navigation is non-duplicative. Forbidden naming (§4.3) is binding. If P01 evidence cannot preserve the contract cleanly, fall back to enhancing an existing surface (no new route) — but `/governance` is authorized in principle.
- **R-2 — Certification source (Q2):** **Canonical read-only certification display is sufficient; DO NOT add a certification-status backend endpoint.** A cert endpoint (even read-only) is an actuation-shaped surface risk; certification remains an out-of-band ITRGA/Doc-11 governance act. Display `Production: NOT CERTIFIED` / `Doc 11: HELD` / `TD-UI-POSTCSS-HIGH: non-waivable pre-cert blocker` as inert facts.
- **R-3 — Evidence viewer depth (Q3):** P04 evidence viewer = **manifest/index + stored fields rendered verbatim** (id/type/status-verdict-as-stored/method-version/sample/scope/uncertainty/limitations/source-ids/lineage/hash/dates). **No AI summaries, no recomputed verdicts, no cherry-picking.** Rendering selected first-party bundled markdown excerpts is acceptable ONLY if (a) it is static first-party content, (b) no backend file-listing API is added, and (c) it introduces no new dependency (no markdown lib without a spike) — otherwise index + stored-field disclosure only.
- **R-4 — Readiness dispositions (Q4):** W7-U07 readiness dispositions displayed from **existing governance/read records or existing code constants**, verbatim; a new backend read route requires separate ITRGA authorization (not granted here).
- **R-5 — TD-UI-POSTCSS-HIGH scheduling (Q5):** The dedicated **dependency-remediation Build Order MUST be scheduled BEFORE UI-007-P02** (which renders certification status — it is incoherent to display a "non-waivable pre-cert blocker" surface while the blocker itself is unaddressed for two more phases). Until remediated, every UI-007 phase displays the residual honestly (open, non-waivable) and never relabels the audit green. Remediation-BO evidence per plan §7 (manifest diff + networked `npm audit --audit-level=high` exit 0 + green suite + tsc/build).
- **R-6 — Audit raw-psql cadence (Q6):** Raw psql audit-event evidence is required at **P03 (audit explorer)** and **P06 (completion)**. Audit is read-only display (not a new persisted write), so a save→SELECT persistence-capture is not owed; instead P03/P06 must show a raw psql `SELECT` from `audit_events` confirming the UI renders **verbatim** what the table holds (incl. `details->>'reason_code'` / `*_REFUSED`), matching served rows.
- **R-7 — Governance-boundary SPINE (every phase).** Each phase MUST carry the named test `test_ui007_<surface>_contains_no_governance_mutation_gate_or_certification_control` + the G-2 grep (`open_gate|allow_execution|gate.*toggle|certify|mark_ready|approve_production|waive|risk_accept`) + the whole-surface M-4 no-actuation grep + no-recompute/external-AI grep. Verbatim + no-cherry-picking preserved.
- **R-8 — Level-I + Doc-16 + regression.** Build-identity FIRST; named tests DISPLAYED passing; no-drift substitute (head `20260717_0037`, manifests unchanged unless the R-5 remediation BO, no-endpoint unless separately authorized, no registry change unless R-1-approved); full suite ≥ **55f/246t** no test lost + backend ≥414 gated exit 0; **Doc-16 brand B-1…B-7 (never color alone)**; served browser evidence incl. logged-out; networked CI exit 0 + sentinel, or TD-W6-CI-AUDIT env-flake waiver, or `LOCAL_CI_EXIT_CODE:1` solely the tracked TD-UI-POSTCSS-HIGH after gates green — any other nonzero is a finding.

---

## 4. Observations (non-blocking)

- **OBS-DP-1:** Phase split is accepted: P01 frame/route/inventory/read-only-guardrails → P02 governance-status/Gate-CLOSED/certification display → P03 read-only audit explorer + refusal reason-codes → P04 evidence viewer + validation summaries → P05 platform health/readiness/version/API posture → P06 completion.
- **OBS-DP-2 (R-5 emphasis):** The postcss remediation BO before P02 is now a **scheduling condition**, not merely a recommendation — P02's certification-status surface makes an unaddressed pre-cert blocker especially conspicuous. If the operator prefers, the remediation BO may be issued immediately after this plan approval (before P01).
- **OBS-DP-3 (§4.3):** The DA's self-imposed forbidden route/control naming is adopted as a standing acceptance condition for UI-007.

---

## 5. Disposition

**UI-007 Design Plan is APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-8.** On the most constitutionally reflexive workstream, the plan holds the defining line with precision: a governance/evidence workspace that is strictly read-only display of existing governance/audit/certification/validation/health/version records, with the CLOSED Gate and NOT-CERTIFIED status shown as inert facts and no control surface anywhere.

On operator "authorized", ITRGA will issue **`BUILD_ORDER_UI-007-P01` — Governance Workspace Frame, Route, Data-Source Inventory & Read-Only Guardrails** (per §13), carrying R-1…R-8 and the P01 named-test anchors. **Separately, ITRGA will (on operator authorization) issue the dedicated TD-UI-POSTCSS-HIGH dependency-remediation Build Order — due before UI-007-P02 (R-5).**

No implementation is authorized by this review. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
