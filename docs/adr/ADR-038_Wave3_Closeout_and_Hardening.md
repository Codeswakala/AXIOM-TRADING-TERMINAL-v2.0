# ADR-038 — Wave-3 Closeout and Hardening

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U08; pending ITRGA closeout review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W3-U08 |
| Related | W3-U01 through W3-U07, W3-U08 Build Order, `WAVE3_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` |

## Context

Wave 3 assembled the Live Research Advisor: deterministic governed inference, advisory signal persistence, emit-time guardrails, live-market inference adapter, operator signal UI, monitoring alerts, and advisory analytics. W3-U08 is not a feature unit. It is a closeout proof unit whose purpose is to reconcile evidence, documentation, risks, debt, and structural safety guarantees before ITRGA may declare the Professional Advisor Platform Complete milestone.

## Decision

AXIOM performs W3-U08 as a closeout and hardening unit.

The closeout requires:

- build identity proof;
- full backend/frontend regression proof;
- local CI completion marker and explicit exit code;
- Alembic head proof;
- browser E2E screenshots across operator surfaces;
- signal and alert audit completeness proof;
- wave-wide no-execution/no-auto-action grep;
- auth/read-only proof for Wave-3 endpoints;
- docs/register reconciliation;
- Wave-3 Closeout Evidence Index.

A small hardening correction is accepted: the Operations dashboard now includes a read-only monitoring alert panel so W3-U08 browser evidence can show an operator alert surface. The panel has no acknowledge, remediation, execution, broker, order, or action control; it only displays existing inert alert records returned by the authenticated alerts API.

## Non-decisions

W3-U08 does not add:

- execution;
- broker connection;
- order payload;
- paper trading;
- position management;
- auto-retraining;
- auto-remediation;
- external provider/feed integration;
- Wave-4+ features.

## Consequences

### Positive

- The whole Wave-3 chain has one traceable closeout evidence index.
- Operator evidence commands explicitly prove audit completeness and no-execution across the wave.
- Alert browser evidence is possible without creating an action surface.
- Documentation and registers are reconciled to the current platform state.

### Deferred / carried forward

- TD-063 persisted analytics snapshot artifact remains future work if needed.
- TD-064 advanced outcome/return attribution remains future work requiring a governed outcome data contract.
- TD-065 compiled advanced ML wheel compatibility spike remains future work for a compiled-ML unit.
- Execution remains Wave 6 only.

## Review note

DA does not self-approve W3-U08, Wave 3, or the Professional Advisor Platform Complete milestone. Acceptance and milestone declaration remain ITRGA authority.
