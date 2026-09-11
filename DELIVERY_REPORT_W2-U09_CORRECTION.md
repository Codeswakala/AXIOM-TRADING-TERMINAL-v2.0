# Delivery Report — W2-U09 Correction Response

| Field | Value |
|-------|-------|
| Parent unit | **W2-U09** Economic Validation Framework |
| Trigger | `docs/build-orders/ITRGA_REVIEW_W2-U09.md` — CONDITIONAL, C-1 only + MEDIUM process finding |
| Date | 2026-07-15 |
| Author | Development Authority |
| Status | **C-1 evidence command pack supplied; operator persistence proof pending** |
| Approval | **Not self-approved** |

---

## 1. Verdict acknowledgement

The Development Authority accepts ITRGA's W2-U09 review.

ITRGA accepted all economic-validation functionality and evidence except the persisted PostgreSQL economic-report proof. ITRGA also recorded a MEDIUM process finding because this persisted-artifact capture gap recurred after the standing instruction.

The required correction is narrow:

> C-1 — persist one economic report on PostgreSQL using `EconomicValidationService`, commit it, then `SELECT` the `economic_reports` row and its `economic_report` audit event.

---

## 2. Correction supplied

Created:

`docs/evidence/W2-U09_C1_ECONOMIC_PERSISTENCE_COMMANDS.md`

This command pack creates the full pinned chain needed by the service:

1. frozen dataset snapshot;
2. split manifest;
3. approved experiment;
4. research-only model artifact;
5. validation report;
6. calibration report;
7. economic report through `EconomicValidationService.validate(...)`;
8. commit;
9. `psql SELECT` for `economic_reports`;
10. `psql SELECT` for `audit_events` with `resource_type='economic_report'`.

The script is explicitly economic-report focused and does not use the W2-U08 calibration proof script.

---

## 3. Expected closure evidence

The operator output should show:

```text
economic_reports: at least 1 row
experiment_id = operator-economic-proof-...
research_status = research_only
report_hash present
statistical_conclusion present
economic_conclusion present
scenario_results present
cost_model present

audit_events: at least 1 row
action = economic.report_created
resource_type = economic_report
experiment_id = operator-economic-proof-...
```

---

## 4. Process note response

The MEDIUM process finding is acknowledged. Going forward, every unit that introduces a new persisted artifact/report type must include a first-submission committing script and `SELECT >= 1 row` proof for that artifact type.

---

## 5. Current disposition

> W2-U09 remains conditional on C-1 only.  
> No code change is expected.  
> DA does **not** self-approve.  
> W2-U10 must not begin until ITRGA accepts the C-1 persistence proof and approves W2-U09.

---

**End of W2-U09 Correction Response**
