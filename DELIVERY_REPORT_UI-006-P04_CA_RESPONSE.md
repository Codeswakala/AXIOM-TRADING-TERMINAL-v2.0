# DELIVERY REPORT — UI-006-P04 CORRECTIVE ACTION RESPONSE

## R-7 Persistence-Capture Correction

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P04 corrective response** |
| Original Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P04.md` |
| ITRGA review | `docs/build-orders/ITRGA_REVIEW_UI-006-P04.md` |
| Determination being addressed | Corrective Actions Required |
| DA status | Corrective evidence package prepared; not self-approved |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Corrective finding summary

ITRGA determined UI-006-P04 requires corrective action because the first mutation phase did not satisfy the mandatory R-7 raw PostgreSQL persistence-capture control.

Blocking finding:

```text
collection create raw psql row-content SELECT: missing
membership add raw psql SELECT: returned 0 rows = disproof
membership remove claim: contradicted by transcript because before count was 0
```

The issue is evidence completeness and report/transcript reconciliation. ITRGA did not identify a constitutional source-code defect: named tests, no-underlying-artifact-mutation proof, forbidden-column schema proof, no-actuation/no-recompute greps, no-drift, frontend regression, backend regression, browser posture, and Doc 16 posture were otherwise clean.

---

## 2. Corrective package produced

Prepared:

```text
docs/evidence/UI-006-P04_CA_PERSISTENCE_CAPTURE_COMMANDS.md
```

This command pack is designed to produce a fresh UI-006-P04 attempt-2 evidence transcript with:

```text
collection row proof
membership row proof
operator_id -> operators.id no-orphan join
forbidden_org_column_count = 0
source scenario artifact before/after unchanged
membership remove before=1 and after=0 if removal is exercised
alembic current = 20260717_0037 (head)
```

---

## 3. CA-P04-1 — collection create persistence proof

The corrective commands require a fresh, exact collection name:

```text
UI006 P04 CA Collection <timestamp>
```

The operator must create that exact collection in the served `/research-management` UI and then run raw PostgreSQL proof:

```text
SELECT collection_id, name, description, operator_id, joined_operator_id, research_status, audit_correlation_id
FROM research_collections JOIN operators ...
WHERE collection_id = '<created collection id>';
```

The expected raw PostgreSQL proof is:

```text
collection_rows >= 1
operator_id -> operators.id join present
research_status = research_only
```

---

## 4. CA-P04-2 — membership add persistence proof

The corrective commands require the operator to select the exact scenario report id printed by the script:

```text
UI006_P04_CA_SOURCE_SCENARIO_ID
```

The membership row proof then uses both the actual collection id and the scenario id:

```text
SELECT member_id, collection_id, artifact_type, artifact_id, operator_id, joined_operator_id, audit_correlation_id
FROM research_collection_members JOIN operators ...
WHERE member_id = '<created member id>';
```

Expected raw PostgreSQL proof:

```text
member_rows_after_add = 1
artifact_type = scenario_report
artifact_id = UI006_P04_CA_SOURCE_SCENARIO_ID
operator_id -> operators.id join present
```

The command pack includes diagnostics if the row is not found, so a repeat of the attempt-1 silent mismatch is not accepted.

---

## 5. CA-P04-3 — member-reference removal proof

If removal is exercised, the corrective commands require before/after raw PostgreSQL counts on the same member id:

```text
member_before_remove = 1
member_after_remove = 0
```

Attempt-1 showed `member_before_remove = 0`; the corrective pack makes that condition a blocking failure rather than a claim.

---

## 6. CA-P04-4 — report/transcript reconciliation

This corrective response does not claim that persistence has been proven until the fresh corrective transcript returns populated raw rows.

Attempt-1 report claims contradicted transcript results. Attempt-2 must use the raw psql transcript as the source of truth.

---

## 7. Clean items carried from attempt-1

ITRGA stated the following clean items carry forward unless it requests a rerun:

```text
5 named tests displayed passing
M-1/M-2 no-underlying-artifact mutation for source scenario row
M-3 forbidden org-column schema audit = 0
empty-collection delete explicitly out of scope
no-drift / no new migration
frontend full suite 53f/236t with FRONTEND_VITEST_EXIT_CODE: 0
backend 414 passed
Doc 16 brand and browser posture
TD-W6-CI-AUDIT env-flake waived after substantive gates green
```

The corrective pack still includes source-artifact before/after proof because it is directly tied to the new persisted membership row.

---

## 8. DA disposition

DA submits this corrective action response and command pack for operator execution.

DA does not self-approve UI-006-P04.

UI-006-P05 is not authorized until ITRGA approves or approves-with-observations the corrected UI-006-P04 evidence.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of DELIVERY_REPORT_UI-006-P04_CA_RESPONSE.md**
