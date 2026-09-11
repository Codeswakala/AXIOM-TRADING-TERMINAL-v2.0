#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Backend tests"
cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
pytest -q

echo "==> Frontend tests"
cd "$ROOT/frontend"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm test

echo "==> All tests completed"
