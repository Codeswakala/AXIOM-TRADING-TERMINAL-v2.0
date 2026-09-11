# Repository Provenance & Baseline Protocol

| Field | Value |
|---|---|
| Authority | `BUILD_ORDER_TD-AXIOM-GIT-PROVENANCE-REMEDIATION` as consolidated/amended by ITRGA |
| Status | Active from `AXIOM_v0.62.0_BASELINE` forward |
| Scope | Repository provenance, commit anchoring, tags, conflict/credential prevention |
| Gate / Production | Gate CLOSED · Production NOT CERTIFIED — unchanged |

## 1. Baseline principle

`AXIOM_v0.62.0_BASELINE` is the first anchored repository baseline. It represents the approved v0.62.0 platform state at UI-007 completion; it does not fabricate per-phase historical commits.

The baseline tag annotation states that earlier Waves and UI workstreams predate phase-isolating history. No retrospective per-phase tag or commit may imply a historical point that was not recorded.

## 2. Forward commit and tag rule

For every future ITRGA-approved unit:

1. retain the full approved worktree in a normal commit after all required evidence is collected;
2. record the unit, ITRGA determination, scope, regression baseline, Gate posture, and residuals in the appropriate governance records;
3. create an annotated tag at the approved commit using the ITRGA-authorized unit/version identifier;
4. include an honest tag annotation stating the approval determination and any limitation;
5. verify `git rev-parse --verify <tag>` and preserve the tag output in operator evidence.

This protocol makes phase-isolating diffs possible from the first anchored baseline forward. A phase tag must never be backdated, moved, force-updated, or used to imply history that did not exist.

## 3. Commit-time guard

The repository uses `.githooks/pre-commit` with `scripts/git_provenance_guard.py`. The guard:

- rejects staged conflict markers;
- scans staged Class A/B/C credential-value patterns without printing values;
- prints raw, D-2, D-5, and reconciliation counters;
- permits only the two hash-fingerprinted D-2 entries in `TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_MANIFEST.md`;
- rejects a changed exception path, identifier, or value fingerprint as an unreviewed match.

The D-2 exceptions are tracked under `TD-AXIOM-DEV-CREDENTIAL-LITERALS` and must be removed by a future dedicated security-remediation Build Order before Doc 11 §2 certification.

## 4. Evidence / local-data handling

Evidence outputs, operator transcripts, raw captures, and local database files are review inputs and are not committed to the anchored baseline. `.gitignore` controls future additions; existing historical review material is retained locally after authorized index-only removal.

## 5. Authority separation

The DA may create baseline commits, tags, manifests, and submission records but cannot mark a remediation debt closed. `TD-AXIOM-GIT-PROVENANCE` remains **Remediation submitted — awaiting ITRGA determination** until the independent closure ruling records the resolved baseline SHA in a follow-up governance-only commit.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

## Recovery operations after an anchored baseline

Any recovery must state its restore plan before execution and prove HEAD == tag, a clean strict conflict scan, disclosed status, and the expected tag-to-HEAD diff on completion. Relay actual artifact contents, not a path listing.