# Delivery Report — W3-U04

| Field | Value |
|---|---|
| Build Order | **W3-U04** Live Market Inference Adapter |
| Platform | **0.26.0** |
| Wave | **3 — Live Research Advisor** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-15 |

---

## 1. Executive Summary

W3-U04 implements the Live Market Inference Adapter. It feeds live/near-real-time candles from the existing W1 simulated live-market persistence/query seam into the W3-U01 deterministic inference engine and W3-U02/W3-U03 governed signal path.

The headline control is implemented: **a future candle cannot enter the inference input**. The adapter builds a point-in-time inference window using only candles with `open_time <= requested_as_of_time`; future candles are excluded and counted for evidence.

Implemented outcomes:

- reuses the existing W1 live-market/persistence query seam;
- adds no external feed/provider/broker connection;
- assembles causal live inference inputs from persisted live candles only;
- excludes future candles from inference windows;
- computes deterministic causal features without identity fields;
- refuses `seed:synthetic` as authoritative live inference input;
- anchors `InferenceInput.as_of_time` to the freshest included candle so W3-U03 stale-data guardrails apply;
- scores deterministic live snapshots with identical score/hash for identical as-of inputs;
- persists governed live-path advisory signal records through W3-U01/W3-U02/W3-U03 services;
- adds no UI, alert, live signal WebSocket push, external feed, broker, execution, order, paper trading, or position path.

DA does not self-approve. This delivery is submitted for operator evidence collection and ITRGA independent review.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W3-U03 ITRGA approval | `docs/build-orders/ITRGA_REVIEW_W3-U03.md` |
| W3-U04 Build Order | `docs/build-orders/BUILD_ORDER_W3-U04.md` |
| W3-U04 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W3-U04.md` |
| Live adapter ADR | `docs/adr/ADR-034_Live_Market_Inference_Adapter.md` |
| Operator evidence commands | `docs/evidence/W3-U04_OPERATOR_EVIDENCE_COMMANDS.md` |

---

## 3. Implementation Summary

### 3.1 Live Market Inference Adapter

Added:

```text
backend/app/trading_intelligence/live_market/adapter.py
backend/app/trading_intelligence/live_market/errors.py
backend/app/trading_intelligence/live_market/__init__.py
```

Key objects:

- `LiveMarketInferenceAdapter`;
- `LiveMarketInferenceWindow`;
- `LiveMarketSignalResult`;
- `LiveMarketInferenceError`.

The adapter uses `CandleRepository` and persisted `candles` from the existing live-market seam. It does not open network connections.

### 3.2 As-of / No-Look-Ahead Input Assembly

The adapter queries causal windows with:

```text
open_time <= requested_as_of_time
source in ('live:simulated')
```

It records `excluded_future_candle_count` for evidence and sets the inference input `as_of_time` to the freshest included candle's timestamp.

### 3.3 Deterministic Features

The live adapter computes deterministic numeric features only:

```text
return_1
range_pct
```

It does not include learned identity fields such as `symbol`, `provider`, or `market_class` in `features`.

### 3.4 Stale Live Data Handling

Because the adapter anchors `InferenceInput.as_of_time` to the freshest included candle, stale data is naturally routed through W3-U03 `STALE_INPUT` guardrails.

### 3.5 Governed Signal Path

The adapter can persist a governed signal through:

```text
LiveMarketInferenceAdapter.produce_signal(...)
  → AdvisorySignalService.produce(...)
  → W3-U01 eligibility gate
  → W3-U02 signal persistence
  → W3-U03 guardrails/staleness
```

No operator push or signal route was added.

### 3.6 Repository Query Helpers

Extended `CandleRepository` with:

```text
list_window_as_of(...)
count_after(...)
```

These support causal as-of windows and no-look-ahead evidence counts.

---

## 4. Files Created

```text
backend/app/trading_intelligence/live_market/__init__.py
backend/app/trading_intelligence/live_market/adapter.py
backend/app/trading_intelligence/live_market/errors.py
backend/tests/test_live_market_inference_adapter.py
docs/adr/ADR-034_Live_Market_Inference_Adapter.md
docs/build-orders/ITRGA_REVIEW_W3-U03.md
docs/build-orders/BUILD_ORDER_W3-U04.md
docs/build-orders/BUILD_ORDER_INTAKE_W3-U04.md
docs/evidence/W3-U04_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W3-U04.md
```

---

## 5. Files Modified

```text
backend/app/__init__.py
backend/app/core/config.py
backend/app/main.py
backend/app/models/system.py
backend/app/repositories/candle_repository.py
backend/pyproject.toml
backend/README.md
backend/tests/test_system.py
frontend/src/layouts/TerminalLayout.tsx
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Acceptance Criteria Mapping

| Build Order Requirement | DA Result |
|---|---|
| Reuse existing W1 seam; no external broker/feed | Implemented via `CandleRepository` persisted live candle query; no network/provider imports |
| No look-ahead | Implemented and tested; future candles counted/excluded from window |
| Stale live data withheld `STALE_INPUT` | Implemented via W3-U03 guardrail path and tested |
| Deterministic live scoring | Implemented and tested; same snapshot → same score/hash |
| No `seed:synthetic` authoritative input | Implemented and tested; adapter refuses seed-only authoritative window |
| No symbol/provider identity as model input | Implemented and tested; features only `return_1`, `range_pct` |
| Governed live path | Implemented and tested; non-advisory model withheld by name |
| No UI/alert/push/execution | Preserved; no route/UI/push/broker/execution code added |
| Persisted live-path proof | Evidence pack includes committing script, raw `SELECT`, audit proof, and API read-back |

