# ADR-040 — Wave-4 Institutional Intelligence Foundation and Scientific Dependency Policy

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U01; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U01 |
| Related | TD-065, Wave-4 guardrails GR-1…GR-8, D-W2-001 Option A, `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` |

## Context

Wave 4 expands institutional analytical capability. Before any analytical feature is built, AXIOM needs a foundation for two risks:

1. compiled scientific dependency compatibility on the operator target platform; and
2. a common inert intelligence artifact/report contract with lineage, uncertainty, audit correlation, and no action payload.

W4-U01 is a foundation unit only. It does not implement a correlation, regime, scenario, portfolio/risk, or signal-validation feature.

## Decision

AXIOM creates the `institutional_intelligence` backend bounded context and a common `IntelligenceArtifactContract`.

The contract includes:

```text
artifact_id
created_at UTC
artifact_type
method_version
config
input_lineage
source_artifact_ids
market_scope
as_of_start
as_of_end
sample_count
uncertainty
results
limitations
report_hash
research_status
created_by
audit_correlation_id
```

The contract is inert. It rejects action/remediation payload fields such as:

```text
order_payload
order_intent
execution_payload
remediation_payload
broker_account_id
quantity
stop_loss
take_profit
auto_retrain
retrain_triggered
```

AXIOM also adds pure-Python fallback primitives for mean and Pearson correlation so early Wave-4 work can proceed with a governed fallback if compiled dependencies fail or remain unapproved.

## Scientific dependency policy

Candidate dependencies for W4-U01 evidence:

```text
numpy
pandas
scipy
```

`scikit-learn` is not adopted in W4-U01. Any future use requires a separate compatibility spike or explicit authorization.

No compiled scientific dependency is added to runtime project dependencies in W4-U01. No application code imports `numpy`, `pandas`, `scipy`, or `sklearn` until operator target evidence passes and ITRGA accepts the dependency decision.

The operator evidence pack runs an isolated install/import/smoke spike and records resolved versions. The spike is file-recorded, not persisted in a database table.

## Persistence decision

W4-U01 adds no new persisted artifact/report table. Therefore no Alembic migration is added and the persistence-capture control is not triggered for a new table.

Future Wave-4 persisted reports must each use Alembic and provide first-submission committing script + raw `psql SELECT >= 1 row` + audit event evidence.

## Consequences

### Positive

- Wave 4 has a bounded context before features.
- Artifact lineage/uncertainty/audit fields are standardized.
- The artifact contract structurally rejects action/remediation payloads.
- A pure-Python fallback exists if compiled dependencies fail.
- TD-065 can be discharged through target evidence before any compiled dependency is adopted.

### Deferred

- Actual correlation/regime/scenario/risk reports are deferred to later Wave-4 Build Orders.
- Persisted scientific dependency spike table is not added; file evidence is used.
- Compiled dependency adoption is pending target operator evidence and ITRGA review.

## Review note

DA does not self-approve this ADR or W4-U01. Acceptance requires operator target evidence and ITRGA review.
