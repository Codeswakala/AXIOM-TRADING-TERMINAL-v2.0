# ITRGA Amendment — BO-V2-BE-0-001 Repository Custody and Git Operations

| Field | Value |
|---|---|
| Amendment ID | ITRGA-AMD-BO-V2-BE-0-001-RC1 |
| Status | Active |
| Date | 2026-08-23 |
| Amends | `BUILD_ORDER_V2_BE-0_GOVERNANCE_BASELINE_FOUNDATION.md` |
| Authority | Operator repository-custody clarification `AXIOM-V2-GOV-CUSTODY-001` |

---

## 1. Purpose

This amendment aligns BO-V2-BE-0-001 with the Operator’s clarification that all GitHub/Git operations belong exclusively to the Operator.

## 2. Replaced Build Order requirements

The following requirements are replaced:

### Original §3 item 5

> Create tag `AXIOM_V2_BE0_BASELINE` only after all BE-0 artifacts and baseline evidence are complete; record tag and SHA in the provenance record.

### Replacement

> **Operator action:** After the DA has completed the authorized BE-0 artifact set and supplied its Delivery Report/evidence package, the Operator may create/publish tag `AXIOM_V2_BE0_BASELINE` at the selected completion commit. The Operator must supply the resulting tag/ref/SHA evidence to the ITRGA review corpus. The DA does not create tags, commits, pushes, pulls, branches, or other GitHub/Git state.

### Original §5 Level I Git/tag evidence

> `git rev-parse HEAD` / parent-baseline recording; Alembic-head evidence; complete artifact file inventory; `git diff --name-only` and suitable diff evidence; baseline tag name and resolved SHA.

### Replacement

> The DA supplies the authored artifact inventory, local command output, and stated parent/baseline identifiers. The Operator supplies all Git/GitHub evidence, including commit/tag/ref/diff/branch/remote evidence, to the ITRGA review corpus. ITRGA treats unsupplied repository state as NOT PROVEN, not false.

### Original §6 acceptance criterion 7–8

> Git evidence demonstrates no prohibited V1 code/schema/configuration/history modification; the tag resolves to the documented BE-0 completion SHA.

### Replacement

> Before final BE-0 closure, the Operator must supply repository evidence demonstrating the committed/published scope and, if the Operator elects to create the baseline tag, the tag target. Until such evidence is supplied, the ITRGA may assess documentation and local test evidence but cannot issue a repository/provenance verification finding.

## 3. Delivery-review effect

The DA is not responsible for the Git/tag evidence requested in ITRGA review `ITRGA-REV-V2-BE-0-DELIVERY-001`. The resubmission shall distinguish:

- **DA correction evidence:** missing provenance artifact, corrected Current State, corrected maturity registry, and direct local command output where available;
- **Operator-supplied repository evidence:** commit/tag/diff/ref/remote publication evidence.

## 4. Unchanged boundaries

This amendment does not authorize any code, schema, provider, broker, paper-trading, execution, account, external-AI, production, or frontend work. It does not reduce the requirement for truthful provenance evidence; it only assigns custody and Git operations to the Operator.

---

**End of Amendment**
