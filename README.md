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

> **Note:** every step below assumes you start from the **repository root**
> (`kyn-ai-portal/`, the folder you land in right after `git clone` + `cd kyn-ai-portal`).
> Each numbered step `cd`s into a subfolder and back out again, so you always
> return to the repo root before starting the next step.

1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/hayriyeaydin777/kyn-ai-portal.git
   cd kyn-ai-portal
   ```
   You are now at the repo root. Stay here for step 2.

2. **Start the databases** (MySQL + Redis) — run from the repo root

   If you're on macOS using Colima instead of Docker Desktop, make sure the Colima VM is
   running first (`colima status`, then `colima start` if needed) — otherwise `docker`
   commands fail with `failed to connect to the docker API ... no such file or directory`.

   ```bash
   make up
   ```
   Still at the repo root after this — `make up` does not change directory.

3. **Set up the API (Python/FastAPI)** — starts at repo root, ends back at repo root

   > If VS Code shows a notification like *"An environment file is configured but
   > terminal environment injection is disabled"* after `cp .env.example .env`, that's
   > just an informational popup from the Python extension — it's safe to dismiss
   > and does not indicate a failed command.

   ```bash
   cd apps/api                        # repo root -> apps/api
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   cp .env.example .env               # defaults already point at the compose MySQL instance
   .venv/bin/alembic upgrade head     # creates all database tables
   .venv/bin/python -m scripts.seed   # optional: adds 3 synthetic demo applications
   cd ../..                           # apps/api -> repo root
   ```

4. **Set up the web app (SvelteKit)** — starts at repo root, ends back at repo root
   ```bash
   cd apps/web                        # repo root -> apps/web
   npm install
   cd ../..                           # apps/web -> repo root
   ```

5. **Set up the policy service (.NET)** — run from the repo root; no extra setup needed
   beyond the SDK. `dotnet run` (used in the next section) restores packages automatically
   on first run, from inside `services/policy-service`.

## Running the app

You need **3 separate terminal windows/tabs**, each one starting at the **repo root**
(`kyn-ai-portal/`). Run one command per terminal — leave all three running at the same time:

| Terminal | Command | URL |
|---|---|---|
| 1 | `make api` | FastAPI on http://localhost:8000 |
| 2 | `make policy` | ASP.NET Core policy service — check its console output for the exact port (commonly http://localhost:5142) |
| 3 | `make web` | SvelteKit dev server on http://localhost:5173 |

None of the `make` commands require you to `cd` anywhere first — always run them from the
repo root, and the Makefile `cd`s into the right subfolder internally.

Once all three are running, open **http://localhost:5173** in a browser. Use `make down`
(from the repo root, in any terminal) to stop MySQL/Redis when done — you can leave the
`make api` / `make policy` / `make web` terminals running or stop them with `Ctrl+C`.

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
