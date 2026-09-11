# BUILD ORDER — UI-007-P06

**UI-007 Completion Checkpoint** — *(Proof unit · the final UI-007 phase)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P06 — Completion Checkpoint (LAST phase)** |
| Predecessor verdict | `ITRGA_REVIEW_UI-007-P05_FINAL.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-1…G-7)/§8 (P06), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8, esp. **R-6**), Doc 11, Doc 16 Part XIV |
| Baseline of record | **v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 60f / 271t** |
| Governance Gate | **CLOSED** (must remain closed) |
| Production | **NOT CERTIFIED** (must remain, and must be displayed as such) |
| On approval | 🏛️ **UI-007 — GOVERNANCE & EVIDENCE WORKSPACE COMPLETE** |

**Motto: "We don't guess. We prove."**

---

## 1. Nature of this phase

**P06 is a PROOF unit, not a feature unit.** Its deliverable is workstream-wide evidence that the six surfaces built across P01–P05 form one coherent, constitutionally inert governance workspace.

The thesis to be proven is a single sentence from the design plan §8:

> **"Governance is visible without becoming governable from the UI."**

Everything below exists to test that claim across the *whole* surface at once — not phase by phase, where a gap between phases could hide.

**No new capability.** Adding any feature at a completion checkpoint is scope expansion (R16) and will be treated as a finding.

---

## 2. Scope

### IN scope
1. **Completion evidence only** — whole-surface proofs spanning P01…P05.
2. **Browser end-to-end workflow** — a single authenticated pass through every UI-007 surface, plus the logged-out block.
3. **R-6 raw-psql audit-verbatim proof** (second mandated cadence after P03).
4. **Doc 16 validation** across the completed workspace.
5. **Full regression** and docs/register reconciliation.

### OUT of scope — do NOT build
- **Any new surface, panel, control, field, filter, or capability.**
- Any new backend endpoint / service / table / migration / dependency / route / persistence (G-7).
- Any governance / audit / Gate / certification / validation mutation (G-1…G-4); actuation (G-6/M-4); external AI; recompute.
- Remediation of `TD-AXIOM-GIT-PROVENANCE` — it requires its own Build Order. **Disclose it; do not fix it here.**

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui007_completion_governance_audit_evidence_health_and_version_are_discoverable`
2. `test_ui007_completion_all_governance_surfaces_are_read_only_and_inert`
3. `test_ui007_completion_no_actuation_recompute_external_ai_gate_or_certification_control`
4. `test_ui007_completion_verbatim_no_cherry_picking_and_residual_disclosure_hold`
5. `test_ui007_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold`

---

## 4. 🔴 R-6 — Raw-psql audit-verbatim proof (the keystone)

Mandated at P03 and again here. Audit is read-only display, so **no save→SELECT persistence-capture is owed** — this is a **verbatim-render** proof:

- Raw `psql SELECT id, category, action, actor, resource_type, resource_id, details->>'reason_code', created_at FROM audit_events` — **≥1 row, including ≥1 `*_REFUSED` row**.
- The **served UI renders the same rows verbatim** — screenshot beside the psql output.
- **Use existing rows only.** No audit event may be created to manufacture evidence.
- **No inference:** a `*_REFUSED` code renders as the stored refusal, never reinterpreted as an authorization path.

The P03 proof used `PLUGIN_CONTRACT_IMPORT_REFUSED` (audit id `055e3295-…`). Re-proving it at completion confirms the constitutional refusal trail is still surfaced honestly at the end of the workstream.

---

## 5. Mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL standard. **Use the v2.0.0 runner** — per-gate exit-code sentinels, terminal summary, guarded script blocks so a `throw` halts rather than falling through.

