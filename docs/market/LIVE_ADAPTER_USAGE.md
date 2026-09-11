# Live Market Adapter — Usage

## Overview

Foundation live feed uses a **simulated** adapter. No external broker is required. All live-control REST endpoints are operator-authenticated.

## Config (`.env`)

```env
AXIOM_LIVE_MARKET_ENABLED=true
AXIOM_LIVE_MARKET_AUTO_START=false
AXIOM_LIVE_MARKET_CLASS=forex
AXIOM_LIVE_MARKET_SYMBOL=EURUSD
AXIOM_LIVE_MARKET_SYMBOLS=EURUSD,BTCUSD
AXIOM_LIVE_MARKET_TIMEFRAME=M1
AXIOM_LIVE_MARKET_INTERVAL_SECONDS=2.0
```

## Auth

Login with explicitly configured operator/bootstrap credentials:

```bash
TOKEN=$(curl -s -X POST localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<configured-password>"}' | jq -r .tokens.access_token)
```

## Control

```bash
# Start simulated feed
curl -s -X POST localhost:8000/api/v1/market/live/start \
  -H "Authorization: Bearer $TOKEN" | jq

# Status / stats
curl -s localhost:8000/api/v1/market/live/status -H "Authorization: Bearer $TOKEN" | jq
curl -s localhost:8000/api/v1/market/live/stats -H "Authorization: Bearer $TOKEN" | jq

# Query persisted live candles
curl -s 'localhost:8000/api/v1/persistence/candles?symbol=EURUSD&timeframe=M1&limit=5' \
  -H "Authorization: Bearer $TOKEN" | jq

# Stop
curl -s -X POST localhost:8000/api/v1/market/live/stop \
  -H "Authorization: Bearer $TOKEN" | jq
```

## WebSocket

Issue a short-lived one-time ticket:

```bash
TICKET=$(curl -s -X POST localhost:8000/api/v1/auth/ws-ticket \
  -H "Authorization: Bearer $TOKEN" | jq -r .ticket)
```

Connect:

```text
ws://localhost:8000/ws/market?ticket=$TICKET
```

Messages:

- `subscribed` on connect
- `live_candle` on each bar
- `pong` response to client `ping`

## Readiness

`GET /ready` includes `live_market` check (`up` when running, `degraded` when stopped).

## Single uvicorn

```bash
./scripts/run_dev.sh
# http://localhost:8000
```

---

**End of live adapter usage**
