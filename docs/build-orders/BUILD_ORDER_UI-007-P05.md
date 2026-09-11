# BUILD ORDER — UI-007-P05

**Platform Health, System Readiness, Version & API Posture** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P05** |
| Predecessor verdict | `ITRGA_REVIEW_UI-007-P04_FINAL.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-3/G-6/G-7)/§8 (P05), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8, esp. **R-2 / R-4 / R-7**), Doc 11, Doc 16 |
| Baseline of record | **v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 59f / 266t** |
| Governance Gate | **CLOSED** (must remain closed) |
| Production | **NOT CERTIFIED** (must remain, and must be displayed as such) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Render **platform health, runtime readiness, metrics, persistence statistics, version, and route/API/plugin posture** as read-only operations evidence on the existing `/governance` workspace.

**The spine of this phase is G-3 / R-4: runtime readiness is NOT production certification.** A green `/health` and a passing `/ready` prove a process is running. They do not prove the platform is fit for production — that determination belongs exclusively to **Doc 11**, out-of-band, and it currently reads **NOT CERTIFIED**. This is the one phase where a careless label could imply the platform is production-ready. **It must not.**

### IN scope

1. **Health & readiness display** — `/health`, `/ready` rendered as-returned.
2. **Metrics & persistence stats** — `/api/v1/metrics`, `/api/v1/persistence/stats` as-returned.
3. **Version & system info** — `/api/v1/system/info` (platform version, alembic head) verbatim.
4. **Posture inventory** — route inventory, RBAC permission vocabulary, API catalogue, plugin contracts, rendered from **existing** W7 read endpoints, disclosing **no** Gate/dynamic-plugin/actuation capability.
5. **Explicit runtime-vs-certification separation** — a visible, unambiguous statement that runtime readiness ≠ production certification, with Doc 11 status shown as **NOT CERTIFIED**.
6. **Readiness dispositions (R-4)** — W7-U07 dispositions from **existing governance records or existing code constants**, verbatim.

### OUT of scope — do NOT build

- Completion checkpoint (**P06**).
- **Any new backend endpoint, service, table, migration, dependency, route, or governance-state persistence (G-7).** A new health/readiness/certification read route requires separate ITRGA authorization — **not granted** (R-2/R-4).
- Any governance/audit/Gate/certification/validation mutation (G-1…G-4); actuation (G-6/M-4); external AI/LLM; recompute/inference/reclassification.
- **Any restart / redeploy / drain / clear-cache / reset-metrics / re-run-migration / health-check-trigger control.** Operations *evidence*, never an operations *console*.
- Saved-view/filter persistence.

---

## 2. Binding refinements applied

- **R-1** — Enhance existing `/governance`; **no new route**; 14-field registry contract unchanged.
- **R-2 (BINDING)** — **No certification-status backend endpoint.** Certification is an out-of-band Doc 11 governance act; display canonical status only.
- **R-4 (BINDING)** — Readiness dispositions from existing records/constants, **verbatim**; **no new backend read route**.
- **R-7 (SPINE)** — Named governance-boundary test + G-2 grep + M-4 no-actuation grep + no-recompute/external-AI grep.
- **R-8** — Level-I evidence, Doc-16 brand, regression **≥ 59f/266t and backend ≥414**, no test lost, gated exit 0.

---

## 3. 🔴 The honesty requirements (this phase's defining risk)

**H-1 — Runtime readiness must never be styled, labelled, or grouped as production readiness.** No "Production Ready", "All Systems Go", "Certified", "Fully Operational", or green master-status badge implying certification. `/ready` returning OK means *dependencies reachable* — nothing more. **Doc 11 status `NOT CERTIFIED` must be visible on the same surface**, not buried in another panel.

**H-2 — Residuals must be disclosed, not smoothed.** These currently stand and must render honestly if surfaced:

| Residual | Must display as |
|---|---|
| `TD-W7-U07-RATE-GUARD` | Abuse/rate guard **deferred — not implemented** |
| `TD-W6-CI-AUDIT` | Networked CI `npm audit` env-flake **tracked** |
| `TD-UI-REACTROUTER-MODERATE` | **Open**, moderate, non-blocking |
| `UI-002-P04b` | Independent non-blocking item |
| **`TD-AXIOM-GIT-PROVENANCE`** | **NEW — open; pre-certification blocker** |
| `TD-UI-POSTCSS-HIGH` | Closed / remediated (as stored) |

A posture surface that shows only green while `TD-AXIOM-GIT-PROVENANCE` is open would be **cherry-picking under G-5** ⇒ Corrective.

**H-3 — `admin/admin123` must not be displayed as an open vulnerability *or* silently omitted.** Per `ITRGA_VERDICT_W7-U07_FINAL.md` it is **proven rejected under production framing** (`ADMIN_DEFAULT_CREDENTIAL_REJECTED_WITH_INSECURE_DEV_OFF: True`). Render as-stored if surfaced — no stronger and no weaker.

**H-4 — No secrets or PII.** No connection strings, tokens, credentials, or internal hostnames from health/metrics/stats payloads. Redact per §77; prove `SECRET_MARKER_COUNT: 0`.

---

## 4. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui007_platform_health_version_and_readiness_render_existing_read_api_values`
2. **`test_ui007_runtime_readiness_is_not_displayed_as_production_certification`** ← spine
3. `test_ui007_api_route_plugin_posture_discloses_no_gate_dynamic_plugin_or_actuation_capability`
4. `test_ui007_platform_health_contains_no_governance_mutation_gate_or_certification_control`
5. `test_ui007_platform_health_accessibility_and_doc16_brand_hold`

