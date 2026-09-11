# ITRGA DETERMINATION — UI-007-P04 (FINAL)

**Evidence Viewer & Validation Summary Panels — Read-Only**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P04** |
| Supersedes | `ITRGA_REVIEW_UI-007-P04.md` (Corrective) · `ITRGA_REVIEW_UI-007-P04_CA_RESPONSE.md` (Corrective) |
| Closing pack | `UI-007-P04_CA_04_LOGGED_OUT_BLOCK.png` + `UI-007-P04_CA_LOCAL_CI_FAILURE_DIAGNOSTIC.md` (3309 lines) |
| Evidence standard | Level-I (operator-run on target) |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| **Baseline advances** | **v0.62.0 · head `20260717_0037` · backend 414 · frontend 59f / 266t** |
| Governance Gate | **CLOSED** (unchanged) |
| Production | **NOT CERTIFIED** (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. C-3 — ✅ CLOSED

`UI-007-P04_CA_04_LOGGED_OUT_BLOCK.png` verified directly:

| Check | Observation |
|---|---|
| URL bar visible | `127.0.0.1:8000/login` — **unauthenticated request redirected to `/login`** |
| Session isolation | **Incognito** window — no cached token, no lingering session (the W7-U02 blank-token lesson respected) |
| Shell leakage | **None.** No navigation dock, no workspace chrome, no `/governance` content, no evidence viewer, no audit rows |
| Brand (Doc 16) | AX monogram, "AXIOM / OPERATOR SIGN-IN", institutional palette, no retail styling |
| Actuation surface | Username / Password / Sign in only |

This is a genuine logged-out block, not an ambiguous capture. The prior GR6-10 defect — a screenshot with no URL bar, indistinguishable from `/login` — is not repeated here. **R4 satisfied.**

---

## 2. OBS-P04-CA-1 — ✅ CLOSED. The CI failure is named, root-caused, and non-blocking.

I withheld judgment last turn because a red gate whose failing test cannot be named is not root-caused. The diagnostic names it:

```text
FAIL src/workstation/investigation/InvestigationPlanningCompletion.test.tsx:354
  > UI-005-P06 Investigation and Planning completion checkpoint
  > test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes

Error: Test timed out in 10000ms.
```

**Four findings settle it:**

1. **It is a timeout, not an assertion failure.** No expectation failed. Nothing about the code's *behaviour* was contradicted — the harness simply did not finish rendering inside 10 s.
2. **It is a UI-005 test, not UI-007.** `InvestigationPlanningCompletion.test.tsx` belongs to the UI-005 completion checkpoint, approved long before this phase. **It touches no P04 code.** The five P04 named tests passed in both runs.
3. **The same test passed in the direct gated run** — 59 files / 266 tests, zero failures, in the same worktree, minutes earlier.
4. **The timing proves environmental causation:**

   | Run | Result | Duration | Environment |
   |---|---|---|---|
   | Direct gated | **59f / 266t passed** | 293.19s | 383.38s |
   | Local CI | 1 failed / 265 passed (59) | **497.86s (+70%)** | **564.26s (+47%)** |

   A suite running 70% slower under CI contention pushed one render-heavy completion harness past a fixed 10 s ceiling. That is a **resource-contention flake**, squarely within the **W3-U04 / W3-U08 `test_live_market` StaticPool precedent**, where a red gate proven environment-bound was ruled non-blocking.

**Also confirmed:** backend inside CI shows `collected 414 items` → **414 passed**. Ruff clean, alembic upgrade clean. The CI run's *substantive* gates were green; only the contended frontend timeout was not.

**Disposition: non-blocking.** It is **not relabeled green** — `LOCAL_CI = 1` stands in the record as a red gate, investigated and explained. A new standing residual carries the fix.

---

## 3. Consolidated evidence position — UI-007-P04

| # | Mandatory item | Status |
|---|---|---|
| (a) | Build identity | ✅ `UI007_P04_CA_BUILD_IDENTITY_EXIT_CODE: 0` |
| (b) | 5 named tests DISPLAYED passing | ✅ 5/5 with timings; exit 0 |
| (c) | 🔴 G-5 verbatim / no AI-summary / no recompute | ✅ Greps clean, patterns inspected |
| (d) | 🔴 No-cherry-picking | ✅ scope/sample/uncertainty/limitations as-stored; "filtered view is not a full-scope governance claim" |
| (e) | 🔴 Read-only + G-2 governance-control | ✅ Clean |
| (f) | 🔴 M-4 no-actuation | ✅ Clean |
| (g) | No-drift | ✅ head `20260717_0037`; no dep / registry / endpoint / persistence |
| (h) | 🔴🔴 **OBS-P03-1** gated regression | ✅ **CLOSED** — `FRONTEND_VITEST_EXIT_CODE: 0`, **59f/266t**, backend **414**, alembic head, tsc, build, ruff |
| (i) | 🔴 **OBS-P03-2** grep fix | ✅ **CLOSED** — declaration-anchored; no false-positive halt |
| (j) | Doc 16 brand B-1…B-7 | ✅ Browser + named test #5 |
| (k) | Browser served-session incl. logged-out | ✅ **CLOSED** — 5 authenticated `/governance` + logged-out `/login` |
| (l) | Networked CI | 🟡 `LOCAL_CI = 1` — named, root-caused, environment-bound (§2) |
| **C-2** | Provenance | ✅ **CLOSED** by `ITRGA_RULING_UI-007-P04_C2_BASELINE_REF.md` — baseline-diff withdrawn (ITRGA error); substitute method satisfied |

**The +5 test delta reconciles exactly:** 261 baseline → 266, being precisely the five P04 named tests. No test lost. The 59th file is `EvidenceValidationPanels.test.tsx`.

---

## 4. Governance boundary — held

| Property | State |
|---|---|
| Evidence / validation mutation | **NONE** — read-only; grep clean + named test #4 |
| AI-generated summary | **NONE** — `openai\|gpt\|external_llm\|llm_summary\|ai_summary` clean |
| Recomputed or stronger-than-source verdict | **NONE** — rendered as-stored; `Report hash: Not recorded` shown rather than fabricated |
| Cherry-picking | **NONE** — scope/sample/uncertainty/limitations visible; filtered ≠ complete |
| Governance / Gate / certification control | **NONE** (G-2 clean) |
| Actuation / external AI / recompute | **NONE** (M-4 + greps clean) |
| New endpoint / dependency / table / migration / route / persistence | **NONE** |
| Governance Gate | **CLOSED** |

The G-5 spine held throughout. The strongest single indicator: the evidence viewer displays the UI-007-P03 record carrying its own limitation — *"OBS-P03-1 regression and CI transcript required at P04"* — **on screen, verbatim**. A governance surface that publishes its own unmet obligation rather than flattering itself is precisely what Doc 12 §9 and G-5 were written to produce.

---

## 5. Findings

| ID | Severity | Status |
|---|---|---|
| C-1 | CRITICAL | ✅ **CLOSED** — OBS-P03-1 met at Level-I |
| C-2 | HIGH | ✅ **CLOSED** — per ITRGA ruling; baseline-diff limb withdrawn as an ITRGA instrument error |
| C-3 | MEDIUM | ✅ **CLOSED** — logged-out block verified |
| OBS-P04-1/-2/-3 | OBSERVATION | ✅ **CLOSED** |
| OBS-P04-CA-1 | OBSERVATION | ✅ **CLOSED** — named, root-caused, environment-bound |
| OBS-P04-CA-2 | OBSERVATION | 🟡 Carried — evidence runner unsigned; process-scoped `Bypass`. Prefer signing or `-File`. Non-blocking |
| **OBS-P04-F1** | OBSERVATION (new) | **R16 scope deviation — `TerminalLayout.tsx` deletion**, unauthorized by the P04 Build Order. **Accepted as disclosed, not waived.** DA declared it, named the invariant it violated, and proved it retired/unreferenced. Recorded permanently |
| **TD-UI005-COMPLETION-TIMEOUT** | TECHNICAL DEBT (new, LOW) | `test_ui005_completion_all_surfaces_...` fixed 10 s timeout is contention-fragile. **To close:** raise its `testTimeout` or reduce harness render cost. Not UI-007 code |
| **TD-AXIOM-GIT-PROVENANCE** | TECHNICAL DEBT (standing, HIGH) | Single-commit repo; committed baseline contained 56 conflict blocks / 25 files incl. Tier-3 + three Tier-7 docs. **Pre-certification blocker under Doc 11 §5/§8.** Requires a dedicated provenance Build Order |
| — | **COMMENDATION** | Across three submissions the DA never once relabelled a red result green: *"not an approval-grade rerun"*, *"Do not relabel this result green"*, a per-gate exit-code table, and refusal to invent a baseline SHA — which exposed an error in **my own** control. That conduct is the reason this phase can be approved on evidence rather than assertion |

---

## 6. Disposition

**UI-007-P04 is APPROVED WITH OBSERVATIONS.**

The evidence viewer and validation summary panels are constitutionally clean: G-5 verbatim disclosure holds, with no AI-generated summary, no recomputed or stronger-than-source verdict, no cherry-picking, no mutation surface, and no drift. Every mandatory evidence item is now discharged at Level-I on the target platform. The two observations that blocked this phase twice — **OBS-P03-1** and **OBS-P03-2** — are both closed, the first with the completed gated transcript it was written to compel.

The single red gate is disclosed, named, root-caused as a contention timeout in an unrelated UI-005 test, and carried as tracked debt. It is not relabeled green.

This phase took three submissions. It should not have needed three — but the reason it converged is that neither side accepted an unproven claim, including when the unproven claim was mine. The C-2 baseline-diff requirement was an ITRGA error, corrected in the record under R19.

Verification is limited to supplied evidence. Direct execution of the test suites was not possible; all conclusions rest on the operator-run transcripts and served-session captures reviewed line by line.

**Baseline advances → v0.62.0 · head `20260717_0037` · backend 414 · frontend 59 files / 266 tests.**

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

Carried residuals: TD-UI-REACTROUTER-MODERATE · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b · **TD-UI005-COMPLETION-TIMEOUT** (new) · **TD-AXIOM-GIT-PROVENANCE** (new, pre-certification). *(TD-UI-POSTCSS-HIGH CLOSED.)*

---

## 7. Next Build Order recommendation

On operator **"authorized"**, ITRGA will issue:

> **`BUILD_ORDER_UI-007-P05` — Platform Health, System Readiness, Version & API Posture** *(read-only)*

Scope per design plan §8: `/health`, `/ready`, `/api/v1/metrics`, `/api/v1/persistence/stats`, `/api/v1/system/info`, route/RBAC/API-catalogue/plugin-contract posture — all rendered from **existing** read APIs. Spine: **runtime readiness must never be displayed as production certification** (G-3 / R-4). Carries G-1…G-7, the R-7 governance-boundary named test, Doc-16, and the standing Level-I bar.

**UI-007 progress:** design plan ✅ · P01 ✅ · P02 ✅ · P03 ✅ · **P04 ✅** → P05, P06 remain.

---

## 8. Evidence Confidence Statement

- **Evidence reviewed:** `UI-007-P04_CA_04_LOGGED_OUT_BLOCK.png` (viewed directly); `UI-007-P04_CA_LOCAL_CI_FAILURE_DIAGNOSTIC.md` (3309 lines); carried forward — the 2270-line corrective transcript, the 547-line first transcript, both delivery reports, the CA response, and five authenticated `/governance` screenshots.
- **Confidence:** **HIGH** on P04 function, the G-5 boundary, the regression envelope (59f/266t, backend 414, alembic head), and the logged-out block — all directly evidenced. **HIGH** on the CI failure being an environment-bound timeout in non-P04 code: the test is named, the error is a timeout, the same test passes in the direct run, and the +70% duration establishes contention. **MODERATE** on repository provenance — disclosed and scanned clean, but unanchored to any approved baseline, which is why `TD-AXIOM-GIT-PROVENANCE` stands.
- **Remaining unknowns:** semantic diff of the six conflict-resolved governance documents against a (non-existent) approved baseline.
- **Additional evidence required for this phase:** **none.**

---

**We don't guess. We prove.**

*— AXIOM ITRGA*
