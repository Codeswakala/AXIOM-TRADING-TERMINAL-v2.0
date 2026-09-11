# DELIVERY REPORT — UI-003-P02

## Watchlists via Existing Preferences

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Phase | **UI-003-P02** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-003-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-003-P01.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 32f/132t |
| DA status | Implemented; evidence package prepared; not self-approved |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for:

```text
UI-003-P02 — Watchlists via Existing Preferences
```

It is not a UI-003-P01 report.

This implementation is governed by:

```text
docs/build-orders/BUILD_ORDER_UI-003-P02.md
docs/build-orders/ITRGA_REVIEW_UI-003-P01.md
```

Binding refinements applied:

- **R-1:** watchlists reuse existing `operator_workspace_preferences`; no new table/migration/column.
- **R-2:** operator evidence must include one raw `psql SELECT` read-back of the persisted preference row; API read-back does not substitute.
- **R-4:** reorder controls are deferred because P02 does not implement reorder; watchlist add/remove/focus controls are native keyboard-operable controls.
- **R-6:** presentation-only, no execution/actuation, no backend/schema/dependency drift, Level-I evidence.

---

## 2. Implementation summary

UI-003-P02 implements operator watchlists as presentation preferences in the existing professional market workspace.

Implemented:

1. `marketWatchlists.tsx` preference model and validation;
2. watchlist persistence via existing workspace preference API:

   ```text
   fetchWorkspacePreferences
   createWorkspacePreference
   updateWorkspacePreference
   ```

3. `professional-market-workspace-v1` workspace preference key;
4. watchlist payload containing symbol/timeframe identifiers only;
5. recursive forbidden-field validation for order/account/broker/execution/P&L/Gate fields;
6. `MarketWatchlistPanel` with keyboard-operable native controls;
7. integration into `/charts` professional market workspace;
8. named UI-003-P02 tests.

No new backend endpoint, schema, migration, column, table, or dependency was introduced.

---

## 3. Files added

```text
frontend/src/market/marketWatchlists.tsx
frontend/src/market/MarketWatchlists.test.tsx
docs/build-orders/ITRGA_REVIEW_UI-003-P01.md
docs/build-orders/BUILD_ORDER_UI-003-P02.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-003-P02.md
docs/evidence/UI-003-P02_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-003-P02.md
```

---

## 4. Files modified

```text
frontend/src/pages/ChartWorkspacePage.tsx
frontend/src/styles/global.css
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

---

## 5. Watchlist persistence model

Preference key:

```text
professional-market-workspace-v1
```

Preference table reused:

```text
operator_workspace_preferences
```

Payload fields:

```text
layout_config.active_symbol
layout_config.active_timeframe
layout_config.watchlists[].watchlist_id
layout_config.watchlists[].name
layout_config.watchlists[].symbols[]
layout_config.watchlists[].timeframes[]
layout_config.overlay_visibility
```

Allowed `visible_modules` use the existing backend allowlist:

```text
chart_workspace
live_market
```

No new table is proposed or implemented.

---

## 6. Forbidden-field validation

The watchlist validator rejects nested fields matching:

```text
quantity
position
order
side
buy
sell
broker
account
balance
margin
capital
allocation
stop_loss
take_profit
stop
target
real_pnl
pnl
open_gate
allow_execution
```

Named test:

```text
test_ui003_watchlists_reject_execution_broker_account_payload_fields
```

---

## 7. Explicitly not added

UI-003-P02 did not add:

- new table;
- migration;
- schema column;
- backend endpoint;
- backend business logic;
- new dependency;
- watchlist quantities;
- positions;
- orders;
- sides;
- broker/account fields;
- balances, margin, capital, allocation;
- stop/target fields;
- P&L fields;
- execution/Gate path;
- chart overlays or research markers;
- external AI/LLM;
- dynamic plugin execution;
- production certification.

---

## 8. Local DA validation

### 8.1 Named UI-003-P02 tests

Command:

```bash
cd frontend
npm test -- --reporter=verbose MarketWatchlists.test.tsx
```

Result:

```text
1 file passed / 5 tests passed
```

Named tests displayed passing:

```text
test_ui003_watchlists_use_operator_workspace_preferences_no_new_table
test_ui003_watchlists_store_symbol_ids_only_no_positions_orders_or_accounts
test_ui003_watchlists_reject_execution_broker_account_payload_fields
test_ui003_watchlists_are_keyboard_operable_and_accessible
test_ui003_watchlist_persistence_preserves_alembic_head
```

### 8.2 Frontend regression

Commands:

```bash
cd frontend
npm audit --audit-level=high
npm test -- --reporter=verbose
npx tsc -b --pretty false
npm run build
```

Results:

```text
npm audit: 0 vulnerabilities
Frontend full suite: 33 files / 137 tests passed
TypeScript: clean
Production build: successful
```

Build output:

```text
CSS: 38.23 kB
JS: 492.47 kB
```

Baseline comparison from UI-003-P01:

```text
Frontend tests: 32 files / 132 tests → 33 files / 137 tests
Bundle: CSS 37.81 kB / JS 486.72 kB → CSS 38.23 kB / JS 492.47 kB
Delta: +1 test file / +5 tests; +0.42 kB CSS / +5.75 kB JS
```

### 8.3 Backend regression

Commands:

```bash
cd backend
ruff check .
pytest -q
```

Results:

```text
Ruff: All checks passed!
Backend full suite: 414 passed, 1 warning
```

### 8.4 Alembic head

Temp SQLite Alembic smoke:

```text
alembic current: 20260717_0037 (head)
```

Operator target must still provide the required PostgreSQL-target `alembic current` and raw `psql SELECT` evidence.

---

## 9. R-2 raw psql evidence requirement

Prepared operator command pack includes mandatory raw PostgreSQL read-back:

```text
docs/evidence/UI-003-P02_OPERATOR_EVIDENCE_COMMANDS.md §7
```

Accepted output must show:

```text
workspace_key = professional-market-workspace-v1
layout_config->'watchlists' contains symbols/timeframes only
forbidden_field_present = f
professional_market_watchlist_rows >= 1
```

An API read-back does not substitute for this raw psql proof.

---

## 10. Operator evidence package

Prepared:

```text
docs/evidence/UI-003-P02_OPERATOR_EVIDENCE_COMMANDS.md
```

The command pack covers:

- build identity;
- five named tests displayed passing;
- symbol/timeframe ids only proof;
- forbidden-field validation proof;
- no-actuation source grep;
- no-drift substitute evidence;
- browser watchlist add/remove/keyboard/restore evidence;
- mandatory raw psql read-back;
- frontend/backend regression;
- networked Git-Bash CI with exit-code sentinel.

---

## 11. Constitutional attestation

UI-003-P02 is presentation preference work only.

The implementation:

- reuses existing `operator_workspace_preferences`;
- stores symbol/timeframe identifiers only;
- inherits operator scoping from the existing workspace preference API;
- adds no new table, migration, column, endpoint, backend logic, or dependency;
- introduces no position/order/account/broker/P&L/Gate fields;
- introduces no execution or actuation path;
- introduces no external AI/LLM or dynamic plugin execution;
- keeps the Governance Gate CLOSED;
- does not certify production deployment.

---

## 12. DA disposition

DA submits UI-003-P02 for operator evidence collection and ITRGA review.

DA does not self-approve UI-003-P02.

UI-003-P03 is not authorized until ITRGA approves UI-003-P02 and explicitly authorizes the next Build Order.

---

**End of DELIVERY_REPORT_UI-003-P02.md**
