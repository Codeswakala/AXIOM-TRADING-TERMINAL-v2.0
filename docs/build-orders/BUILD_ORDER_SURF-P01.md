# BUILD ORDER — SURF-P01

**Issuing authority:** Independent Technical Review & Governance Authority
**Authorized by:** Operator, 2026-08-16
**Programme:** SURF — Surface the unsurfaced · Phase 1 of 3
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`) + item4 Rev B (`a516c2c1…`)
**Predecessor:** CONV programme — COMPLETE, APPROVED WITH OBSERVATIONS
**Governing documents:** `AXIOM_UI_TRANSFORMATION_BLUEPRINT.md` §5 · turn-56 reframe · Doc 17

---

## 1. OBJECTIVE

Blueprint §5, verbatim:

> **SURF-P01** **Execution Research dock** — simulated runs, fills, ledger entries, experiments, risk reports (13 endpoints). Labelled `SIMULATED · NON-ACTUATING` throughout; T-1 applies with full force.

**This phase changes character from CONV.** CONV re-homed surfaces that already existed. SURF *surfaces capability that is built but not reachable*. The turn-56 reframe is now the primary driver: **if an aspect has already been built, it must be presented in the best possible way.**

---

## 2. VERIFIED STARTING STATE

Established by ITRGA against the base chain. The DA must not restate these as claims.

### 2.1 The backend has 17 endpoints, not 13

`backend/app/api/routes/execution_research.py` — **12 GET + 5 POST**:

| Resource | Endpoints |
|---|---|
| Simulated runs | `GET /simulated-runs` · `GET /simulated-runs/{run_id}` · `GET /simulated-runs/{run_id}/fills` · **`POST /simulated-runs`** |
| Simulated fills | `GET /simulated-fills/{fill_id}` |
| Paper ledger | `GET /simulated-ledger-entries` · `GET /simulated-ledger-entries/{ledger_entry_id}` · **`POST /simulated-ledger-entries`** |
| Risk reports | `GET /execution-risk-reports` · `GET /execution-risk-reports/{report_id}` · **`POST /execution-risk-reports`** |
| Experiments | `GET /execution-experiments` · `GET /execution-experiments/{experiment_id}` · **`POST /execution-experiments`** |
| Analytics reports | `GET /simulated-analytics-reports` · `GET /simulated-analytics-reports/{report_id}` · **`POST /simulated-analytics-reports`** |

The blueprint's figure of 13 is superseded by direct inspection. **This is an inventory correction, not a scope expansion** — see §4 for what is actually in scope.

### 2.2 The frontend reaches almost none of it

```
api/client.ts  →  fetchExecutionResearchBundle()   ← the ONLY execution-research client function
```

The bundle calls `GET /simulated-runs?limit=25`, then `/{run_id}/fills` for **`runs.slice(0, 5)` only**, then list endpoints for ledger, risk reports, experiments and analytics.

**Consequently:**
- **All six detail GETs are unreachable** — `{run_id}`, `{fill_id}`, `{ledger_entry_id}`, `{report_id}` ×2, `{experiment_id}`.
- **All five POSTs have no client function at all** — `grep` returns 0.
- Fills are silently truncated at the first 5 runs.

### 2.3 The existing page

`frontend/src/pages/ExecutionResearchPage.tsx` — 436 lines, **0 `data-testid`**, one endpoint (the bundle).

Capability groups present: Execution Research Workspace · Investigation Context · Persisted SIMULATED artifacts · Simulated Runs · Simulated Fills · Paper Research Ledger · Risk Research Reports · Replay Experiments · Analytics & Comparison · plus per-item **Replay scope · Assumptions · Limitations · Request evidence · Pre-registration plan · As-of window · Replay lineage · Included scope · Metrics**.

`route: "/execution-research"`, `navigationCategory: "Plan"`, `Component: ExecutionResearchPage`.

---

## 3. 🔴 T-1 APPLIES WITH FULL FORCE — THE DEFINING CONSTRAINT

This is the closest surface in the platform to execution. It is **simulated, non-actuating research** and must be unmistakably presented as such.

`backend/tests/test_execution_research_safety.py` enforces the boundary today:

```
test_governance_gate_remains_closed_for_wave6
test_null_or_simulated_broker_refuses_connect_when_gate_closed
test_null_or_simulated_broker_refuses_execute_when_gate_closed
test_broker_logic_contained_in_external_integration
test_execution_research_has_no_live_broker_sdk_or_credentials
test_wave6_bright_line_grep_no_live_execution_path
```

Forbidden packages: `metatrader`, `mt5`, `ccxt`, `ib_insync`, `oandapy`, `alpaca`, `binance`, `openai`, `anthropic`, `transformers`, `langchain`, `llama`. Forbidden runtime strings: `api_key`, `secret_key`, `password`, `token`, `credential`.

**Note: this suite does not currently pin a frontend path.** The CONV-phase guards (`test_signal_investigation_workspace.py`, `test_research_management.py`) do pin frontend files and were re-pointed with non-vacuity assertions.

**M1 — Add a frontend T-1 guard.** Extend `test_execution_research_safety.py` with a source-inspection test over the new execution-research UI module, asserting:
- **non-vacuity** — a positive assertion that the file contains the surface (the item-4 pattern: `assert "simulated" in text` or similar anchor text),
- absence of `place_order`, `submit order`, `go live`, `connect broker`, `broker_account`, `order_ticket`, `account_id`, `execute_order`, `live_trade`.

Without this, the phase's most execution-adjacent surface is the only major surface with **no frontend constitutional guard**.

**M2 — `SIMULATED · NON-ACTUATING` labelling throughout.** Every region rendering runs, fills, ledger entries or analytics carries the label. Not once in a header — **at each artifact group**. The existing page's per-item `Limitations`, `Assumptions` and `Replay scope` sections must survive; they are the honesty surfaces of this domain.

**M3 — No execution affordance, real or implied.** No button, label, or icon may suggest order placement, broker connection, or going live. Simulated runs are *research artifacts*, not trades.

---

## 4. SCOPE — WHAT IS IN, WHAT IS NOT

### IN SCOPE

**S1 — Re-home the surface into the terminal.** `/execution-research` follows the CONV pattern: a dock tab, overlay, or stage view. The DA selects and states reasoning. Given nine capability groups and per-item detail, a **bottom-dock tab or full-height surface** is likely; the right dock at 320 px is almost certainly too narrow. **A disposition note is not required.**

**S2 — Surface the six unreachable detail GETs.** This is the phase's *surfacing* mandate. Selecting a run, fill, ledger entry, risk report, experiment or analytics report should retrieve and present its detail record. Currently the platform can only show what the list endpoints return.

**S3 — Remove the silent fills truncation** (`runs.slice(0, 5)`), or **disclose it explicitly in the UI**. A truncation the operator cannot see is a quiet inaccuracy — the `OBS-CONV2-1` family. Either fetch on demand for the selected run, or state "showing fills for the first 5 runs" verbatim.

**S4 — `data-testid` across all regions.** Baseline 0. CONV deliveries: 8, 10, 20, 17, 23, 20.

### 🔴 NOT IN SCOPE — THE FIVE POST ENDPOINTS

**Do not add client functions for the five POSTs. Do not add UI that creates simulated runs, ledger entries, risk reports, experiments or analytics reports.**

Reasons, in order of weight:

1. **Blueprint §5 scopes SURF-P01 to surfacing existing capability**, not adding write paths.
2. Every CONV write surface I approved — item 3 preferences, item 4 collections/tags — was **re-homing an existing, already-governed write**. Creating a *new* write path into the execution-research domain is a different act requiring its own authorization.
3. **This is the execution-adjacent domain.** A "create simulated run" control is exactly the affordance that, misread or later modified, edges toward T-1. It warrants a dedicated Build Order with its own guard design, not an incidental inclusion.

**If the DA judges a POST surface necessary to present a capability honestly, stop and report.** Do not implement it. That is an Operator decision.

### ALSO OUT OF SCOPE

SURF-P02 (Alerts / `TD-061`) · SURF-P03 (governance & platform) · DATA · CHART · POLISH · the 687 kB bundle (POLISH-P01) · brand mark (`F-BRAND-1`, GA-173) · backend endpoint, schema or model changes of any kind.

---

## 5. STANDING REQUIREMENTS

**R1 — Preserve every capability.** The §2.3 inventory is the acceptance checklist. `Limitations`, `Assumptions`, `Replay scope`, `Pre-registration plan`, `As-of window`, `Replay lineage`, `Included scope`, `Request evidence` are constitutional honesty surfaces — not decoration.

**R2 — `/execution-research` must not 404.** Follow the established redirect pattern (`ResearchManagementRedirect` :63 is the current model).

**R3 — No fabricated values.** With 17 endpoints the temptation to synthesise a count, a P&L figure or a fill price is highest here. **A simulated artifact with no data renders explicit absence** — the `"—"` and *"No … returned."* discipline. Never a plausible-looking number.

**R4 — Independent per-source degradation.** Multiple fetches; one failure must not blank the surface. The item-4 M5 pattern — per-source state with genuine loaded counts — is the standard to match.

**R5 — RBAC not widened.** 16/16 `protectedWorkspace()` wrappers, `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`, no per-entry override.

**R6 — Suite green.** Current verified: **775 frontend / 415 backend = 1,190**. New surface requires new tests. **Never delete a failing test to reach green.**

**R7 — `npm ci` before `tsc -b`.**

**R8 — Deletion discipline.** Delete `ExecutionResearchPage.tsx` and its test in the same cycle once superseded, after re-pointing dependants. Check for coupled suites first — CONV items 5 and 6 each had six.

---

## 6. DELIVERY REQUIREMENTS

**Transport — four consecutive hash-reconciled deliveries; repeat exactly.** Neither authority commits to the repository; that is Operator-only. The verified patch is the artifact of record.

```bash
git diff <base> > surf_p01.patch
git apply --check surf_p01.patch ; echo "exit=$?"
sha256sum surf_p01.patch
```

Inline in the message body · **LF endings, terminating newline** · **state the base chain explicitly**.

**Report must contain:**

1. Chosen home + reasoning.
2. Capability disposition table — every §2.3 group mapped.
3. **Endpoint coverage table** — all 17, each marked `surfaced` / `already surfaced` / `out of scope (POST)`.
4. M1 frontend T-1 guard: the assertion text, its non-vacuity anchor, and confirmation it passes.
5. M2 labelling: where `SIMULATED · NON-ACTUATING` appears.
6. S3 disposition: truncation removed, or the disclosure text used.
7. Raw console transcripts — vitest, tsc -b, vite build, pytest.
8. **Level-I captures attached** — self-contained HTML, base64 PNGs, incl.:
   - the surface populated, showing `SIMULATED · NON-ACTUATING` labelling,
   - a **detail record** retrieved via one of the six newly surfaced GETs,
   - an **empty-state capture scrolled to the empty region**,
   - a **single-seam failure** showing independent degradation,
   - the `/execution-research` redirect landing.
9. **Interaction trace** for any click-dependent affordance — the item-4 Playwright `elementFromPoint` method.
10. Exact wording: *deleted* / *relocated* / *copied* / *extended* / *surfaced*.

---

## 7. ACCEPTANCE

1. Every §2.3 capability present and reachable.
2. Six detail GETs surfaced and demonstrably retrieving records.
3. Fills truncation removed or explicitly disclosed.
4. **Zero POST client functions added; no create affordance anywhere.**
5. M1 frontend T-1 guard present, non-vacuous, passing.
6. M2 labelling at every artifact group.
7. M3 no execution affordance real or implied.
8. `/execution-research` resolves.
9. `data-testid` across all regions.
10. R3 absence rendered as absence; no fabricated values.
11. R4 independent degradation.
12. Suite green ≥ 1,190; nothing deleted to force green.
13. `tsc -b` clean; `vite build` succeeds.
14. RBAC not widened.
15. `ExecutionResearchPage.tsx` + test deleted once superseded.
16. Captures attached incl. detail record, scrolled empty state, seam failure; interaction trace supplied.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This Build Order authorizes **SURF-P01 only**. It is not authorization for SURF-P02, SURF-P03, DATA, CHART or POLISH.
**No implementation beyond this scope. The five POST endpoints are explicitly excluded.**

**We don't guess. We prove.**
