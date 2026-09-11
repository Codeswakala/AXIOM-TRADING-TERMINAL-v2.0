# ITRGA DETERMINATION — UI-007-P04

**Evidence Viewer & Validation Summary Panels** — *(Read-Only)*

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P04** |
| Build Order | `BUILD_ORDER_UI-007-P04.md` |
| Pack | `DELIVERY_REPORT_UI-007-P04.md` (219 lines) + `OPERATOR_RESULTS.md` (547 lines) + 5 served screenshots |
| Governing docs | Doc 12 §9, `UI-007_ENGINEERING_DESIGN_PLAN.md` §3 (G-5)/§8 (P04), `ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` (R-1…R-8, esp. R-3/R-6/R-7), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 58f/261t |
| **DETERMINATION** | 🟡 **CORRECTIVE ACTIONS REQUIRED** |
| Baseline | **UNCHANGED — v0.62.0** (no version advance on a non-approving verdict) |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-007-P04`; Phase `**UI-007-P04**`; "not self-approved" | ✅ OF the unit |
| Operator transcript | `UI007_P04_EVIDENCE_STARTED: 2026-07-28T09:50:30`; `UI007_P04_BUILD_IDENTITY_CONFIRMED` block greps the P04 report, the P03 review, the P04 Build Order and the DA intake | ✅ OF the unit |
| Predecessor chain | P03 review cited with OBS-P03-1/-2 quoted verbatim | ✅ Correct |
| Stale/concatenated pack | None detected | ✅ |

**Pack confirmed OF UI-007-P04.** The DA does not self-approve. Build identity is the one gate this pack passes without qualification.

---

## 2. Level-I evidence verification — line-by-line

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| (a) | Build identity | `UI007_P04_BUILD_IDENTITY_CONFIRMED` + header greps | ✅ PASS |
| (b) | 5 named tests DISPLAYED passing | **`Test Files 1 passed (1)` / `Tests 5 passed (5)`** (L125–126), all five named verbatim with per-test timings; `UI007_P04_NAMED_VITEST_EXIT_CODE: 0` (L145) | ✅ PASS |
| (c) | 🔴 G-5 verbatim / no AI-summary / no recompute | `UI007_P04_R6_NO_RECOMPUTE_RELATIONSHIP_INFERENCE_GREP_CLEAN` + `UI007_P04_EXTERNAL_AI_GREP_CLEAN` (L235–236). **Patterns inspected and correct** (`openai\|gpt\|external_llm\|llm_summary\|ai_summary`; `recompute\|recalculat\|deriveConfidence\|reclassif\|new .*Engine`), throw-guarded, 5 named source files | ✅ PASS |
| (d) | 🔴 No-cherry-picking | Source shows `scope`/`uncertainty`/`limitations`/`sample count` rendered as stored; page text *"filtered view is not a full-scope governance claim"* (L294); browser confirms; named test #2 | ✅ PASS |
| (e) | 🔴 Read-only + G-2 governance-control grep | `UI007_P04_EVIDENCE_AND_VALIDATION_READ_ONLY_GREP_CLEAN` + `UI007_P04_GOVERNANCE_CONTROL_GREP_CLEAN` (L254–255); pattern includes `open_gate\|allow_execution\|gate.*toggle\|certify\|mark_ready\|approve_production\|waive\|risk_accept` | ✅ PASS |
| (f) | 🔴 M-4 no-actuation grep | `UI007_P04_NO_ACTUATION_GREP_CLEAN` (L256); broad pattern incl. `buy\|sell\|place_order\|execute\|broker\|position\|margin\|real_pnl` | ✅ PASS |
| (g) | No-drift | `alembic current` → **`20260717_0037 (head)`** (L465); `UI007_P04_NO_MARKDOWN_RENDERER_DEPENDENCY`; `UI007_P04_NO_REGISTRY_DRIFT`; `UI007_P04_ROUTE_DECLARATION_GREP_CLEAN`; existing intelligence read seam confirmed | ✅ PASS |
| (h) | **🔴🔴 OBS-P03-1 — completed gated regression** | **FAILED.** `UI007_P04_FRONTEND_FULL_REGRESSION_FAILED:1` (L509) — the full suite exited **1** and `$ErrorActionPreference=Stop` **threw**. `FRONTEND_VITEST_EXIT_CODE:` was **never printed**. No `Test Files`/`Tests` full-suite total appears anywhere. Backend `pytest` total **never displayed**; `BACKEND_PYTEST_EXIT_CODE:` never printed. Networked CI **never ran** | ❌ **UNMET — C-1** |
| (i) | 🔴 OBS-P03-2 — grep fix | Replaced with `@router.(get\|post\|put\|patch\|delete)` declaration-anchored scan over `backend/app/api`, with `governance_gate.py` explicitly `Test-Path`-asserted and excluded by scope: `UI007_P04_PREEXISTING_GOVERNANCE_GATE_MODULE_EXCLUDED_BY_SCOPE` (L275). Completed without false-positive halt | ✅ **CLOSED** |
| (j) | Doc 16 brand B-1…B-7 | `.mono` on ids/hashes/sample counts in source; browser shows monospace metadata, palette, GATE CLOSED / RESEARCH-ONLY chips; named test #5 | ✅ PASS (browser + test) |
| (k) | Browser served-session | 5 authenticated `/governance` screenshots — evidence viewer index + verbatim stored fields, validation summaries, audit explorer, residuals, boundary cards, no mutation control. **No logged-out `/login` screenshot supplied** | ⚠️ **PARTIAL — C-3** |
| (l) | Networked CI `LOCAL_CI_EXIT_CODE: 0` | **Absent.** Run halted at (h) before CI. Report discloses attempt returned **127** (relative-path launch) | ❌ **UNMET — C-1** |

---

## 3. 🔴 C-1 (CRITICAL) — OBS-P03-1 unmet a second time; transcript halted again

The Build Order's determination rule is explicit: *"a report-only regression (OBS-P03-1 unmet) … or a halted/false-positive evidence transcript ⇒ Corrective Actions Required."* Both conditions are present.

- **The gated full suite failed, it did not merely go unrecorded.** `UI007_P04_FRONTEND_FULL_REGRESSION_FAILED:1` with a PowerShell `OperationStopped` trace at L509–514. The mandated sentinel `FRONTEND_VITEST_EXIT_CODE: 0` was **never emitted** — only its `Write-Host` command echo at L490, which is a command, not a result. **A command echo is not output (R7).**
- **Everything downstream is therefore absent:** `tsc -b`, `npm run build`, the backend `pytest` total, `BACKEND_PYTEST_EXIT_CODE`, `UI007_P04_RUFF_EXIT_CODE`, and the networked CI. The later backend block ran but its `Get-Content`/`Select-String` display never rendered a `414 passed` line; the block terminated on an alembic `NativeCommandError`. **Backend 414 is unproven at Level-I in this pack.**
- **This is the second consecutive halted transcript.** P03 halted on a benign false-positive; P04 halted on a *genuine test failure*. OBS-P03-1 was declared **non-waivable at P04** in writing. It is unmet.

**On the honesty of the disclosure — credit where due.** The DA did not bury this. Report §3 states plainly: *"Operator attempt 1 — **not an approval-grade rerun**"*, itemising the `TerminalLayout` failure (58/59 files, 265/266 tests), the alembic launcher fault, the backend exit 1, and the CI 127. It states the transcript *"remains a finding, not a green result."* That is exactly the conduct this standard is built to produce, and it is why this lands at Corrective rather than Rejected. **But an honest disclosure of missing evidence does not become the evidence.** The DA is asking me to approve on Level-IV report figures — precisely what OBS-P03-1 was written to stop.

### R12 — internal consistency: four different frontend totals

| Source | Files / Tests | Tier |
|---|---|---|
| Baseline of record (carried in the Build Order) | 58f / 261t | — |
| Report §3 "local engineering validation" | **59f / 266t** | Level-IV (dev box, not target) |
| Report §3 "operator attempt 1" | **58f / 265t** — one failure | Level-IV |
| Browser evidence card (TD-POSTCSS, as-stored) | 56f / 251t | as-stored historical — legitimate |
| **Operator transcript (only Level-I source)** | **NOT PRINTED** | — |

The 59f/266t figure comes from the DA's own environment *after* deleting a file, not from the target. Per R3, target-platform operator-run evidence is mandatory. **The gated total remains unproven.**

---

## 4. 🟠 C-2 (HIGH) — undisclosed-until-now repository integrity event + unauthorized source deletion

Report §6 discloses that the baseline checkout contained **56 committed unresolved merge-conflict blocks across 25 tracked files** — governance documents, backend modules, tests, frontend source, and configuration — causing backend parser failures *before P04 validation could start*. The DA resolved them by retaining the `HEAD` side, then deleted `frontend/src/layouts/TerminalLayout.tsx`.

This is disclosed responsibly and is plausibly a genuine repair. **It is also the most serious build-provenance event in this workstream's history**, and it cannot be waved through:

1. **R16 scope discipline.** `TerminalLayout.tsx` deletion is **not authorized** by the P04 Build Order (the string does not appear in it). Deleting source to make a suite pass is a scope deviation, however benign — and it is the direct cause of the 58f/265t → 59f/266t delta. Even well-intentioned extras are findings.
2. **Build provenance.** A worktree that had 56 conflict blocks across 25 files, resolved by hand, is not self-evidently the approved baseline. Every prior verdict's evidence chain assumes a clean tree. **I require proof that the repaired worktree equals the approved baseline plus P04 only** — `git status`, `git diff --stat` against the last approved commit, and a conflict-marker grep (`<<<<<<<|=======|>>>>>>>`) returning empty across the tree.
3. **Governance documents were among the affected files.** If any Tier-1…Tier-7 document was altered by conflict resolution, that is a constitutional matter, not a housekeeping one. It must be enumerated explicitly.

---

## 5. ⚠️ C-3 (MEDIUM) — logged-out block not evidenced

Item (k) requires a logged-out `/login` screenshot. Five authenticated `/governance` shots were supplied; none shows the unauthenticated block. This has been a standing requirement since GR6-10 and was met in prior phases. Low effort to close.

---

## 6. What genuinely passed — the G-5 spine is sound

I want the record to be precise about this, because the P04 *design* is not the problem.

The **G-5 spine holds on the evidence supplied.** The evidence viewer renders an index of recorded evidence with source-preserving fields — `Status / verdict as stored`, `Method / version as stored`, `Observed sample / test count`, `Scope as stored`, `Uncertainty / observation`, `Limitations`, `Source ids`, `Lineage`, `Audit reference`, `Report hash`, `Recorded at`. The browser shows `Report hash: Not recorded` rather than fabricating one, and the UI-007-P03 card carries its own `OBS-P03-1 regression and CI transcript required at P04` limitation **on screen**. The header states *"This is an index of recorded evidence, not a file browser, upload surface, or generated narrative"* and *"Recorded fields only · No source alteration."*

That is textbook R-3/G-5: the workspace discloses its own unmet obligation verbatim instead of flattering itself. All four boundary greps are clean with correct, inspected patterns. No new endpoint, dependency, migration, route, or persistence. Alembic head holds at `20260717_0037`. **OBS-P03-2 is properly closed** with a declaration-anchored scan that is narrower *and* stricter than the pattern it replaces.

**The implementation looks right. The proof does not exist yet.**

---

## 7. Findings by severity

| ID | Severity | Finding |
|---|---|---|
| **C-1** | **CRITICAL** | OBS-P03-1 unmet (declared non-waivable): gated full-suite failed exit 1 and halted; `FRONTEND_VITEST_EXIT_CODE: 0` never printed; backend 414 never displayed; networked CI never ran |
| **C-2** | **HIGH** | 56 merge-conflict blocks across 25 files repaired in-flight; unauthorized deletion of `TerminalLayout.tsx` (R16); build provenance of the repaired worktree unproven |
| **C-3** | **MEDIUM** | Logged-out `/login` screenshot absent |
| OBS-P04-1 | OBSERVATION | Four divergent frontend totals across report/browser/baseline (R12) — reconcile to one Level-I number |
| OBS-P04-2 | OBSERVATION | Target `alembic` launcher references a prior repo location; backend block ended on `NativeCommandError`. Head *was* proven `20260717_0037` earlier at L465, so this is tooling hygiene |
| OBS-P04-3 | OBSERVATION | CI invoked by relative path → 127. Anchor to `$repoRoot` |
| ✅ | CLOSED | **OBS-P03-2** — endpoint grep fixed, no false-positive halt |
| — | COMMENDATION | §3 and §6 disclosures are candid and self-penalising. This is the conduct the standard exists to produce |

---

## 8. Required corrections (re-submission, no re-implementation)

The product code appears not to need changes. Re-run the evidence pack, root-anchored, on the target:

1. **C-1 —** Completed gated transcript: `FRONTEND_VITEST_EXIT_CODE: 0` printed with the **full** `Test Files` / `Tests` totals (≥58f/261t, **no test lost**); backend `pytest -q` with `414 passed` **displayed**; `BACKEND_PYTEST_EXIT_CODE: 0`; `alembic current 20260717_0037`; `tsc -b` + `npm run build`; networked CI `LOCAL_CI_EXIT_CODE: 0` (or a documented TD-W6-CI-AUDIT env-flake **after** substantive gates are green). **If the suite legitimately advances to 59f/266t via the TerminalLayout removal, prove that on the target and state the delta explicitly.**
2. **C-2 —** Build-provenance proof: `git status`, `git diff --stat` vs the last approved baseline, conflict-marker grep returning empty, and an **explicit enumeration of every governance document touched** by the conflict resolution. Confirm no Tier-1…Tier-7 document changed meaning.
3. **C-3 —** Logged-out `/login` screenshot.
4. Re-affirm the four boundary greps in the same completed run (cheap; keeps one coherent transcript).

**A third report-only or halted regression transcript will not be adjudicated a third time.**

---

## 9. Disposition

**UI-007-P04 is CORRECTIVE ACTIONS REQUIRED.**

The evidence viewer and validation summary panels appear constitutionally clean — G-5 verbatim disclosure holds, no AI summary, no recompute, no stronger-than-source verdicts, no cherry-picking, no mutation surface, no drift — and **OBS-P03-2 is closed**. But **OBS-P03-1, expressly declared non-waivable at P04, is unmet for the second consecutive phase**, this time because the gated suite genuinely failed and halted the run. The Build Order's own determination rule makes this outcome mandatory; I have no discretion to approve around it, and adjudicating it a second time would convert a non-waivable control into a negotiable one.

The in-flight repair of 56 merge-conflict blocks and the unauthorized source deletion compound this: the worktree that produced these figures has not been proven to be the approved baseline.

Verification is limited to supplied evidence. Direct runtime validation of the full regression suite, backend total, and CI was not possible.

**Baseline does NOT advance — remains v0.62.0 · head `20260717_0037` · backend 414 · frontend 58f/261t.** No Build Order for UI-007-P05 is issued. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

Carried residuals: TD-UI-REACTROUTER-MODERATE · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b. (TD-UI-POSTCSS-HIGH CLOSED.)

---

## 10. Evidence Confidence Statement

- **Evidence reviewed:** `DELIVERY_REPORT_UI-007-P04.md` (219 lines); `OPERATOR_RESULTS.md` (547 lines, read in full); 5 served browser screenshots; the P04 Build Order and P03 determination.
- **Confidence:** **HIGH** that the P04 named tests, all four boundary greps, no-drift, alembic head, and the G-5 verbatim design are proven at Level-I. **HIGH** that OBS-P03-1 is unmet — the failure sentinel and the absent totals are directly evidenced. **LIMITED** on full-suite regression state, backend total, tsc/build, CI, and worktree provenance — none were produced.
- **Remaining unknowns:** the true target full-suite total; whether the single failure was solely `TerminalLayout.tsx`; backend and CI state on target; exact governance-document diffs from the conflict repair.
- **Additional evidence required:** items 1–4 of §8.

---

**We don't guess. We prove.**

*— AXIOM ITRGA*