---

## 7. Local Validation Evidence Collected by DA

### Backend lint

```text
$ ruff check .
All checks passed!
```

### Backend tests

```text
$ pytest -q
183 passed, 1 warning in 30.68s
```

### Named W3-U04 tests

```text
$ pytest tests/test_live_market_inference_adapter.py -q
6 passed, 1 warning in 0.53s
```

### Alembic local migration smoke

W3-U04 adds no schema migration. Full migration chain remains green:

```text
20260715_0017 (head)
```

### Frontend validation

```text
npm audit --audit-level=high
found 0 vulnerabilities

npm test
Test Files 8 passed
Tests 16 passed

npm run lint
# TypeScript clean

npm run build
✓ built
```

### No-external-feed / no-execution grep

```text
grep -RInE "place_order|cancel_order|broker\.|MetaTrader|mt5|requests\.|httpx\.|socket\.|websocket-client|external_feed|ExternalFeed" backend/app/trading_intelligence/live_market
# no output
```

```text
grep -RInE "place_order|cancel_order|broker\.|execute|order_intent dispatch" backend/app/trading_intelligence/live_market backend/app/trading_intelligence/signals backend/app/api/routes/advisory_signals.py
# no output
```

```text
grep -RInE "live_signal|emit_signal|place_order|cancel_order" backend/app/api/routes frontend/src
# no output
```

---

## 8. Security Review

| Area | Review |
|---|---|
| Authentication | No new public endpoint or auth path added. Existing history API remains Bearer-authenticated. |
| Authorization | No operator-triggered live inference route was added. |
| Secrets | No new secrets or credentials introduced. |
| External egress | No external provider/feed/broker connection introduced. |
| PII | No PII introduced. |
| Execution | No broker/order/execution path added. |

---

## 9. Performance / Scalability Review

- Adapter queries bounded causal windows using existing indexed candle columns.
- Feature computation is O(window size), with default small windows.
- No background task, stream, scheduler, or polling surface was introduced.
- Existing live-market service behavior is unchanged.

---

## 10. Maintainability Review

- Adapter is isolated under `app/trading_intelligence/live_market`.
- It extends W1/W3 seams instead of rewriting live-market service or signal service.
- Repository helpers are generic and reusable.
- Tests cover no-look-ahead, stale data, deterministic scoring, seed refusal, governed non-advisory refusal, and no external/feed execution path.

---

## 11. Governance Compliance Review

| Rule | Compliance |
|---|---|
| Build Order scope | Implemented Components A–F only. |
| No future wave work | No W3-U05 UI, W3-U06 alerts, W3-U07 analytics, external feed, or Wave-6 execution implemented. |
| Database integrity | No schema change required; Alembic head remains W3-U03 `20260715_0017`. |
| ML governance | W3-U01 eligibility and W3-U02/W3-U03 signal persistence/guardrails are reused. |
| No-look-ahead | Implemented by as-of repository query and named tests. |
| Evidence | Operator command pack includes tests, no-look-ahead proof, stale proof, deterministic proof, persisted live-path proof, API read-back, grep, CI marker, and parity smoke. |
| ITRGA relationship | DA does not self-approve; report submitted for independent review. |

---

## 12. Known Risks

| Risk | Status |
|---|---|
| Operator advisory dashboard absent | Accepted; explicitly W3-U05 scope. |
| Alerts/live signal stream absent | Accepted; explicitly W3-U06 scope. |
| External market-data-provider integration absent | Accepted; future gated provider unit. |
| Background signal expiry worker absent | Carried from TD-056; API current filtering remains mitigation. |
| PostgreSQL operator evidence not yet run in DA sandbox | Requires operator-run target evidence per command pack. |

---

## 13. Technical Debt Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

- `TD-055` closed foundationally: live market inference adapter implemented.
- `TD-057` added: operator advisory dashboard absent, deferred to W3-U05.
- `TD-058` added: live alert/push stream absent, deferred to W3-U06.
- `TD-059` added: external market data provider integration absent, future gated work.

---

## 14. Operator Evidence Command Pack

The full operator evidence command pack is available at:

```text
docs/evidence/W3-U04_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. Alembic schema status to `20260715_0017 (head)`;
2. full backend/frontend tests;
3. named W3-U04 no-look-ahead/stale/deterministic tests;
4. W3-U01/W3-U02/W3-U03/live-market/broker regression tests;
5. persisted live-path signal proof using raw `SELECT`;
6. audit-event proof;
7. authenticated API read-back;
8. no-external-feed/no-execution grep evidence;
9. local CI completion marker capture;
10. parity smoke.

---

## 15. DA Non-Approval Statement

W3-U04 is implemented and locally validated by the Development Authority. It is **not accepted, approved, or complete by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W3-U04_OPERATOR_EVIDENCE_COMMANDS.md`;
2. ITRGA independent review;
3. ITRGA verdict.

DA will not begin W3-U05 or any subsequent unit without ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U04**
