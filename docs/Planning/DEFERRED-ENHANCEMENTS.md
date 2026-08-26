# Deferred Enhancements

Tracked improvements suggested during build-out but intentionally skipped/deferred
to save Copilot tokens and avoid scope creep. Revisit before the demo if token
budget allows.

## UI does not pixel-match the `materials/` mockups (partially addressed)
A small, cheap styling pass has been done: shared layout (`+layout.svelte`) with a
persistent top nav, plus `app.css` (design tokens, typography, form/button/card/list
styling). This makes the app look coherent and presentable, but it is **not** a
pixel-accurate implementation of the `materials/design/ui-mockups/*.png` mockups —
those remain directional references only. Still not done: per-page visual polish
(data tables instead of plain lists, dashboard-style layout, badges/status colors
matching the mockups, responsive/mobile layout). Revisit if more time/budget allows
before a live demo.

## From Stage 4 (AI Briefing)
- **S4-10 — Real Claude provider adapter**: `LLMProvider` interface and
  `AI_PROVIDER` env switch are already wired (`app/providers/factory.py`).
  Implementing `app/providers/claude.py` is a self-contained follow-up task.
  Only do this right before a live demo, with a real Anthropic API key, since
  it's the only place in the app that spends real tokens.

## From Stage 6 (AI Engineering Workspace)
- **Real static-analysis tool integration** (ruff, bandit, mypy, eslint, etc.):
  skipped in favor of our own deterministic Python checks. Would add subprocess
  management, tool installation, and per-language config — meaningful effort
  for a demo app. Revisit if a hiring reviewer specifically wants to see real
  tool integration.
- **Multi-language code review/test/doc generation** (JS/TS/C#): skipped,
  Python-only for now. Each language needs its own parser/checks.
- **Suggested-patch auto-diff generation**: skipped. Findings + narrative
  describe fixes in text; no diff/patch computation or safe-apply/rollback
  machinery was built. Would be a good "Code Review" module deepening later.
- **Sandboxed execution of submitted code**: intentionally NOT deferred —
  this is a permanent security boundary, not a token-saving shortcut. All
  code review / test generation works via `ast` parsing only, never `exec`.

## From Stage 7 (Architecture Governance)
- **Real diagram file upload/rendering** (Mermaid/PlantUML storage, images):
  skipped. `diagram_metadata` only stores title/description/scope/version/
  linked decision ids — matches "diagrams never become source of truth."
- **Role-based author/reviewer/approver enforcement**: skipped — no real auth
  system exists yet (Stage 10 Hardening). The API enforces the *state machine*
  (draft→proposed→accepted/rejected, immutable once accepted) but not *who*
  is allowed to call which endpoint.

## From Stage 8 (Agent Platform) — token-budget-conscious pass (75% used)
- **Agent Catalog UI** (`/agents` SvelteKit page): skipped for now. Backend
  (`/v1/agents`, `/v1/agents/{id}/versions`, lifecycle transitions, tool
  allowlist validation) is complete and tested; only the UI page is deferred.
  Revisit before the demo if a visual catalog view is wanted.
- **Seed script for the 7 initial agents** (Modernization, Architecture, Code
  Review, Testing, Evidence, Dependency, Briefing): skipped. Backend supports
  creating these via the API directly; a seed script is a nice-to-have for
  demo polish, not required to prove the architecture.
- **A real shared agent orchestration runtime** that dynamically dispatches
  tools by name at request time: skipped. ADR-011 says agents are
  "configurations over a shared runtime," but building a generic dispatch
  engine is substantial effort with little added value beyond what the
  catalog/metadata (governance, versioning, tool allowlisting, lifecycle)
  already demonstrates. Each capability stays invoked via its existing direct
  endpoint (Stage 3/5/6 routers).
- **Evaluation-threshold-gated promotion** (tied to Stage 9, not built yet):
  skipped. The "approved" lifecycle transition is currently human-only via
  `/advance`, without requiring evaluation scores. Revisit once Stage 9 exists.


## General / cross-cutting (not yet scoped into any stage)
- **CI coverage for `dotnet test` running on GitHub-hosted runners** — done
  (Stage 3), but consider adding coverage reporting (dotnet-coverage /
  coverlet) if useful for the portfolio evidence matrix later.
- **GitHub secret scanning** — not available on a free private repo; currently
  substituted with a local gitleaks pre-commit hook. If the repo is ever made
  public (e.g., for the actual job-search demo), enable native GitHub secret
  scanning too.
- **SvelteKit/Svelte version currency** — pinned to Svelte 4 / SvelteKit 2.5
  for stability (see Stage 2 fix commit). A deliberate Svelte 5 migration is
  a separate, larger task, not something to do incidentally.