---

## 5. Mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL standard. **Use the v2.0.0 runner pattern** — per-gate exit-code sentinels, a final summary table, and no `$ErrorActionPreference=Stop` halt that truncates later mandatory evidence.

- **(a) Build identity** — delivery report + transcript header proving the pack is OF UI-007-P05.
- **(b) 5 named tests DISPLAYED passing** by name.
- **(c) 🔴 H-1 runtime ≠ certification** — served UI shows readiness and **`Production: NOT CERTIFIED` / Doc 11 HELD** on the same surface; named test #2; grep for forbidden labels (`production.ready|all systems go|certified|fully operational|production_ready`) → **CLEAN** (or justified as as-stored Doc-11 vocabulary).
- **(d) 🔴 H-2 residual honesty** — residuals rendered as stored, **including `TD-AXIOM-GIT-PROVENANCE` as open**; no green-only aggregate.
- **(e) 🔴 Values are as-returned** — for ≥2 surfaces (e.g. `/api/v1/system/info` version + alembic head; `/api/v1/persistence/stats` a count), show the **raw API/curl response beside the rendered UI value** and prove they match. No recompute, no rounding, no derived "score".
- **(f) 🔴 G-2 governance-control grep CLEAN** — `open_gate|allow_execution|gate.*toggle|certify|mark_ready|approve_production|waive|risk_accept`.
- **(g) 🔴 M-4 whole-surface no-actuation grep CLEAN** — plus **ops-actuation** terms: `restart|redeploy|drain|flush|reset_metrics|clear_cache|rerun_migration|trigger_health`.
- **(h) 🔴 No-recompute + external-AI greps CLEAN.**
- **(i) 🔴 H-4 no secrets/PII** — `SECRET_MARKER_COUNT: 0`; no connection string/token/credential/internal hostname in rendered output.
- **(j) No-drift** — `alembic current` = `20260717_0037`; manifests unchanged (**no new dependency**); **no new endpoint** (declaration-anchored grep, `governance_gate.py` excluded — the P04 pattern); no route/registry change; no persistence.
- **(k) Regression** — clean gated **`FRONTEND_VITEST_EXIT_CODE: 0`**, frontend **≥59f/266t no test lost** (print the full totals), backend `pytest -q` **≥414 passed**, `BACKEND_PYTEST_EXIT_CODE: 0`, tsc + build clean.
- **(l) 🔴 Doc 16 B-1…B-7** — palette, `--font-mono` on numerics (versions, counts, latencies, uptimes), no hardcoded colour in production TSX, unified iconography, institutional-not-retail, **never colour alone** (a green dot must carry a text label).
- **(m) Browser served-session** — logged-in `/governance` health/readiness/version/metrics/posture panels + the runtime-vs-certification statement + **no ops-actuation control**; **logged-out `/login` block** (the P04 Incognito pattern was exemplary — repeat it).
- **(n) Networked CI** — `LOCAL_CI_EXIT_CODE: 0` + sentinel; **or** a documented env-flake/known-timeout finding **after** substantive gates are green. If `TD-UI005-COMPLETION-TIMEOUT` recurs, name it and state it is the tracked non-P05 residual. **Never relabel a red gate green.**

---

## 6. Determination rule

A single CRITICAL, **any implication that runtime readiness constitutes production certification (H-1)**, green-only/cherry-picked posture hiding an open residual (H-2/G-5), a recomputed or not-as-returned value, any ops-actuation control, any governance/Gate/certification control, a new endpoint/dependency/route/persistence, a secret/PII leak, a report-only or halted regression transcript, or any unmet mandatory evidence item ⇒ **Corrective Actions Required / Rejected**.

Only **Approved** or **Approved with Observations** authorizes the next Build Order (**UI-007-P06 — Completion Checkpoint**, which will carry the R-6 raw-psql audit-verbatim proof and the whole-surface completion proofs).

---

## 7. Carried context for the DA

- **OBS-P04-F1** (`TerminalLayout.tsx` R16 deviation) is recorded and closed — no action.
- **OBS-P04-CA-2** — evidence runner is unsigned; process-scoped `Bypass` is acceptable. Signing or `-File` invocation preferred, not required.
- **`TD-UI005-COMPLETION-TIMEOUT`** — if the UI-005 completion test times out again under CI contention, name it and move on; it is tracked and not a P05 defect.
- **`TD-AXIOM-GIT-PROVENANCE`** — do **not** attempt to remediate in P05. It requires its own Build Order. **But it must render honestly if the posture surface lists residuals.**

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
