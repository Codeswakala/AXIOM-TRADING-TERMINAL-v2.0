# ITRGA INDEPENDENT REVIEW — W5-U04 (Signal Investigation Workspace)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U04** — Signal Investigation Workspace |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U04.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U04.md` + `uploads/operator results.md` (1,499 lines) + 5 browser screenshots |
| DA-claimed platform | 0.42.0 |
| Review date | 2026-07-17 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.42.0** |
| Confidence | **HIGH** — no-signal-mutation proven by identical before/after row + write endpoints proven absent (405); browser-proven |

> **We don't guess. We prove.** The workspace explains a signal and provably never touches it — before/after rows are identical, and `/emit` + `/override-guardrail` don't exist. Approved.

---

## 1. Bottom line

W5-U04 delivers a read-only Signal Investigation Workspace that **explains** a signal's rationale, guardrail
states, lineage, and linked intelligence reports — and **provably mutates nothing.** Every keystone is met on
target: **no-signal-mutation** (identical before/after row + 4 named tests + write endpoints absent 405);
**presentation-only** (no client recompute); **calibrated confidence, no raw score**; **read-only API
401/200**; **no LLM/dep (R5-2)**; **browser-proven (R5-6)**. No new migration/table/report type; full suite
268; CI exit 0. **APPROVED, CLEAN, no residual.**

---

## 2. No-signal-mutation (keystone) — PROVEN ✅

- **Identical before/after row:** operator captured signal `4326dbf4-…` (state emitted, raw_score 0.987654,
  calibrated_confidence 0.5, rationale, transition history, audit id) **before** investigation, ran it, and
  captured **after** — `Compare-Object` produced **no difference** (byte-identical). Investigation changed
  nothing.
- **Write endpoints ABSENT (above spec):** `POST /signals/history/{id}` → **405**, `…/emit` → **405**,
  `…/override-guardrail` → **405**. There is no signal-write/emit/override endpoint.
- Named tests PASS: `test_signal_investigation_triggers_and_mutates_nothing` (asserts advisory-signal +
  model-artifact row counts, signal snapshot, model `status`, and `advisory_status` all unchanged),
  `..._has_no_signal_write_endpoint`, `..._workspace_has_no_mutation_or_execution_path`,
  `..._reads_require_auth_and_return_persisted_context`. ✅

## 3. Browser (R5-6, mandatory) — complete ✅

Five screenshots on a reachable served session (`localhost:8000`, W5-U04 / v0.42.0):
- **Investigation view** (`/investigate`): "**Research investigation only.** …not a trade instruction, not a
  signal mutation, and not an action surface… AXIOM does not act." + "Investigation reads persisted evidence
  only. It does not change this signal, rerun the model, alter guardrails, or create an instruction."
- Persisted signals list (EMITTED/EXPIRED/WITHHELD/WARNING states); **INVESTIGATION DETAIL** with rationale,
  **"50.0% calibrated confidence"** (calibrated, **no raw score**).
- **Guardrail states** (state reason/domain/calibration/economic/freshness/expiry) + **lineage** (signal id/
  model/version/experiment/feature-set/input hash) + linked validation/report ids.
- **Linked intelligence reports** (correlation/regime/scenario/portfolio-risk/signal-validation, all
  `research_only`).
- **No action controls anywhere**; **logged-out block** → `localhost:8000/login`. No `ERR_CONNECTION_REFUSED`. ✅

## 4. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity | `Test-Path` new page/test/ADR True; v0.42.0 |
| Presentation-only (GR-8) | UI states "no client-side inference / no authoritative recompute"; mutation grep on the page empty |
| No raw score | calibrated only (screenshot + frontend test) |
| Read-only API | unauth **401** / list **200** / detail **200**; no signal write endpoint |
| No assistant summary this unit | correctly stated (R5-1/R5-3/R5-5/R5-7 N/A); W5-U01/U02 safety tests remain in regression |
| **R5-2 no LLM/dep** | collaboration grep no `openai\|anthropic\|transformers\|langchain\|llama`; no new dep |
| **R5-8 grep + gate** | mutation grep empty; wave-wide grep residual = disclaimer text on the page only (benign); broker gate 7 passed; Gate CLOSED |
| No new artifact/migration | head `20260717_0025` unchanged; reads existing APIs only |
| Regression + CI | 35 named collab/investigation tests PASS; backend **268 passed** (264→268, +4), frontend **14 files / 38 tests** (+5); ruff clean; npm audit 0; **CI via Git-Bash → marker + `LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U04) |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 5. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | No-signal-mutation (identical before/after row + 4 named tests + write endpoints 405) ✅ |
| — | — | R5-6 browser (view + rationale/guardrails/lineage/linked reports + calibrated-no-raw-score + no-action + logged-out) ✅ |
| — | — | presentation-only · read-only 401/200 · R5-2 no-LLM · R5-8 grep+gate · 268 tests · CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 6. Disposition & next step

- **W5-U04 — ✅ APPROVED, CLEAN.** Platform **v0.41.0 → v0.42.0**.
- Commendation: the no-mutation keystone is proven the strongest way — an **identical before/after signal row
  (`Compare-Object` empty)** plus **write/emit/override endpoints proven absent (405)** — and the browser set
  is complete with calibrated-confidence-no-raw-score. Every prior lesson held.
- **Next:** ITRGA recommends **W5-U05 — Scenario Comparison Workspace**: compare existing persisted scenario
  reports (W4-U04) read-only; **no scenario generation beyond existing APIs**, uncertainty/provenance visible,
  no guaranteed outcomes; presentation-only; browser evidence mandatory (R5-6); R5-8; assistant summary only if
  grounded/non-actuating/disclaimed/audited (R5-1/R5-3/R5-5/R5-7) + no LLM. On operator authorization ITRGA
  issues `BUILD_ORDER_W5-U05.md`.
- External LLM remains future hard-gated (R5-2). DA does not self-authorize W5-U05, ship an LLM, add an
  actuating tool/execution/order/account linkage, mutate a signal, or open the Gate.

> **We don't guess. We prove.** — ITRGA
