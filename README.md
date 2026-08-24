# kyn-ai-portal

Resilience Operations & AI Engineering Portal — a synthetic portfolio application.
Planning materials (architecture docs, ADRs, prompts, mockups) are kept locally under
`materials/` and are intentionally not tracked in this repository.

See `SECURITY.md` and `DATA_POLICY.md` for constraints that apply to all code in this repo.

## Prerequisites

- [Node.js](https://nodejs.org/) 22+
- [Python](https://www.python.org/) 3.10+
- [.NET SDK](https://dotnet.microsoft.com/download) 10+
- [Docker](https://www.docker.com/) (or [Colima](https://github.com/abiosoft/colima) on macOS) with Docker Compose

## First-time setup

1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/hayriyeaydin777/kyn-ai-portal.git
   cd kyn-ai-portal
   ```

2. **Start the databases** (MySQL + Redis)

   If you're on macOS using Colima instead of Docker Desktop, make sure the Colima VM is
   running first (`colima status`, then `colima start` if needed) — otherwise `docker`
   commands fail with `failed to connect to the docker API ... no such file or directory`.

   ```bash
   make up
   ```

3. **Set up the API (Python/FastAPI)**
   ```bash
   cd apps/api
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   cp .env.example .env   # defaults already point at the compose MySQL instance
   .venv/bin/alembic upgrade head   # creates all database tables
   .venv/bin/python -m scripts.seed  # optional: adds 3 synthetic demo applications
   cd ../..
   ```

4. **Set up the web app (SvelteKit)**
   ```bash
   cd apps/web
   npm install
   cd ../..
   ```

5. **Set up the policy service (.NET)** — no extra setup needed beyond the SDK; `dotnet run` restores packages automatically on first run.

## Running the app

Each service runs in its own terminal (all from the repo root):

```bash
make api      # FastAPI on http://localhost:8000
make policy   # ASP.NET Core policy service on http://localhost:5142 (or as shown in its console output)
make web      # SvelteKit dev server on http://localhost:5173
```

Then open **http://localhost:5173** in a browser. Use `make down` to stop MySQL/Redis when done.

By default `AI_PROVIDER=fake` in `apps/api/.env` — the app runs fully functional deterministic demos (assessments, briefs, modernization advisor, code review, etc.) with **zero AI/LLM token cost**. Set `AI_PROVIDER=claude` and provide real credentials only if you intend to wire up the real Claude provider adapter.

## Running tests

```bash
cd apps/api && .venv/bin/pytest        # backend (uses an in-memory SQLite DB, no infra needed)
cd apps/web && npm run test:unit       # frontend unit tests (Vitest)
cd apps/web && npm run test:e2e        # end-to-end smoke test (Playwright)
cd services/PolicyService.Tests && dotnet test   # .NET policy rule tests
```

## Local development (quick reference)

- `make up` — start MySQL + Redis (Docker Compose)
- `make web` — run the SvelteKit dev server (apps/web)
- `make api` — run the FastAPI dev server (apps/api, requires `apps/api/.venv`)
- `make policy` — run the ASP.NET Core policy service (services/policy-service)
- `make down` — stop MySQL + Redis
