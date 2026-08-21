# Deferred Enhancements

Tracked improvements suggested during build-out but intentionally skipped/deferred
to save Copilot tokens and avoid scope creep. Revisit before the demo if token
budget allows.

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
