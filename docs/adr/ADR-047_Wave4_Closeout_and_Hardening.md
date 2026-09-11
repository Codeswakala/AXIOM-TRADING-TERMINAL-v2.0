# ADR-047 — Wave-4 Closeout and Hardening

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U08; pending ITRGA closeout review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U08 |
| Related | W4-U01 through W4-U07, Wave-4 guardrails GR-1…GR-8 |

## Context

Wave 4 introduced Institutional Intelligence: foundation contracts, correlation reports, regime reports, scenario reports, portfolio/risk reports, professional signal validation reports, and a presentation-only dashboard. W4-U08 is a closeout and hardening unit, not a feature unit.

The W4-U07 final verdict carried OBS-1: numeric uncertainty interval bounds were present in report JSON but displayed as em-dashes in the dashboard summary. W4-U08 closes that display binding issue and provides full-wave evidence for safety, audit completeness, auth/read-only behavior, no execution, and docs/register reconciliation.

## Decision

W4-U08 performs the following:

- fixes dashboard interval-bound rendering for nested metric uncertainty data;
- adds test coverage proving nested interval bounds render numerically;
- provides Wave-4 Closeout Evidence Index;
- provides operator evidence commands for full-wave closeout;
- reconciles documentation and registers to platform v0.38.0.

## Non-decisions

W4-U08 does not add:

- new analytical capability;
- new report type;
- new backend endpoint;
- schema migration;
- execution/order/broker/account/position/sizing path;
- auto-retrain or auto-remediation;
- Wave-5/6 functionality.

## Consequences

### Positive

- W4 dashboard shows numeric interval bounds rather than em-dashes when persisted data contains bounds.
- W4 has a single traceable evidence index for ITRGA milestone review.
- Closeout proof covers all five W4 report families.

### Deferred

- Detailed per-report drill-down remains future UI work.
- Any execution/broker/account integration remains out of scope and governance-gated.

## Review note

DA does not self-approve W4-U08 or declare the Institutional Intelligence Layer Complete milestone. Acceptance and milestone declaration remain ITRGA authority.
