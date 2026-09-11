# ITRGA DETERMINATION — UI-007-P04 (Corrective Response)

**Evidence Viewer & Validation Summary Panels — Corrective Re-submission**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P04 — corrective response** |
| Predecessor determination | `ITRGA_REVIEW_UI-007-P04.md` — Corrective Actions Required (C-1/C-2/C-3) |
| Pack | `DELIVERY_REPORT_UI-007-P04_CA_RESPONSE.md` (170 lines) + `OPERATOR_RESULTS.md` (**2270 lines**, runner v2.0.0) |
| Evidence standard | Level-I (operator-run on target) |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 58f/261t |
| **DETERMINATION** | 🟡 **CORRECTIVE ACTIONS REQUIRED (C-1 CLOSED · C-2 PART-CLOSED, ITRGA-BLOCKED · C-3 OPEN)** |
| Baseline | **UNCHANGED — v0.62.0** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Transcript is NEW, not a re-attachment | **2270 lines** vs the prior 547; `UI007_P04_CA_EVIDENCE_STARTED: 2026-07-28T13:51:23` vs prior `09:50:30`; `UI007_P04_CA_RUNNER_VERSION: 2.0.0` | ✅ |
| Repo root anchored | `UI007_P04_CA_REPO_ROOT: C:\Users\Swakala\.vscode\AXIOM\axiom` | ✅ |
| Build identity gate | `UI007_P04_CA_BUILD_IDENTITY_EXIT_CODE: 0` | ✅ |
| Cites this ITRGA determination | `ITRGA_REVIEW_UI-007-P04.md` — Corrective Actions Required | ✅ |
| Findings accepted without relabeling | §1 accepts C-1/C-2/C-3 and all three OBS explicitly | ✅ |

**Pack confirmed OF the UI-007-P04 corrective response.** This is a genuine re-run, not a re-submission of the failed transcript.

---

## 2. ✅ C-1 — **CLOSED**. OBS-P03-1 is met.

This is the finding that blocked the phase twice. It is now discharged at Level-I on target.

| Gate | Evidence (line) | Verdict |
|---|---|---|
| **Full-suite sentinel** | **`FRONTEND_VITEST_EXIT_CODE: 0`** (L546) — printed as output, not a command echo | ✅ |
| **Full-suite totals** | **`Test Files 59 passed (59)` / `Tests 266 passed (266)`** (L797–798), duration 293.19s | ✅ |
| **No test lost** | 266 ≥ 261 baseline; **+5 = exactly the P04 named tests**. Reconciles cleanly | ✅ |
| **5 named tests** | All five DISPLAYED passing with timings; `UI007_P04_CA_NAMED_VITEST_EXIT_CODE: 0` (L247) | ✅ |
| **Backend** | **`414 passed, 1919 warnings in 645.78s`** (L1175); `BACKEND_PYTEST_EXIT_CODE: 0` (L956) | ✅ |
| **Alembic on target PostgreSQL** | **`20260717_0037 (head)`**; `UI007_P04_CA_ALEMBIC_CURRENT_EXIT_CODE: 0` (L1181) | ✅ |
| **TypeScript** | `UI007_P04_CA_TYPESCRIPT_EXIT_CODE: 0` (L927) | ✅ |
| **Production build** | `UI007_P04_CA_FRONTEND_BUILD_EXIT_CODE: 0` (L930), Vite built in 1.73s | ✅ |
| **Ruff** | `UI007_P04_CA_RUFF_EXIT_CODE: 0` — "All checks passed!" | ✅ |
| **npm audit high gate** | `NPM_AUDIT_HIGH_EXIT_CODE: 0`; 2 moderate react-router advisories disclosed, not suppressed | ✅ |
| **Boundary greps** (re-affirmed in the same run) | read-only `0` · governance-control `0` · no-actuation `0` · R6 no-recompute `0` · external-AI `0` · route-declarations `0` (L295–305) | ✅ |
| **No drift** | `UI007_P04_CA_NO_MARKDOWN_RENDERER_DEPENDENCY`; `UI007_P04_CA_NO_REGISTRY_DRIFT` (L524–525) | ✅ |

**OBS-P03-1 — CLOSED.** The evidence the P03 and first P04 transcripts halted before producing now exists, on target, with the mandated sentinels and real totals. The `59f/266t` figure I could not accept as a Level-IV report claim last turn is now proven at Level-I, and the +5 delta is exactly the P04 named tests — no test was lost.

### The residual `LOCAL_CI = 1` — investigated, not waived by reflex

`LOCAL_CI` exited 1 because its embedded frontend run showed `Test Files 1 failed | 58 passed (59)` / `Tests 1 failed | 265 passed (266)` at ~497s, versus the direct gated run's clean `59/266` at ~293s.

**Assessment:** the *same* suite, same worktree, passed 59/59 minutes earlier in the direct gated run. The CI run took ~70% longer, which is the signature of a resource-contended sequential CI pass. This has strong precedent in this project — the **W3-U04/W3-U08 `test_live_market` StaticPool flake**, where a red gate was proven environment-bound and ruled non-blocking.

