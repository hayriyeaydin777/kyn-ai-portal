# Local Setup

## Prerequisites

Install Git, Node.js LTS, Python 3.12+, uv, .NET 10 SDK, Docker Desktop, and VS Code.

Verify:

```bash
git --version
node --version
npm --version
python3 --version
uv --version
dotnet --version
docker --version
docker compose version
```

## Repository setup

```bash
git init
git add .
git commit -m "docs: add portfolio architecture and safety baseline"
```

Create the personal GitHub repository, confirm `git remote -v` points only to the personal account, and push the baseline.

## Claude setup

Configure Claude to read `CLAUDE.md`, then send `prompts/00-FIRST-SESSION-PROMPT.md`. Approve one TODO at a time.

## Runtime scaffolding

Scaffold each runtime only after its TODO is approved:

```bash
npx sv create apps/web
```

```bash
cd apps/api
uv init --package
uv add "fastapi[standard]" pydantic-settings sqlmodel sqlalchemy alembic
uv add --dev pytest pytest-asyncio httpx ruff mypy
```

```bash
cd services/policy-service
dotnet new webapi -n Resilience.PolicyService --framework net10.0 --use-minimal-apis
```

Keep `AI_PROVIDER=fake` until the deterministic orchestration tests are complete.
