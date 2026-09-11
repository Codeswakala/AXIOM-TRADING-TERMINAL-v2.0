# Delivery Report — W4-U02 Correction Response

| Field | Value |
|---|---|
| Unit | W4-U02 Correlation Intelligence Reports |
| ITRGA review | `docs/build-orders/ITRGA_REVIEW_W4-U02.md` |
| Verdict | Conditional approval |
| Conditions | C-1 raw SELECT + no-orphan audit proof; C-2 detail endpoint proof |
| DA response | Evidence correction pack only; no implementation change |
| Date | 2026-07-16 |

---

## 1. Summary

ITRGA conditionally approved W4-U02. Core function is approved: no-look-ahead, uncertainty, non-signal behavior, dependency discipline, read-only list API, full regression, and CI are proven.

Two evidence gaps remain:

1. C-1: raw `psql SELECT >= 1 row` from `correlation_reports` plus matching audit/no-orphan proof was not run.
2. C-2: detail endpoint was not proven due an evidence script path placeholder.

No code change is required. DA created a targeted correction command pack.

---

## 2. Correction evidence file

Use:

```text
docs/evidence/W4-U02_C1_C2_CORRECTION_COMMANDS.md
```

It provides exact commands for:

- raw `correlation_reports` SELECT by report id;
- audit join proof for `correlation_report.created`;
- orphan audit count expected `0`;
- authenticated detail endpoint `GET /api/v1/intelligence/correlation-reports/{report_id}` with `DETAIL_STATUS: 200`;
- detail fields: sample count, uncertainty method, economic verdict, limitations.

---

## 3. DA non-approval statement

DA does not self-approve W4-U02. W4-U02 remains conditionally approved until operator correction evidence is run and ITRGA issues a final approval verdict.

DA will not begin W4-U03 without ITRGA final approval and a new Build Order.

---

**End of W4-U02 Correction Response**
