.PHONY: up down web api policy dev

up:
	docker compose -f infra/compose/docker-compose.yml up -d

down:
	docker compose -f infra/compose/docker-compose.yml down

web:
	cd apps/web && npm run dev

api:
	cd apps/api && .venv/bin/uvicorn app.main:app --reload --port 8000

policy:
	cd services/policy-service && dotnet run

dev: up
	@echo "Infra started. Run 'make web', 'make api', 'make policy' in separate terminals."
