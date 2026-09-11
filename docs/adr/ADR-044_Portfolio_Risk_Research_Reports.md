# ADR-044 — Portfolio/Risk Research Reports

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U05; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U05 |
| Related | W4-U01 artifact contract, W4-U04 scenario reports, GR-1…GR-8, R-8 no account/broker/position linkage |

## Context

W4-U05 introduces portfolio/risk-style analytics as hypothetical market-series research. The primary risk is that "portfolio risk" drifts into real account, broker, or position linkage.

## Decision

AXIOM implements persisted `portfolio_risk_reports` and `PortfolioRiskReportService`.

The service:

- reads persisted market candles read-only;
- uses as-of-bounded windows with no future data;
- computes market-series risk metrics such as max drawdown, realized volatility, and stress-loss-style metric;
- stores per-metric uncertainty and sample count;
- stores hypothetical assumptions and limitations;
- stores independent economic usefulness verdict;
- persists the report and writes `portfolio_risk_report.created` audit event;
- exposes authenticated read-only list/detail APIs.

## R-8 decision

The report is market-series research only. It has no real account, broker, live position, order, or sizing linkage.

No columns or fields are added for account identifiers, broker identifiers, position identifiers, holdings, order payloads, execution payloads, quantities, order size, or position size.

## Non-decisions

W4-U05 does not add UI, real portfolio/account integration, signal validation, order sizing, signal emission, execution, broker integration, or guaranteed-return framing.

## Persistence

Alembic revision:

```text
20260716_0022_w4_u05_portfolio_risk_reports.py
```

The persistence-capture control applies. Operator evidence must include raw `SELECT >= 1 row` from `portfolio_risk_reports`, matching audit event, and no-orphan proof.

## Review note

DA does not self-approve this ADR or W4-U05. Acceptance requires operator target evidence and ITRGA review.
