# ITRGA RULING — UI-007-P04 C-2 APPROVED BASELINE REFERENCE

**Subject:** The approved baseline reference required for `-ApprovedBaselineRef`
**Authority:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**Date:** 2026-07-28
**Applies to:** `DELIVERY_REPORT_UI-007-P04_CA_RESPONSE.md` · `UI007_P04_CA_PROVENANCE_EXIT_CODE: 9001`

**Motto: "We don't guess. We prove."**

---

## 1. RULING — no approved baseline reference exists, and I will not invent one

**There is no approved baseline commit SHA, signed tag, or Git ref to supply.**

The AXIOM implementation repository contains **exactly one commit**:

```text
HEAD    = 22c735a01f33cd4c5886b8bab1944dac19604127
SUBJECT = AXIOM TRADING PLATFORM v1.0
```

Everything from Wave 0 through UI-007-P04 exists as **uncommitted working-tree state** on top of that single commit. There is no pre-P04 commit, no per-phase tag, and no last-approved-baseline ref anywhere in the repository. Therefore `git diff <approved-baseline>..HEAD` is **structurally impossible to run meaningfully** — not merely inconvenient.

The same rule that binds the DA binds me. A fabricated or "close enough" SHA from ITRGA would be exactly the offence the DA correctly refused to commit. **I do not guess either.**

**`-ApprovedBaselineRef` is therefore WITHDRAWN as an evidence requirement for UI-007-P04.**

---

## 2. This is settled precedent — and I should have applied it before demanding the ref

This is not a new problem. It was diagnosed, litigated, and **formally retired** at UI-002-P05.

**The precedent chain (`ITRGA_REVIEW_UI-002-P05.md` → `ITRGA_REVIEW_UI-002-P05_FINAL_AND_UI-002_COMPLETION.md`):**

1. ITRGA imposed a phase-isolating `git diff` no-drift gate against `UI-002-P04_BASELINE`.
2. The ref did not exist. `git diff` returned `fatal: bad revision 'UI-002-P04_BASELINE..HEAD'` and wrote nothing — and the harness printed the **clean sentinel off a failed command**. ITRGA called that what it was: *"an R7 non-result presented as a pass — a false-clean"* and returned **Corrective**.
3. The DA then did it properly: created the tag (`git tag UI-002-P04_BASELINE 7aff710`), verified it, and gated on `$LASTEXITCODE`. The diff **succeeded** — and printed `PHASE_ISOLATED_DIFF_FILENAMES_PRESENT`, listing W0–W4 migrations and Wave-0-era backend files.
4. **Root cause, established by `git log --oneline --all`:** the repository held **exactly one commit** — `7aff710 "Initial commit: AXIOM platform foundation (W4-U05)"`. So `7aff710..HEAD` spanned *all history since W4-U05*, sweeping in files that predate UI-002 by months.

ITRGA's own recorded conclusion:

> **"A git-diff phase-isolation of the UI-002 delta is structurally IMPOSSIBLE in this repo — no per-phase (or even per-wave) commits exist to diff against. The `FILENAMES_PRESENT` result is a structural artifact, not evidence of drift."**
>
> **"Operator disposition: retire the git-diff no-drift gate; accept the corroborated no-drift evidence."**

**The repository has since been re-initialised** — `7aff710 (W4-U05)` → `22c735a (v1.0)` — but the defect is unchanged: still a single commit, still no per-phase history. The condition that made the gate unworkable at UI-002 makes it unworkable at UI-007.

**I record this against myself:** when I raised C-2 I demanded a baseline diff without first checking whether the ref could exist. That was a governance-instrument error on my part — I imposed a control this repository cannot satisfy. The DA's refusal to invent the ref is what surfaced it. **Under R19, the correction belongs in the record, not quietly dropped.** The DA is not at fault for the 9001, and it costs the DA nothing further.

---

## 3. What replaces it — the substitute method, already satisfied

Per the UI-002-P05 disposition, no-drift is proven by **methods that work in a single-commit repository**. For UI-007-P04 these were **already produced and verified** in the corrective transcript:

| Guarantee | Evidence in the CA transcript | Result |
|---|---|---|
| Tree contains no unresolved conflict text | **`UI007_P04_CA_CONFLICT_MARKER_SCAN_CLEAN`** — exact tree-wide scan | ✅ |
| Working-tree delta fully disclosed | Full `git status` displayed: 21 `M`, 1 `D`, all `??` untracked evidence artifacts | ✅ |
| Alembic head unchanged | `20260717_0037 (head)`; `UI007_P04_CA_ALEMBIC_CURRENT_EXIT_CODE: 0` | ✅ |
| No new dependency | `UI007_P04_CA_NO_MARKDOWN_RENDERER_DEPENDENCY`; `NPM_AUDIT_HIGH_EXIT_CODE: 0` | ✅ |
| No registry drift | `UI007_P04_CA_NO_REGISTRY_DRIFT` | ✅ |
| No new endpoint | `UI007_P04_CA_ROUTE_DECLARATIONS_EXIT_CODE: 0` (declaration-anchored) | ✅ |
| Backend unaffected | **414 passed**; `BACKEND_PYTEST_EXIT_CODE: 0` | ✅ |
| Governance docs enumerated | Manifest §3 — six files named; **no Tier-1/2/4/5/6 file affected** | ✅ |
| `TerminalLayout` disposition | `UI007_P04_CA_TERMINAL_LAYOUT_RETIRED_AND_UNREFERENCED`; recorded as an explicit R16 deviation | ✅ |

