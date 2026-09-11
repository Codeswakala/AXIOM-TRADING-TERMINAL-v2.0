#!/usr/bin/env bash
# W1-U02 local CI equivalent. Requires a running PostgreSQL matching AXIOM_DATABASE_URL.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

: "${AXIOM_DATABASE_URL:=postgresql+asyncpg://axiom:axiom_dev_password@localhost:5432/axiom}"
: "${AXIOM_JWT_SECRET_KEY:=local-ci-secret-key-at-least-32-chars}"
export AXIOM_DATABASE_URL
export AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false
export AXIOM_ENVIRONMENT=testing
export AXIOM_JWT_SECRET_KEY
export AXIOM_ALLOW_INSECURE_DEV=true
export AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
export AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
export AXIOM_BOOTSTRAP_ADMIN_PASSWORD=admin123
export AXIOM_LIVE_MARKET_AUTO_START=false

cd "$ROOT/backend"
echo "==> Backend dependencies"
python -m pip install -r requirements.txt

echo "==> Alembic upgrade head against PostgreSQL"
alembic upgrade head

echo "==> Ruff"
ruff check .

echo "==> Pytest"
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
pytest

cd "$ROOT/frontend"
echo "==> Frontend dependencies"
npm ci

echo "==> npm audit (high/critical gate)"
npm audit --audit-level=high

echo "==> Vitest"
npm test

echo "==> TypeScript"
npx tsc -b --pretty false

echo "==> Frontend build"
npm run build

echo "==> Local CI equivalent complete"
