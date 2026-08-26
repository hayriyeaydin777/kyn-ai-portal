#!/usr/bin/env bash
# Starts colima (if needed), infra (mysql/redis), and all three app processes together.
# Ctrl-C stops everything cleanly.
set -euo pipefail
cd "$(dirname "$0")/.."

if command -v colima >/dev/null 2>&1 && ! colima status >/dev/null 2>&1; then
	echo "Starting colima..."
	colima start
fi

echo "Starting infra (mysql/redis)..."
docker compose -f infra/compose/docker-compose.yml up -d

pids=()
cleanup() {
	echo
	echo "Stopping app processes..."
	for pid in "${pids[@]}"; do
		kill "$pid" 2>/dev/null || true
	done
	wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

(cd apps/api && .venv/bin/uvicorn app.main:app --reload --port 8000) &
pids+=($!)

(cd apps/web && npm run dev) &
pids+=($!)

(cd services/policy-service && dotnet run) &
pids+=($!)

echo "All processes started. API :8000, Web :5173, Policy service running. Press Ctrl-C to stop."
wait
