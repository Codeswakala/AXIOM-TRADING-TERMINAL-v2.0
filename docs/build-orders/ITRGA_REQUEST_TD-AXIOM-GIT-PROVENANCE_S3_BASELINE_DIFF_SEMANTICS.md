# ITRGA REQUEST — Consolidated Amendment 3 §3 Baseline-Diff Semantics

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| Authority under review | `ITRGA_CONSOLIDATED_AMENDMENT_3_TD-AXIOM-GIT-PROVENANCE.md` §3 steps 9 and 14 |
| DA posture | **HALTED before D-3 index removal, staging, commit, tag, hook activation, or history operation** |
| Gate / Production | **CLOSED** / **NOT CERTIFIED** — unchanged |

## 1. Direct conflict in the consolidated order

The consolidated order requires both:

1. **Step 9:** commit the approved v0.62.0 repository state on top of the sole historical commit `22c735a`; and
2. **Step 14:** `git show --stat <baseline SHA>` must show zero files in the forbidden column, including every `backend/app/**`, `frontend/src/**`, and test file.

Those requirements cannot both hold in this one-commit repository. The current approved v0.62.0 worktree contains the entire delivered platform/UI history as uncommitted changes relative to `22c735a`. Anchoring it necessarily makes those pre-existing product and test files appear in the baseline commit diff, even though this provenance unit does not edit them.

## 2. Direct measurement — no interpretation substituted

Before staging, the prospective baseline diff against `22c735a` contains:

```text
backend/app changed: 9
frontend/src changed: 8
backend/tests + frontend test candidates: 10
```

The affected paths are existing Wave/UI implementation state, not new edits by this provenance unit. A baseline commit that omits them fails the stated purpose of anchoring the approved v0.62.0 state; a baseline commit that includes them fails Step 14’s literal `git show` test.

The §2 allowlist corrects the prior claim that no file may change *by this unit*, but Step 14 still tests the commit diff against the historical conflicted parent and therefore reintroduces the same impossible condition.

## 3. Related unresolved W-8 item

The previously submitted `ITRGA_REQUEST_TD-AXIOM-GIT-PROVENANCE_W8_BASELINE_RECORDING.md` remains unresolved by Consolidated Amendment 3. Step 13 still asks for the baseline SHA inside post-baseline registers and for debt closure before independent review, without specifying a valid one-commit/no-self-approval form.

## 4. Requested single correction

Please prescribe the allowed proof for **“no forbidden files modified by this provenance unit”** that distinguishes:

- pre-existing, approved v0.62.0 implementation state being anchored; from
- source/test changes introduced during this remediation unit.

The DA recommends a pre-unit content manifest captured before provenance edits, followed by a comparison at baseline time. Under that method:

- the baseline commit may honestly include existing product/test changes relative to `22c735a`;
- the provenance unit proves it did not alter their content after the intake snapshot;
- `git show --stat <baseline SHA>` remains disclosed in full rather than falsely asserted empty for forbidden paths.

Please also provide the final W-8 register/closure record form in the same ruling so execution can resume under one coherent sequence.

No source, test, configuration, dependency, schema, route, Gate, certification, or production change is proposed. No commit or tag has been made.

**A baseline must anchor the real state, not a selectively empty state.**
