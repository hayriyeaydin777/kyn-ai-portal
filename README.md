# 🛡️ kyn-ai-portal

**Resilience Operations & AI Engineering Portal** — a synthetic portfolio application.

Planning materials (architecture docs, ADRs, prompts, mockups) are tracked under
[`docs/`](docs/): [`docs/Planning/`](docs/Planning/) for architecture/ADR docs,
[`docs/Prompts/`](docs/Prompts/) for the build prompts, and [`docs/Designs/`](docs/Designs/)
for UI mockups.

📄 See [`SECURITY.md`](SECURITY.md) and [`DATA_POLICY.md`](DATA_POLICY.md) for constraints
that apply to all code in this repo.

---

## 📚 Contents

- [🚀 Quick start](#-quick-start)
- [✅ Prerequisites](#-prerequisites)
- [🧰 First-time setup](#-first-time-setup)
- [▶️ Running the app](#️-running-the-app)
- [🎨 UI status](#-ui-status)
- [🧪 Running tests](#-running-tests)
- [📎 Command reference](#-command-reference)

---

## 🚀 Quick start

> Already done the one-time setup below? Just run this from the repo root:
>
> ```bash
> make dev-all
> ```
>
> This starts **everything** — Colima (if needed), MySQL/Redis, the API, the web app, and
> the policy service — in one terminal. Open **http://localhost:5173** once you see
> `All processes started`. Press `Ctrl+C` once to stop it all.

First time here? Continue reading below. 👇

---

## ✅ Prerequisites

| Tool | Version | Notes |
|---|---|---|
| 🟢 [Node.js](https://nodejs.org/) | 22+ | for the SvelteKit web app |
| 🐍 [Python](https://www.python.org/) | 3.10+ | for the FastAPI backend |
| 🔷 [.NET SDK](https://dotnet.microsoft.com/download) | 10+ | for the policy service |
| 🐳 [Docker](https://www.docker.com/) | any | or [Colima](https://github.com/abiosoft/colima) on macOS, with Docker Compose |

---

## 🧰 First-time setup

> 💡 Every step below assumes you start from the **repository root**
> (`kyn-ai-portal/` — the folder you land in right after `git clone` + `cd kyn-ai-portal`).
> Each step `cd`s into a subfolder and back out again, so you always return to the repo
> root before the next step.

### 1️⃣ Clone and enter the repo

```bash
git clone https://github.com/hayriyeaydin777/kyn-ai-portal.git
cd kyn-ai-portal
```

### 2️⃣ Start the databases (MySQL + Redis)

> 🍎 On macOS with Colima instead of Docker Desktop: run `colima status`, then
> `colima start` if it's not running — otherwise `docker` commands fail with
> `failed to connect to the docker API ... no such file or directory`.

```bash
make up
```

### 3️⃣ Set up the API (Python / FastAPI)

> ℹ️ If VS Code shows *"An environment file is configured but terminal environment
> injection is disabled"* after `cp .env.example .env`, that's just an informational
> popup from the Python extension — safe to dismiss.

```bash
cd apps/api
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env               # defaults already point at the compose MySQL instance
.venv/bin/alembic upgrade head     # creates all database tables
.venv/bin/python -m scripts.seed   # optional: adds 3 synthetic demo applications
cd ../..
```

### 4️⃣ Set up the web app (SvelteKit)

```bash
cd apps/web
npm install
cd ../..
```

### 5️⃣ Set up the policy service (.NET)

```bash
cd services/policy-service
dotnet restore                      # downloads NuGet packages (one-time)
cd ../..
```

> ⚠️ `dotnet run` only works when run **from inside `services/policy-service`**. The
> `make policy` command already `cd`s there for you, so you never need to run
> `dotnet run` manually.

✅ Setup complete — jump to **Running the app** below.

---

## ▶️ Running the app

### 🅰️ Option A — one command (recommended)

```bash
make dev-all
```

Starts Colima (if installed and not already running), MySQL/Redis, the FastAPI backend
(`:8000`), the SvelteKit web app (`:5173`), and the .NET policy service (`:5142`) — all
together, in one terminal. Press `Ctrl+C` once to stop everything cleanly.

Open **http://localhost:5173** once you see `All processes started`.

<details>
<summary>🅱️ Option B — separate terminals (manual control over each process)</summary>

> ⚠️ **Run every `make` command from the repository root** (`kyn-ai-portal/`) — the same
> folder that contains this `README.md` and the `Makefile`. If you `cd`ed into a subfolder
> for setup, run `cd ~/path/to/kyn-ai-portal` first. Running `make api` / `make policy` /
> `make web` from inside a subfolder fails with `make: *** No rule to make target ...`.
>
> Check where you are at any time with `pwd` — it should end in `.../kyn-ai-portal`.

You need **3 separate terminal windows/tabs**, each starting at the repo root. Run one
command per terminal — leave all three running at the same time:

| Terminal | Command | URL |
|---|---|---|
| 1 | `make api` | FastAPI on http://localhost:8000 |
| 2 | `make policy` | ASP.NET Core policy service — check console output for the exact port (commonly http://localhost:5142) |
| 3 | `make web` | SvelteKit dev server on http://localhost:5173 |

Open **http://localhost:5173** once all three are running. Use `make down` (from the repo
root, in any terminal) to stop MySQL/Redis when done.

</details>

> 💰 By default `AI_PROVIDER=fake` in `apps/api/.env` — the app runs fully functional
> deterministic demos (assessments, briefs, modernization advisor, code review, etc.)
> with **zero AI/LLM token cost**. Set `AI_PROVIDER=claude` and provide real credentials
> only if you intend to wire up the real Claude provider adapter.

---

## 🎨 UI status

The app has a Tailwind-styled shell with a responsive sidebar
([`Sidebar.svelte`](apps/web/src/lib/Sidebar.svelte)) and shared design tokens — a first
pass at matching the [`docs/Designs/`](docs/Designs/) mockups. Per-page visual
polish (data tables, dashboard layouts, status badges) is still incomplete — see
[`docs/Planning/DEFERRED-ENHANCEMENTS.md`](docs/Planning/DEFERRED-ENHANCEMENTS.md) for what's
tracked as not-yet-done.

---

## 🧪 Running tests

```bash
cd apps/api && .venv/bin/pytest        # backend (in-memory SQLite, no infra needed)
cd apps/web && npm run test:unit       # frontend unit tests (Vitest)
cd apps/web && npm run test:e2e        # end-to-end smoke test (Playwright)
cd services/PolicyService.Tests && dotnet test   # .NET policy rule tests
```

---

## 📎 Command reference

| Command | Description |
|---|---|
| `make dev-all` | 🚀 Start everything together (Colima, MySQL/Redis, API, web, policy service) |
| `make up` | Start MySQL + Redis (Docker Compose) |
| `make down` | Stop MySQL + Redis |
| `make api` | Run the FastAPI dev server (`apps/api`, requires `apps/api/.venv`) |
| `make web` | Run the SvelteKit dev server (`apps/web`) |
| `make policy` | Run the ASP.NET Core policy service (`services/policy-service`) |
