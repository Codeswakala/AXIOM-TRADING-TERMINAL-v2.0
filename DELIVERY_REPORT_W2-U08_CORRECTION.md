# Delivery Report — W2-U08 Correction Response

| Field | Value |
|-------|-------|
| Parent unit | **W2-U08** Calibration + Probability Quality Framework |
| Trigger | `docs/build-orders/ITRGA_REVIEW_W2-U08.md` — CONDITIONAL, C-1 only |
| Date | 2026-07-14 |
| Author | Development Authority |
| Status | **C-1 evidence command pack supplied; operator persistence proof pending** |
| Approval | **Not self-approved** |

---

## 1. Verdict acknowledgement

The Development Authority accepts ITRGA's W2-U08 review.

ITRGA accepted all functional/calibration evidence except one mandatory item:

> C-1 — persisted PostgreSQL calibration report + audit event proof.

The existing operator run showed all tests, migration, miscalibration detection, base-rate null, CI, and parity smoke. The only missing artifact is a committing PostgreSQL proof that a calibration report and its audit event live on disk.

---

## 2. Correction supplied

Created:

`docs/evidence/W2-U08_C1_CALIBRATION_PERSISTENCE_COMMANDS.md`

This command pack provides a copy-paste PowerShell/Python script that:

1. creates a frozen dataset snapshot;
2. creates a temporal split manifest;
3. creates/pre-registers/approves an experiment;
4. creates a research-only model artifact;
5. creates a validation report;
6. calls `CalibrationService.calibrate(...)`;
7. commits the session;
8. prints report id/hash/Brier/ECE/base-rate details;
9. runs `psql SELECT` against `calibration_reports`;
10. runs `psql SELECT` against `audit_events` for `calibration.report_created`.

---

## 3. Expected closure evidence

The required ITRGA evidence should show:

```text
calibration_reports: at least 1 row
experiment_id = operator-calibration-proof-...
research_status = research_only
report_hash present
brier_score present
expected_calibration_error present
base_rate_significance present

audit_events: at least 1 row
action = calibration.report_created
resource_type = calibration_report
experiment_id = operator-calibration-proof-...
```

---

## 4. Current disposition

> W2-U08 remains conditional on C-1 only.  
> No code change is expected.  
> DA does **not** self-approve.  
> W2-U09 must not begin until ITRGA accepts the C-1 persistence proof and approves W2-U08.

---

**End of W2-U08 Correction Response**