**But I will not close it on inference (R2/R7).** The failing test's **name and error output do not appear anywhere in the 2270-line transcript** — the display was truncated before `Failed Tests 1`. A red gate whose failing test cannot be named is not yet root-caused. It is downgraded to an **OBSERVATION with a named closure**, not a blocker, because the authoritative gated run is green and every substantive gate passed. **It is not relabeled green.**

---

## 3. 🟠 C-2 — **PART-CLOSED.** The remaining half is blocked on *me*, not the DA.

**Delivered and verified:**

| Item | Evidence | Verdict |
|---|---|---|
| Tree-wide conflict-marker scan | **`UI007_P04_CA_CONFLICT_MARKER_SCAN_CLEAN`** — exact scan, zero markers | ✅ |
| `git status` + HEAD | `HEAD=22c735a01f33cd4c5886b8bab1944dac19604127`, full modified/untracked listing displayed | ✅ |
| **Governance-document enumeration** (my explicit demand) | Manifest §3 names all six: `04_PROJECT_ROADMAP` (Tier 3), `GOVERNANCE_AMENDMENTS`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`, `PROJECT_STATE` (Tier 7), `CHANGELOG`. **Explicit statement: no Tier 1 Vision, Tier 2 Spec, Tier 4 Architecture, Tier 5 domain, or Tier 6 framework file was in the 25-file list** | ✅ **Answered exactly as demanded** |
| Full conflict manifest | 56 blocks / 25 files, per-file counts, `HEAD` side retained in each | ✅ |
| `TerminalLayout` disposition | `UI007_P04_CA_TERMINAL_LAYOUT_RETIRED_AND_UNREFERENCED` (L522); manifest §4 records it as an **explicit R16 scope deviation**, and names the invariant it violated: `test_terminal_layout_retired_shell_is_sole_frame` | ✅ Disclosed correctly |

**Blocked — and correctly so:** `UI007_P04_CA_PROVENANCE_EXIT_CODE: 9001` with `UI007_P04_CA_APPROVED_BASELINE_REF_MISSING`. The runner requires `-ApprovedBaselineRef` and **refuses to invent one**: *"The repository contains no local ref identified as the last approved baseline; the clone has one visible commit only… The DA will not invent that reference."*

**That is the correct behaviour, and the gap is mine.** I demanded `git diff --stat` against "the last approved baseline" without supplying the ref. The clone has exactly one commit (`22c735a`, "AXIOM TRADING PLATFORM v1.0") — the same single-commit condition I observed when I cloned `ITRGA-FILES` at onboarding. A DA that fabricated a plausible-looking baseline SHA to make a gate go green would have committed a far worse offence than the one it is answering. **Refusing to guess is the standard working.**

**C-2 therefore cannot close this turn.** It is not a DA failure. It requires the Operator to supply the approved baseline commit SHA / signed tag — this is now **an operator action item**, and it is the reason this determination is not an approval.

**A note I must record for the institutional file:** the discovery that the *committed* baseline contained 56 conflict blocks across 25 files — including a Tier-3 and three Tier-7 governance documents — means the repository's approved-baseline provenance was already compromised **before** UI-007-P04 began. That is a program-level integrity matter that outlives this phase.

---

## 4. ❌ C-3 — **OPEN.** Browser evidence absent.

`UI007_P04_CA_BROWSER_SCREENSHOT_MISSING_OR_EMPTY` lists all four required captures as missing:
`UI-007-P04_CA_01_EVIDENCE_VIEWER_MANIFEST.png` · `..._02_VALIDATION_SUMMARY_FIELDS.png` · `..._03_NO_MUTATION_OR_ACTUATION_CONTROLS.png` · **`..._04_LOGGED_OUT_BLOCK.png`**

No screenshots accompanied this pack. Under **R4 — UI units are judged in the browser** — this alone caps the verdict. I hold the five authenticated `/governance` screenshots from the prior submission and they were strong, but the **logged-out block has never been evidenced in this phase**, and re-running the suite does not substitute for it.

**Note on scope:** the runner demands four captures; my C-3 required only the logged-out shot (the other three were already satisfied last turn). Supplying `..._04_LOGGED_OUT_BLOCK.png` alone would discharge C-3 as I wrote it — though a matched set is cleaner for the archive.

---

## 5. Findings

| ID | Severity | Status |
|---|---|---|
| **C-1** | CRITICAL | ✅ **CLOSED** — OBS-P03-1 met; gated 59f/266t exit 0, backend 414, alembic head, tsc/build/ruff green |
| **C-2** | HIGH | 🟠 **PART-CLOSED** — conflict scan clean, governance docs enumerated, R16 deviation disclosed; **baseline-diff blocked pending ITRGA/Operator ref** |
| **C-3** | MEDIUM | ❌ **OPEN** — browser evidence, incl. logged-out block, not supplied |
| OBS-P04-1 | OBSERVATION | ✅ **CLOSED** — one authoritative target total (59f/266t), reconciled to baseline +5 |
| OBS-P04-2 | OBSERVATION | ✅ **CLOSED** — `python -m alembic`, exit 0, head printed |
| OBS-P04-3 | OBSERVATION | ✅ **CLOSED** — CI invoked by absolute path from repo root; no 127 |
| **OBS-P04-CA-1** | OBSERVATION (new) | `LOCAL_CI = 1`: 1 failed / 265 passed at 497s vs green 59/266 at 293s. Contention-flake signature per the W3-U04/W3-U08 precedent, **but the failing test is unnamed in the transcript**. Must be named + root-caused. **Not relabeled green** |
| **OBS-P04-CA-2** | OBSERVATION (new) | Evidence runner is unsigned; required `Set-ExecutionPolicy -Scope Process Bypass`. Documented, process-scoped only. Acceptable; prefer signing or `-File` invocation |
| **PROGRAM-LEVEL** | HIGH (carried) | Committed baseline contained 56 conflict blocks / 25 files incl. Tier-3 + three Tier-7 governance docs. Predates P04; requires disposition beyond this phase |
| — | **COMMENDATION** | The runner prints a **per-gate exit-code table**, ends with `UI007_P04_CA_EVIDENCE_COMPLETED_WITH_FINDINGS` enumerating every non-zero result, and states verbatim: **"All raw evidence artifacts were still collected. Do not relabel this result green."** A DA that engineers its own harness to make failures impossible to hide is doing exactly what this standard demands |

---

## 6. Required to close

1. **C-2 — ITRGA/OPERATOR ACTION:** supply the approved baseline commit SHA / signed tag for `-ApprovedBaselineRef`, then re-run the provenance gate only (`git diff --stat`, `--name-only`, `--check`). **The DA is correctly blocked until this is provided.**
2. **C-3 — DA:** `UI-007-P04_CA_04_LOGGED_OUT_BLOCK.png` (unauthenticated `/governance` → `/login`); ideally the full four-capture set.
3. **OBS-P04-CA-1 — DA:** name the CI-failing test and its error, and either show it green on re-run or root-cause it as environment-bound in-code.

**No re-implementation. No re-run of the passing gates.** C-1's evidence stands; do not repeat the 10-minute backend suite or the 5-minute frontend suite to close a screenshot.

---

## 7. Disposition

**UI-007-P04 remains CORRECTIVE ACTIONS REQUIRED — but the critical blocker is gone.**

C-1, the non-waivable finding that stopped this phase twice, is **CLOSED on Level-I target evidence**. The gated suite is green at 59 files / 266 tests with the sentinel printed, backend 414 holds, alembic head holds, tsc/build/ruff are clean, and every boundary grep was re-affirmed in the same run. The G-5 verbatim spine — proven sound last turn — is now backed by a complete regression envelope.

What remains is small and largely not the DA's to fix: **C-3** needs one screenshot, and **C-2's** final step is blocked on a baseline reference only the Operator can supply. The DA's refusal to fabricate that ref, and its decision to surface `LOCAL_CI = 1` in a summary table with an explicit instruction not to relabel it green, are the two most creditable acts in this submission. I said last turn that a third report-only or halted transcript would not be adjudicated again. This is neither — it is a complete, honest, root-anchored run.

Verification is limited to supplied evidence. Direct browser validation was not possible this turn; the CI-failing test could not be identified from the transcript.

**Baseline does NOT advance — v0.62.0 · head `20260717_0037` · backend 414 · frontend 58f/261t of record** (the 59f/266t total is proven and will become the baseline of record on approval). **UI-007-P05 remains unauthorized.** Governance Gate CLOSED. Production NOT CERTIFIED.

Carried residuals: TD-UI-REACTROUTER-MODERATE · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b. (TD-UI-POSTCSS-HIGH CLOSED.)

---

## 8. Evidence Confidence Statement

- **Evidence reviewed:** `DELIVERY_REPORT_UI-007-P04_CA_RESPONSE.md`; `OPERATOR_RESULTS.md` (2270 lines, read in full); the C-2 conflict-resolution manifest embedded in the transcript.
- **Confidence:** **HIGH** that C-1 is discharged — sentinels, totals, and per-gate exit codes are directly evidenced on target. **HIGH** that the conflict repair is disclosed accurately and that no Tier-1/2/4/5/6 document was affected. **MODERATE** on the `LOCAL_CI` flake classification — the precedent fits and the direct run is green, but the failing test is unnamed. **LIMITED** on browser state and on baseline equivalence, neither of which was producible this turn.
- **Remaining unknowns:** identity of the CI-failing test; semantic diff of the six conflict-resolved governance documents against an approved baseline; current logged-out behaviour.
- **Additional evidence required:** §6 items 1–3.

---

**We don't guess. We prove.**

*— AXIOM ITRGA*
