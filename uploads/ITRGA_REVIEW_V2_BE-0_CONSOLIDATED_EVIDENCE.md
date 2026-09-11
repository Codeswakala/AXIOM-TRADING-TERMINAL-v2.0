# ITRGA Review — AXIOM V2 BE-0 Consolidated Evidence Package

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-0-DELIVERY-003 |
| Submission | Revised Delivery Report, Correction Package, V1 Regression Baseline, and `AXIOM-V2-BE-0-EVIDENCE-002` |
| Prior review | `ITRGA-REV-V2-BE-0-DELIVERY-002` — CORRECTION REQUIRED |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Package structure assessment

A single consolidated evidence package is acceptable and preferred over fragmented uploads **provided it contains internally consistent, traceable command captures**. The repository-custody rule is correctly reflected: no pre-review DA commit/tag/push is required or expected.

The revised Delivery Report and Correction Package have corrected the earlier tag-status contradictions. They now consistently state that the baseline tag is an Operator post-approval action.

## 2. Closed items

| Prior item | Status | Assessment |
|---|---|---|
| Pre-review Git/tag requirement | Closed/superseded | Correctly removed under Operator custody amendment A1 and BO amendment RC2. |
| Baseline-tag wording in Delivery Report | Closed | The revised Delivery Report no longer claims that the tag was created. |
| DA Git/tag claims in Correction Package | Closed | The revised package states that DA performed no Git operations. |
| Missing provenance artifact | Closed | Provenance Record is supplied and aligns with Operator post-approval tag custody. |
| Current State / maturity-registry corrections | Supported from prior submission | Prior submitted revisions resolved the stated stale-state and maturity-definition issues. |

## 3. Findings

### Finding V2-BE0-DEL-008 — Ruff evidence conflicts with the claimed passing V1 baseline

| Field | Detail |
|---|---|
| Severity | High — evidence-integrity and regression-baseline defect |
| Status | Open |
| Observed condition | `V1_REGRESSION_BASELINE.md` and the Delivery Report claim `ruff check` passed with no errors and `ruff format --check` passed with no differences. The consolidated evidence instead says `ruff check` found 33 lint violations and `ruff format --check` found 46 files that would be reformatted. |
| Direct repository context | The reviewed parent repository configuration selects Ruff lint rules `E`, `F`, `I`, and `W` in `backend/pyproject.toml`; no `exit-zero` configuration is present. Under this configuration, the described violations cannot be represented as a normal passing check without an explicitly documented non-default invocation/configuration. |
| Impact | The V1 baseline cannot simultaneously be “all regression checks pass” and have non-zero lint/format violations. This affects the truth of the reported quality baseline. |
| Required correction | Re-run and capture the exact `ruff check app/` and `ruff format --check app/` commands with their literal stdout/stderr and actual shell exit status. Then correct every affected document: either report the checks as failures/inherited baseline exceptions, or supply the exact approved configuration/invocation that makes exit status zero. Do not call violations “warnings” or a check “pass” unless the command’s actual result supports that wording. |
| Closure criterion | Regression Baseline, Delivery Report, Correction Package, and Consolidated Evidence carry one consistent, reproducible lint/format result with a documented exit status. |

### Finding V2-BE0-DEL-009 — Alembic check is reported inconsistently and exception handling is incomplete

| Field | Detail |
|---|---|
| Severity | High — migration baseline integrity |
| Status | Open |
| Observed condition | The consolidated evidence reports `alembic check` result: `FAILED: New upgrade operations detected`, while labelling the command `Exit Code: 0 (command ran)`. The V1 Regression Baseline and Delivery Report present the migration state as passing/clean without disclosing this failed check. |
| Impact | A failed Alembic check can indicate model/migration drift. The assertion that it is a “fresh-database artifact” is a supported inference, not direct proof, and does not satisfy the Build Order requirement to record exceptions accurately. |
| Required correction | Capture literal `alembic check` output and actual shell exit status. Record it consistently as either a passing check or an inherited/environment-specific exception. If exception, document the exact model/table/index delta, why it occurs, whether it exists at the V1 parent baseline, risk classification, and a bounded follow-up/debt or risk record. Do not report a failed command as passing merely because the process continued. |
| Closure criterion | The migration baseline has a true command result, an evidence-backed explanation for any exception, and synchronized documentation/risk treatment. |

### Finding V2-BE0-DEL-010 — Consolidated evidence provides summaries, not the claimed full command captures

| Field | Detail |
|---|---|
| Severity | Medium — Level-II evidence completeness gap |
| Status | Open |
| Observed condition | The package provides commands, result summaries, selected tails, and claimed exit codes. It does not include full captured output or an indexed evidence annex for each command. The package describes itself as containing “all 9 command captures,” but the attached document contains abbreviated excerpts. |
| Required correction | Keep one consolidated upload, but make it an actual evidence bundle: include each complete capture as an appendix/section or provide a manifest with immutable local artifact filenames, SHA-256 hashes, command, working directory, environment, start/end time, and literal exit status. Full verbose test listing is not required in the review body if a complete raw log artifact is indexed and supplied. |
| Closure criterion | Each asserted Level-II result is traceable to an intact supplied capture rather than a DA summary alone. |

## 4. Required focused re-submission

One consolidated evidence package remains acceptable. It must contain:

1. literal Ruff check and format command captures with actual exit statuses;
2. literal Alembic check capture with actual exit status and exception classification, if non-zero;
3. synchronized revisions to Delivery Report, Regression Baseline, and Correction Package;
4. an evidence manifest/annex for pytest, vitest, TypeScript, frontend build, Ruff, Alembic heads, Alembic upgrade, and Alembic check.

No Git operation, code change, migration, provider/broker/account/paper/execution/AI work, configuration change, or frontend work is authorized by this correction.

## 5. Determination

**CORRECTION REQUIRED.** The package organization and post-approval Git custody treatment are acceptable. BE-0 cannot close until the V1 regression and migration baseline evidence is internally truthful, technically reproducible, and complete at the claimed evidence level.
