# kyn-ai-portal

Resilience Operations & AI Engineering Portal — a synthetic portfolio application.
Planning materials (architecture docs, ADRs, prompts, mockups) are kept locally under
`materials/` and are intentionally not tracked in this repository.

See `SECURITY.md` and `DATA_POLICY.md` for constraints that apply to all code in this repo.

## Local development

- `make up` — start MySQL + Redis (Docker Compose)
- `make web` — run the SvelteKit dev server (apps/web)
- `make api` — run the FastAPI dev server (apps/api, requires `apps/api/.venv`)
- `make policy` — run the ASP.NET Core policy service (services/policy-service)
- `make down` — stop MySQL + Redis
