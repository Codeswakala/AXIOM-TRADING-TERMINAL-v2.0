# ADR-042 — Regime Detection Reports

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U03; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U03 |
| Related | W4-U01 artifact contract, W4-U02 persistence/audit standard, D-W2-001 Option A |

## Context

W4-U03 adds Regime Detection Reports as research context. The risk is that a regime label could become a hidden signal, learn symbol identity, leak future data, or imply certainty without evidence.

## Decision

AXIOM implements persisted `regime_reports` and an explainable rule-based `RegimeReportService`.

The service:

- reads persisted candles read-only;
- uses backward-looking windows with `open_time >= as_of_start` and `open_time <= as_of_end`;
- counts excluded future candles;
- computes normalized trend and volatility features;
- excludes symbol/provider/market identity from features;
- classifies regimes with transparent thresholds;
- returns label, confidence, uncertainty, evidence, thresholds, and limitations;
- persists the report;
- writes `regime_report.created` audit event;
- exposes authenticated read-only list/detail APIs.

## Regime labels

Initial explainable rule labels:

```text
trend
volatile
calm
range
```

## Non-decisions

W4-U03 does not add:

- learned/clustering model;
- per-market specialized model;
- UI;
- signal emission;
- trade instruction;
- economic edge assessment;
- execution/broker/order behavior.

## Persistence

Alembic revision:

```text
20260716_0020_w4_u03_regime_reports.py
```

The persistence-capture control applies. Operator evidence must include raw `SELECT >= 1 row` from `regime_reports`, matching audit event, and no-orphan proof.

## Review note

DA does not self-approve this ADR or W4-U03. Acceptance requires operator target evidence and ITRGA review.
