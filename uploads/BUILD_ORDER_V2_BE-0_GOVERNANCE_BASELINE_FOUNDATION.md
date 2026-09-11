# BUILD ORDER — AXIOM V2 BE-0: Governance, Baseline and Architecture Foundation

| Field | Value |
|---|---|
| Build Order ID | BO-V2-BE-0-001 |
| Issued by | Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-08-23 |
| Status | **AUTHORIZED FOR DA EXECUTION** |
| Governing plan | `AXIOM-V2-BE-0-DA-PLAN-001`, v2.0.0; ITRGA review `ITRGA-REV-V2-BE-0-002` |
| Governing constraints | Active V1 hierarchy; `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` |
| Scope | Governance, provenance, architecture-principles, and regression-baseline artifacts only |

---

## 1. Authority and boundary

This Build Order authorizes BE-0 documentation/baseline work under the **still-active V1 governance framework**. It does not activate V2 as a programme, amend V1, or authorize a V2 feature.

The DA may draft the V2 Programme Charter. The draft is not active until the Operator explicitly approves it. Any Charter provision amending a V1 rule must identify the exact V1 document/section, prior rule, replacement rule, effective scope, approval, and V2 amendment-register entry.

## 2. Objective

Create a controlled, reproducible V2 governance and provenance baseline while preserving V1 historical truth and supported behavior.

## 3. In scope

1. Copy the approved corrected BE-0 plan into `docs/plans/V2_BE-0_DESIGN_PLAN.md` without substantive alteration.
2. Capture the V1 regression baseline at parent commit:
   ```text
   9ab91e76b3ac5f6a42c3066f022700489c214a29
   ```
3. Create the following additive artifacts:
   - `docs/governance/V2_PROGRAMME_CHARTER.md` — **DA draft only; Operator approval pending**;
   - `docs/governance/V2_AMENDMENT_REGISTER.md` — initialized empty with required entry format;
   - `docs/governance/V2_PROVENANCE_RECORD.md`;
   - `docs/governance/V2_ARCHITECTURE_PRINCIPLES.md` — binding Research/Simulation principles only, plus clearly non-binding deferred candidates;
   - `docs/governance/V2_CAPABILITY_MATURITY.md`;
   - `docs/governance/V2_RISK_REGISTER.md`;
   - `docs/governance/V2_TECHNICAL_DEBT_REGISTER.md`;
   - `docs/governance/V2_ADR_CONVENTION.md`;
   - `V2_CURRENT_STATE.md`;
   - `docs/evidence/V1_REGRESSION_BASELINE.md`.
4. Record exact command output and environment information for backend tests, frontend tests, TypeScript build, frontend production build, and Alembic state.
5. Create tag `AXIOM_V2_BE0_BASELINE` only after all BE-0 artifacts and baseline evidence are complete; record tag and SHA in the provenance record.
6. Produce `DELIVERY_REPORT_V2_BE-0.md` with artifact inventory, exact evidence paths, test/build outcomes, known limitations, risks/debt, and no-scope-expansion statement.

## 4. Mandatory constraints

- Do not modify existing V1 source, tests, migrations, APIs, configuration, dependency manifests, or historical governance/evidence records.
- Do not implement any runtime/backend/frontend feature.
- Do not add provider, broker, exchange, account, balance, position, order, fill, paper-trading, execution, external-AI, or production capability.
- Do not create credentials, make external connections, claim real data, or claim production/certification status.
- BE-0 may define and reference only active `RESEARCH` and `SIMULATION` mode scope. Paper/Live are future deferred candidates, not BE-0 designs.
- Do not treat the V2 Programme Charter as active before Operator approval.
- Do not add a duplicate V2 document-precedence policy; use the existing `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`.

## 5. Required evidence

### Level I

- `git rev-parse HEAD` / parent-baseline recording;
- Alembic-head evidence;
- complete artifact file inventory;
- `git diff --name-only` and suitable diff evidence showing only authorized additive BE-0 artifacts;
- baseline tag name and resolved SHA.

### Level II

- full captured backend test output;
- frontend test output;
- TypeScript compilation output;
- frontend production-build output;
- Alembic upgrade/check output, with environment/preconditions recorded.

### Level III

- Charter draft, architecture principles, amendment register, provenance/current-state/risk/debt/maturity/ADR artifacts, and Delivery Report.

## 6. Acceptance criteria

BE-0 is ready for ITRGA review only when:

1. all in-scope artifacts exist and satisfy their stated completion conditions;
2. V1 baseline parent SHA, migration head, test-file inventory, environment, commands, and executed outcomes are recorded accurately;
3. all applicable V1 regression/type/build/migration checks pass, or each exception is explicitly evidenced and classified;
4. the Charter is plainly labelled **DRAFT — Operator approval required**;
5. the V2 Amendment Register is empty and no V1 rule is represented as amended;
6. the architecture artifact separates binding Research/Simulation principles from non-binding future candidates;
7. Git evidence demonstrates no prohibited V1 code/schema/configuration/history modification;
8. the tag resolves to the documented BE-0 completion SHA;
9. Delivery Report and V2 Current State are synchronized.

## 7. Completion and next authorization state

DA must submit the Delivery Report and evidence package for independent ITRGA review. Completion of BE-0 does not authorize BE-1 or any V2 capability. The Operator’s explicit Charter decision remains required before V2 programme activation or any V1 amendment.
