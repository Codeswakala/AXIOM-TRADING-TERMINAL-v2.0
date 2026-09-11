# BUILD ORDER INTAKE — TD-AXIOM-GIT-PROVENANCE-REMEDIATION

| Field | Value |
|---|---|
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| Authority | `BUILD_ORDER_TD-AXIOM-GIT-PROVENANCE-REMEDIATION.md` (ITRGA) |
| Intake date | 2026-07-29 |
| Predecessor | UI-007 complete — final determination recorded |
| Baseline to establish | v0.62.0 · Alembic `20260717_0037` · backend 414 · frontend 61 files / 276 tests |
| Gate / Production | **CLOSED** / **NOT CERTIFIED** — unchanged |
| DA intake status | **HALTED at mandatory P-2 pre-commit credential-scan clarification; no commit, tag, history rewrite, source edit, or production posture change performed** |

## 1. Scope and constraints acknowledged

The Build Order authorizes repository-provenance remediation only:

- one anchored baseline commit on top of the existing `22c735a` commit;
- annotated baseline and honest retrospective workstream tags;
- conflict/credential recurrence guard and forward protocol;
- `.gitignore` hygiene and registers reconciliation.

It explicitly prohibits product source, feature, dependency, migration, schema, route, test, Gate, certification, or production changes; history rewriting; force-push; deletion or amendment of `22c735a`; and fabricated per-phase history.

## 2. P-1 preparation completed in the working tree — not committed

`.gitignore` now contains the Build Order’s evidence/privacy exclusion patterns:

```text
docs/evidence/**
**/OPERATOR_RESULTS*.md
**/*_OPERATOR_RESULTS*.md
**/UI-*_RAW_*.json
scripts/*_evidence*.ps1
```

This does **not** untrack existing files. The initial repository inventory establishes that `docs/evidence/**` already has 570 tracked files, so the eventual compliant staging procedure must explicitly use `git rm --cached` (without deleting the local review corpus) before the baseline commit.

## 3. Mandatory P-2 preflight — blocked before commit

I applied the Build Order’s exact P-2 marker expression to the prospective staged scope **after conceptually excluding the P-1 evidence and evidence-runner paths**. Results are recorded without printing any credential value:

```text
P2_PREFLIGHT_SCOPE_TRACKED_FILES: 1105
P2_PREFLIGHT_MATCHED_FILES: 148
P2_PREFLIGHT_MATCHED_OCCURRENCES: 461
```

The matching files are distributed across root documentation/delivery reports, `.github`, backend source/tests/configuration, frontend auth contracts, scripts, and governance/plan material.

This is not a credential-scan pass. It is a mandatory **halt** under Build Order §3/P-2 and §6.

## 4. Structural ambiguity requiring ITRGA correction

The literal P-2 expression includes `access_token` and `refresh_token`. Those are pre-existing, required auth-contract field names in staged production source and tests; they are identifiers, not credential values. The same expression also matches pre-existing bootstrap/test constants and the Build Order’s own credential examples and required scanner pattern.

Consequently, staging the required product source, tests, Build Order, and governance corpus while executing the expression literally cannot produce the mandatory:

```text
STAGED_SECRET_MARKER_COUNT: 0
```

Redacting those identifiers or test/bootstrap constants would be a product/test/configuration change, expressly outside this metadata-only Build Order. Excluding required source from the baseline would mean the baseline no longer represents the approved v0.62.0 repository state. Either course would violate the Build Order.

## 5. Additional P-1/P-3 concern identified

A tracked database-backup path is present in the current repository and produced P-2 preflight markers. The Build Order’s `*.db` ignore rule does not affect already tracked content. Its disposition must be explicit in the authorized baseline procedure; it cannot be silently retained or removed from history.

The Build Order also contains literal examples and its own required marker expression. P-3 authorizes redaction of Build Orders/governance records, but a redacted scanner expression is no longer the exact expression the Build Order requires the operator to run. This needs an ITRGA-specified canonical redacted form and scan scope.

## 6. DA disposition

No baseline commit, tag, retrospective tag, hook activation, `git rm --cached`, redaction, staging, history rewrite, or production/source change has been performed after this finding.

The DA has prepared `ITRGA_REQUEST_TD-AXIOM-GIT-PROVENANCE-P2_SCAN_SCOPE_CLARIFICATION.md`. The unit may resume only after ITRGA resolves the scan-scope/false-positive contradiction and gives a safe disposition for already tracked evidence and database-backup material.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

---

## 7. Amendment 1 received — P-3 applied; D-2 scan-count disposition remains explicit

`ITRGA_RULING_TD-AXIOM-GIT-PROVENANCE_P2_SCAN_SCOPE.md` supersedes the original P-2/P-3/W-6 control. Its fixed three-class value scanner was applied without printing any matched value.

### P-3 redaction prepared under D-4

The authorized document families were redacted using only the canonical placeholders. The filename-only manifest is:

```text
docs/build-orders/TD-AXIOM-GIT-PROVENANCE_REDACTION_MANIFEST.md
```

```text
P3_REDACTED_FILE_COUNT: 37
P3_REDACTED_CLASS_A_COUNT: 71
P3_REDACTED_CLASS_B_COUNT: 1
P3_REDACTED_CLASS_C_COUNT: 0
```

### Real residual under the unmodified §2 scanner

After the authorized P-3 document work and P-1 path exclusions, the exact fixed scanner reports three Class-A shaped matches: two in pre-existing D-2-permitted source/evidence-runner configuration paths and one synthetic hook-demonstration literal retained verbatim in the new ITRGA ruling:

```text
POST_P3_PROSPECTIVE_STAGED_DIFF_HIT_FILES: 3
POST_P3_PROSPECTIVE_STAGED_DIFF_HIT_OCCURRENCES: 3
```

D-2 says existing dev/test literals may remain and opens `TD-AXIOM-DEV-CREDENTIAL-LITERALS`; D-5 requires an intentionally fake hook demonstration; but the ruling does not prescribe whether the two D-2 matches and the one retained authority-record demonstration are formal, documented exceptions or non-zero P-2 halts. The DA will not invent an allowlist or report a false zero. A narrow D-2/D-4 count-disposition clarification has been requested before staging or committing.

---

## 8. Consolidated Amendment 3 received — Step 9 / Step 14 conflict measured

`ITRGA_CONSOLIDATED_AMENDMENT_3_TD-AXIOM-GIT-PROVENANCE.md` is recorded as the current consolidated execution reference. Its new P-1 raw-artifact ignore pattern has been added.

Before executing D-3 or staging, the DA tested the consolidated Step 14 rule against the actual repository state. The prospective baseline diff relative to the sole parent `22c735a` contains 9 `backend/app/**` paths, 8 `frontend/src/**` paths, and 10 test candidates. These are the approved v0.62.0 state that Step 9 requires the baseline to anchor.

Therefore a real baseline commit cannot both include the approved v0.62.0 platform and yield a `git show --stat <baseline SHA>` with zero forbidden-column paths. This is not a prospective implementation concern; it is directly measurable in the current repository.

The DA has prepared `ITRGA_REQUEST_TD-AXIOM-GIT-PROVENANCE_S3_BASELINE_DIFF_SEMANTICS.md`. No D-3 index removal, staging, commit, tag, hook activation, or history operation occurs until the baseline-diff proof and the related W-8 closure-record form are reconciled.
