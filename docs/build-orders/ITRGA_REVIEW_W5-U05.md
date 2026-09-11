# ITRGA INDEPENDENT REVIEW — W5-U05 (Scenario Comparison Workspace)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U05** — Scenario Comparison Workspace |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U05.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U05.md` + `uploads/operator results.md` (1,373 lines) + 4 browser screenshots |
| DA-claimed platform | 0.43.0 |
| Review date | 2026-07-17 |
| **VERDICT** | **🟡 CONDITIONAL APPROVAL — C-1: a genuine ≥2-scenario comparison was NOT exercised on target (DB had 1 scenario). Safety + core-read function APPROVED.** |
| Confidence | **HIGH** on safety (no-generation proven); the gap is that the workspace's headline function (compare ≥2) is unproven on target |

> **We don't guess. We prove.** No-generation is proven and the safety line holds — but the DB had only ONE scenario, so a real side-by-side comparison was never shown. That core function must be proven before clean approval.

---

## 1. Bottom line

The safety posture is fully proven: **no scenario generation** (BEFORE 1 = AFTER 1; `/generate`, POST,
`/compare` endpoints **405/absent**; 5 named tests PASS), read-only API (401/200), no new migration/table/
report type, no LLM, no execution/action controls, hypothetical/not-guaranteed framing on screen. **But the
target DB contained only ONE `scenario_report`** (`SCENARIO_REPORT_COUNT: 1`) — so the precondition guard
correctly threw, the browser shows *"At least two persisted scenarios are required for comparison,"* and **a
genuine ≥2 side-by-side comparison — the workspace's entire purpose — was never exercised on target.** The
unit tests cover it with fixtures, but operator target + browser evidence does not.

Per proportionality (R13): the **risk items are all proven**, so this is **CONDITIONAL** (not withheld) — the
core function must be shown on target with ≥2 real scenarios before clean approval and the version bump.

---

## 2. What is PROVEN ✅

### 2.1 No-scenario-generation (keystone) — proven
- `SCENARIO_COUNT_BEFORE: 1` → (comparison reads) → `SCENARIO_COUNT_AFTER: 1` — comparison created no new
  `scenario_reports` row.
- API: `SCENARIO_POST_STATUS:405`, **`SCENARIO_GENERATE_STATUS:405`**, `SCENARIO_COMPARE_POST_STATUS:405` — no
  write/generate/compare-POST endpoint exists (above-spec absence proof).
- 5 named tests PASS: `..._reads_existing_reports_and_creates_no_rows`,
  `..._api_auth_read_only_and_no_generate_endpoint`, `..._has_no_generation_or_execution_path`,
  `..._no_new_migration_file`, `..._uses_current_time_only_for_test_fixture`.
- **The DA's precondition guard worked exactly as designed** — it threw ("Need at least two existing
  scenario_reports rows… W5-U05 itself does not generate scenarios") rather than fabricating a second scenario.
  That is the correct, honest behavior. ✅

### 2.2 Safety + read function
- Read-only API unauth **401** / list **200** / detail **200**; no new migration (head `20260717_0025`).
- Presentation-only (grep no generation/compute call on the page); **no raw score** (test); no execution/action
  controls; **R5-2** no LLM/dep; Gate CLOSED; no D-W2-001 breach.
- Backend **273 passed** (268→273, +5), frontend **15 files / 43 tests** (+5), ruff clean, npm audit 0;
  **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → marker + `LOCAL_CI_EXIT_CODE: 0`**
  (transcript W5-U05). No assistant summary this unit (correctly stated). ✅

### 2.3 Browser (partial)
Screenshots show the `/compare-scenarios` view rendered on a served session, the "Hypothetical comparison
only… not a prediction, not guaranteed… AXIOM does not act" disclaimer, a single scenario's assumptions +
uncertainty (`-2.01% to -1.99% · n=5 · historical_volatility_band`) + provenance/source ids + limitations
(`not_a_prediction, not_a_trade_instruction, …`), and the logged-out block. **But the SIDE-BY-SIDE panel reads
"At least two persisted scenarios are required for comparison"** — only one scenario exists, so the actual
comparison is not shown.

---

## 3. Condition to close

### C-1 (must close) — exercise a genuine ≥2-scenario comparison on target
The workspace's headline function — **comparing two or more existing scenarios side by side** — was not
demonstrated because the target DB held only 1 `scenario_report`. To close: on the target, ensure **≥2
existing persisted scenario reports** are present (via prior W4-U04-style authorized seeding of the
`scenario_reports` table — **not** by any W5-U05 generation path, which correctly does not exist), then:
1. re-run the before/after count proof with **BEFORE ≥2 = AFTER ≥2** (still no new rows), and
2. supply a **browser screenshot showing two scenarios rendered side-by-side** (both with assumptions +
   uncertainty + provenance + not-guaranteed framing).

*Why not waived:* the safety controls are proven, but a comparison unit that has never compared two things is
functionally unproven on target (the W4-U07 C-1 precedent — a surface's core purpose must be shown on screen,
not only in fixtures). The gap is data-availability, not a defect — the code is correct and the no-generation
guard behaved perfectly.

---

## 4. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | **MEDIUM** | Genuine ≥2-scenario comparison not exercised on target (DB had 1 scenario; browser shows "need ≥2"); core function unproven on target | **Condition — seed ≥2 existing scenarios, re-run before/after + side-by-side browser shot** |
| — | — | No-generation (BEFORE=AFTER, endpoints 405, 5 tests), read-only API, no raw score, no LLM, gate-closed, 273/15·43, CI exit 0, framing on screen | ✅ proven |

**No CRITICAL. No governance/safety breach.** One core-function evidence condition ⇒ **CONDITIONAL APPROVAL**
(not withheld — every risk item is proven; the gap is target-data availability for the headline feature).

---

## 5. Disposition & next step

- **W5-U05 — 🟡 CONDITIONAL APPROVAL.** Safety + read function **APPROVED**; the no-generation keystone is
  proven. Platform advances to **v0.43.0 on closure of C-1** (until then v0.42.0 remains the version of record
  for ITRGA purposes).
- **To close:** a short re-run — seed ≥2 existing scenario reports (prior-wave path, not generation), show
  BEFORE ≥2 = AFTER ≥2, and a browser shot of a real two-scenario side-by-side comparison. No re-implementation.
  On that, ITRGA issues the FINAL verdict, advances to v0.43.0, and (on operator authorization) issues
  `BUILD_ORDER_W5-U06.md` (Inert Trade Planning Workspace).
- Commendation: the **precondition guard did exactly the right thing** — it refused to run a comparison without
  ≥2 real records rather than generate a second scenario, and the endpoint-absence proof (`/generate` 405) is
  above spec. The gap is purely that the operator's DB wasn't seeded with a second scenario for the run.
- DA does not self-approve, self-advance the version, self-close the condition, build W5-U06, ship an LLM,
  generate a scenario, or open the Gate.

> **We don't guess. We prove.** — ITRGA
