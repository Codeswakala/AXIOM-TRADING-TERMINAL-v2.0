# DELIVERY REPORT — UI-003 ENGINEERING DESIGN PLAN

## Professional Market Workspace

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Trigger | `docs/build-orders/ITRGA_REQUEST_UI-003_DESIGN_PLAN.md` |
| Predecessor milestones | UI-001 COMPLETE · UI-002 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Backend baseline | 414 passed |
| Frontend baseline | 31 files / 127 tests |
| DA status | Design plan produced; implementation not started |
| Approval status | Not self-approved; pending ITRGA design review |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Documents reviewed and recorded

Recorded ITRGA final completion review:

```text
docs/build-orders/ITRGA_REVIEW_UI-002-P05_FINAL_AND_UI-002_COMPLETION.md
```

Recorded ITRGA design-plan request:

```text
docs/build-orders/ITRGA_REQUEST_UI-003_DESIGN_PLAN.md
```

Key determinations accepted into DA programme state:

```text
UI-002-P05: APPROVED
UI-002: COMPLETE
UI-003: Engineering Design Plan requested only
UI-003 implementation: NOT AUTHORIZED until accepted plan + Build Order
Production deployment: NOT CERTIFIED
Governance Gate: CLOSED
```

---

## 2. Deliverable produced

Created:

```text
docs/plans/UI-003_ENGINEERING_DESIGN_PLAN.md
```

The design plan covers the ITRGA-requested areas:

1. objective and Doc 12 §5 scope mapping;
2. presentation-only bright-line controls;
3. UI-001/UI-002 reconciliation table and UI-009 dependency status;
4. professional market workspace architecture;
5. data-source table proving existing read/governed sources only;
6. watchlist persistence decision using existing `operator_workspace_preferences`;
7. chart overlays, research markers, and annotation integration strategy;
8. accessibility plan for chart/market/watchlist surfaces;
9. responsive and layout plan;
10. UI-003-P01 through UI-003-P05 phase decomposition with named test anchors;
11. regression and evidence strategy;
12. risks, mitigations, and open questions;
13. recommended first Build Order.

---

## 3. Watchlist persistence decision

The design plan proposes the preferred ITRGA option:

```text
Reuse operator_workspace_preferences
```

No new watchlist table is proposed.

Watchlists are modeled as presentation preferences containing symbol/timeframe identifiers only. They shall not store positions, quantities, orders, accounts, balances, margin, capital, allocation, stop/target fields, broker metadata, or P&L.

---

## 4. Implementation status

No UI-003 implementation was started.

No frontend source files were changed for UI-003 implementation.

No backend source files were changed.

No API contract, database schema, governance behavior, ML workflow, business logic, trading capability, execution path, broker path, account path, external AI/LLM path, dynamic plugin path, or dependency was changed.

No tests were run because this is a design-plan-only response.

---

## 5. DA recommendation

If ITRGA accepts the design plan, the recommended first implementation Build Order is:

```text
UI-003-P01 — Professional Market Workspace Frame, Existing Data-Source Inventory, and Non-Authoritative Market Presentation
```

The rationale is to prove chart-centered composition inside UI-001/UI-002 before watchlist persistence or overlay expansion.

---

## 6. Governance statement

DA does not self-approve this design plan and does not authorize UI-003 implementation.

Implementation may begin only after ITRGA accepts the design plan and issues or authorizes a controlled Build Order.

The Governance Gate remains CLOSED.

Production deployment remains NOT CERTIFIED under `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md`.

---

**End of DELIVERY_REPORT_UI-003_DESIGN_PLAN.md**
