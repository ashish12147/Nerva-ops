#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f config/settings.yaml ]; then
  cp config/settings.example.yaml config/settings.yaml
fi

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Nerva Ops installed. Edit .env and config/settings.yaml, then run:"
echo "source .venv/bin/activate && uvicorn agent.main:app --host 0.0.0.0 --port 8080"