- **(a) Build identity** — delivery report + transcript header proving the pack is OF UI-007-P06. *(Verify before sending: `Select-String -Path OPERATOR_RESULTS.md -Pattern 'UI007_P06'` must return hits.)*
- **(b) 5 named completion tests DISPLAYED passing** by name.
- **(c) 🔴 R-6 raw-psql audit-verbatim proof** per §4, including a `*_REFUSED` row and the matching served-UI screenshot.
- **(d) 🔴 Whole-surface no-governance-mutation / Gate / certification-control proof** — G-2 grep (`open_gate|allow_execution|gate.*toggle|certify|mark_ready|approve_production|waive|risk_accept`) across **all** UI-007 source files, CLEAN.
- **(e) 🔴 Whole-surface no-actuation proof** — M-4 extended grep including ops-actuation terms (`restart|redeploy|drain|flush|reset_metrics|clear_cache|rerun_migration|trigger_health`), CLEAN.
- **(f) 🔴 Whole-surface no-recompute / no-external-AI proof** — CLEAN.
- **(g) 🔴 Verbatim + no-cherry-picking + residual disclosure hold** — evidence/validation records as-stored; scope/sample/uncertainty/limitations visible; **all standing residuals disclosed at honest severity, including `TD-AXIOM-GIT-PROVENANCE` as OPEN·HIGH pre-certification blocker.** A green-only completion surface is cherry-picking under G-5 ⇒ Corrective.
- **(h) 🔴 Runtime ≠ certification still holds (H-1 carried from P05)** — `Production NOT CERTIFIED` / Doc 11 HELD visible; forbidden-label grep CLEAN. **A completion checkpoint must not imply the platform became certified by completing.**
- **(i) No-drift** — `alembic current` = `20260717_0037`; manifests unchanged (no new dependency); no new endpoint (declaration-anchored grep, `governance_gate.py` excluded); no route/registry change; no persistence.
- **(j) Full regression** — gated **`FRONTEND_VITEST_EXIT_CODE: 0`**, frontend **≥60f/271t no test lost** (print full totals); backend `pytest -q` **≥414 passed** with `BACKEND_PYTEST_EXIT_CODE: 0`; ruff; tsc; build.
- **(k) 🔴 Doc 16 B-1…B-7** across the completed workspace — palette, `--font-mono` numerics, no hardcoded colour in production TSX, unified iconography, institutional-not-retail, **never colour alone**.
- **(l) 🔴 UI-001 / UI-002 integration** — `/governance` mounts in the single UI-001 shell; UI-002 navigation/breadcrumb/palette/switcher remain registry-consistent; **no second shell, no page-specific navigation**.
- **(m) Browser end-to-end** — one authenticated pass across **all** UI-007 surfaces (governance frame · governance status · Gate CLOSED · certification status · residuals · audit explorer + `*_REFUSED` · evidence viewer · validation summaries · health/readiness/version/API posture) showing **no mutation and no actuation control anywhere**; plus the **logged-out `/login` block** (Incognito, URL bar visible — the P05 capture was exemplary).
- **(n) Networked CI** — `LOCAL_CI_EXIT_CODE: 0` (P05 achieved this cleanly); or a named, tracked env-flake disclosed **after** substantive gates are green. **Never relabel a red gate green.**
- **(o) Docs/registers reconciled** — PROJECT_STATE, CHANGELOG, TECHNICAL_DEBT_REGISTER, GOVERNANCE_AMENDMENTS updated for UI-007 completion; **all carried residuals listed with current status.**

---

## 6. 🔴 Residual disposition required at this checkpoint

State each explicitly — status, severity, and disposition. **No silent omissions.**

| Residual | Required treatment |
|---|---|
| **`TD-AXIOM-GIT-PROVENANCE`** | **OPEN · HIGH · pre-certification blocker.** Disclose; do **not** remediate here. Confirm it is displayed on the governance surface |
| `TD-UI005-COMPLETION-TIMEOUT` | Open · low · contention-fragile. Note whether it recurred in this run |
| `TD-UI-REACTROUTER-MODERATE` | Open · moderate · non-blocking |
| `TD-W7-U07-RATE-GUARD` | Deferred — abuse/rate guard not implemented |
| `TD-W6-CI-AUDIT` | Tracked env-flake class; disclose if it recurs |
| `UI-002-P04b` | Independent non-blocking item |
| `OBS-P05-2` | Vite chunk-size advisory, non-failing |
| `OBS-P05-5` | Harness URL/punctuation fix — confirm applied |
| `TD-UI-POSTCSS-HIGH` | **CLOSED / remediated** — display as stored |

---

## 7. Determination rule

A single CRITICAL, any governance/audit/Gate/certification mutation control, any actuation or ops-actuation control, recompute or external AI, a missing or zero-row R-6 raw-psql verbatim proof, cherry-picked completion claims or an undisclosed residual (G-5), any implication that completion equals certification (H-1), new endpoint/dependency/route/persistence, a report-only or halted regression transcript, a wrong-pack transcript, or any unmet mandatory evidence item ⇒ **Corrective Actions Required / Rejected**.

**Only Approved or Approved with Observations permits the UI-007 completion declaration.**

---

## 8. Completion gate — ITRGA-applied on approval

On a passing determination ITRGA will apply the eight-item constitutional validation (per the UI-002/UI-006 precedent) and, if all hold, declare **🏛️ UI-007 — GOVERNANCE & EVIDENCE WORKSPACE COMPLETE**:

constitutional hierarchy respected · no roadmap/scope expansion · no unauthorized business functionality · governance preserved · research-only posture preserved · no execution pathways introduced · UI-001/UI-002 unmodified, single shell · **Governance Gate remains CLOSED**.

**Completion of UI-007 does not constitute production authorization.** Doc 11 certification remains a separate, out-of-band ITRGA track and remains **NOT CERTIFIED** — with `TD-AXIOM-GIT-PROVENANCE` standing as a named pre-certification blocker.

---

## 9. Carried context for the DA

- The P05 evidence pattern was correct — keep it: verified-token capture with HTTP-200 assertion before authenticated calls; per-gate exit table; terminal `COMPLETED_CLEAN` / `WITH_FINDINGS` sentinel; token never printed.
- **Isolate URLs in harness prompts** (OBS-P05-5) — the trailing-period defect cost a full cycle.
- Do not re-run P05's proven gates as new work; this checkpoint's regression covers the current state.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
