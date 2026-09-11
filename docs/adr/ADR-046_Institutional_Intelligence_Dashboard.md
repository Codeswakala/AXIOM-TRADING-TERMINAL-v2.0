# ADR-046 — Institutional Intelligence Dashboard

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U07; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U07 |
| Related | W4-U02..W4-U06 read-only APIs, W3-U05 UI precedent, GR-8 presentation-only |

## Context

W4-U07 is the first Wave-4 operator-facing UI. It displays persisted Institutional Intelligence research reports: correlation, market context/regime, hypothetical scenario, market-series risk, and signal validation reports.

The key risks are execution-control leakage, client-side authoritative recomputation, false precision, raw score display, and guaranteed-return framing.

## Decision

AXIOM implements a protected `/intelligence` route that displays Institutional Intelligence reports from existing read-only APIs.

The dashboard:

- reads existing W4 APIs;
- formats persisted data only;
- displays uncertainty and sample counts;
- displays research/not-guaranteed disclaimer;
- displays limitations/evidence from persisted report payloads;
- sanitizes uncalibrated raw-score keys if ever present in nested payloads;
- provides no execution controls;
- provides no signal/action affordance;
- performs no client-side authoritative recomputation.

## API sources

```text
GET /api/v1/intelligence/correlation-reports
GET /api/v1/intelligence/regime-reports
GET /api/v1/intelligence/scenario-reports
GET /api/v1/intelligence/portfolio-risk-reports
GET /api/v1/intelligence/signal-validation-reports
```

No new backend endpoint or persisted artifact is added in W4-U07.

## Non-decisions

W4-U07 does not add:

- backend analytical computation;
- persisted artifact/report type;
- execution/order/broker controls;
- signal emission;
- raw score rendering;
- guaranteed-return framing;
- Wave-4 closeout.

## Review note

DA does not self-approve this ADR or W4-U07. Acceptance requires operator evidence, browser screenshots, and ITRGA review.
