# AXIOM Frontend

React + TypeScript + Vite operator terminal for the AXIOM platform.

## Quick start

```bash
cd frontend
npm install
npm run dev
```

Ensure the backend is running on port 8000. Vite proxies `/health`, `/ready`, `/system`, `/api`, and `/ws`.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Development server (port 5173) |
| `npm run build` | Typecheck + production build |
| `npm test` | Vitest unit tests |
| `npm run lint` | Typecheck (`tsc -b --pretty false`) |

## Current scope

- Authenticated operator terminal shell
- Operations dashboard
- Live Market dashboard with ticket-based WebSocket connection
- Chart Workspace at `/charts` (alias `/chart`) using TradingView Lightweight Charts
- Presentation-only charting; no indicators, AI overlays, or execution controls

Operational data APIs require an authenticated operator session. WebSockets use short-lived tickets issued by the backend.