**No re-run is required.** The evidence that closes C-2 is already in the 2270-line corrective transcript.

---

## 4. C-2 disposition

**C-2 is CLOSED**, on the UI-002-P05 substitute-method basis:

- The **baseline-diff limb is WITHDRAWN** — structurally impossible; the requirement was mine in error.
- The **conflict-repair limb is SATISFIED** — clean marker scan, full manifest (56 blocks / 25 files), governance enumeration confirming no Tier-1/2/4/5/6 document was touched.
- The **R16 `TerminalLayout` limb is SATISFIED as disclosed** — recorded as an explicit scope deviation, proven retired and unreferenced, with the invariant it violated (`test_terminal_layout_retired_shell_is_sole_frame`) named. **Accepted, not waived**; it stands in the record as a deviation the DA declared rather than hid.

**The DA must not re-run the provenance gate.** Remove `-ApprovedBaselineRef` from the runner's mandatory path, or make it optional and skip cleanly with a stated reason when absent. **A gate that cannot pass must not remain armed** — that is how false-cleans get manufactured, exactly as at UI-002-P05.

---

## 5. 🔴 New standing finding — repository provenance is a program-level defect

I am closing C-2 for this phase, but I will not let the underlying condition disappear with it.

**`TD-AXIOM-GIT-PROVENANCE` (opened 2026-07-28, HIGH, non-blocking for UI-007-P04):**

The implementation repository has **one commit** for a platform spanning Waves 0–7 plus seven UI workstreams, with ~v0.62.0 of delivered work living entirely in an uncommitted working tree. Consequences already realised:

- Phase-isolating diffs are impossible (twice now: UI-002, UI-007).
- The committed baseline `22c735a` contained **56 unresolved merge-conflict blocks across 25 tracked files**, including Tier-3 `04_PROJECT_ROADMAP.md` and three Tier-7 registers. **A conflicted tree was the committed state of record.**
- No approved-baseline anchor exists for any verdict in the ledger.
- Months of delivered work sit unprotected against a single accidental loss.

**This is not a UI-007 defect** — it predates this workstream and touches every unit approved to date. But under **Doc 11 §5 (Deployment) and §8 (Operational Readiness)**, a platform with no commit history and no reproducible baseline is **not certifiable for production**, however green its tests.

**Disposition:** carried as a standing residual. **To close:** a dedicated repository-provenance Build Order — commit the current tree as an anchored, tagged baseline (e.g. `AXIOM_v0.62.0_BASELINE`), tag each subsequent approved phase, and verify no conflict markers at commit time. **This must be dispositioned before Production Readiness Certification** — it joins the pre-certification gate list.

**Operator action:** authorize that Build Order at a time of your choosing. It does not block UI-007-P05.

---

## 6. Where UI-007-P04 now stands

| Finding | Status |
|---|---|
| **C-1** — OBS-P03-1 gated regression | ✅ **CLOSED** (59f/266t exit 0, backend 414, alembic head, tsc/build/ruff) |
| **C-2** — provenance | ✅ **CLOSED** by this ruling (baseline-diff withdrawn; substitute method satisfied) |
| **C-3** — browser evidence | ❌ **OPEN — the sole remaining blocker** |
| OBS-P04-CA-1 — `LOCAL_CI = 1` | 🟡 Open observation — name the failing test + root-cause |
| **TD-AXIOM-GIT-PROVENANCE** | 🔴 New standing residual (program-level, pre-certification) |

**One artifact stands between UI-007-P04 and approval:** `UI-007-P04_CA_04_LOGGED_OUT_BLOCK.png` — unauthenticated `/governance` redirecting to `/login`. Under **R4**, a UI phase is judged in the browser; I hold five strong authenticated `/governance` captures from the first submission, but the logged-out block has never been evidenced in this phase.

**Do not re-run any passing gate to produce it.** One screenshot. Optionally the matched set of four for a clean archive, plus the CI test name if convenient.

---

## 7. Instruction to the Development Authority

1. **Do not supply, infer, or construct a baseline ref.** The requirement is withdrawn. Your refusal was correct and is commended in the record.
2. **Disarm the provenance gate** so it cannot print a clean sentinel off a skipped or failed command (the UI-002-P05 false-clean lesson).
3. **Supply the logged-out browser capture.** That closes C-3.
4. **Optionally** name the CI-failing test and its error.

On receipt, ITRGA expects to determine **Approved with Observations**, advance the baseline of record to **v0.62.0 · head `20260717_0037` · backend 414 · frontend 59f/266t**, and — on operator authorization — issue `BUILD_ORDER_UI-007-P05`.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**. UI-007-P05 remains unauthorized until C-3 closes.

---

*A control that cannot be satisfied is not rigour — it is an obstacle wearing rigour's uniform. The DA proved that by refusing to fake it. The finding was mine; the correction is mine; the record shows both.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
