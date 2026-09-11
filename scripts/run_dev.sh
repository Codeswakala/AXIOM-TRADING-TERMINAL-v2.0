#!/usr/bin/env bash
# Single-process AXIOM dev runner: build frontend (if needed) + uvicorn
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Ensuring backend venv + deps"
cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created backend/.env from example"
fi

echo "==> Building frontend for static mount"
cd "$ROOT/frontend"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm run build

echo "==> Applying migrations"
cd "$ROOT/backend"
alembic upgrade head

echo "==> Starting uvicorn on http://0.0.0.0:8000"
echo "    Login with the explicit bootstrap/operator credentials configured in backend/.env"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
