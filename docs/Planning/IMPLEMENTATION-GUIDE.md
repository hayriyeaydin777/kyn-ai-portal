# Step-by-Step Implementation Guide
## Stage 0 - Safety and repository
Create personal repo; verify remote; commit docs/safety baseline; enable secret scanning; keep private until review.
## Stage 1 - Foundation
Scaffold SvelteKit, FastAPI, .NET policy service, MySQL, Redis; add CI, health/readiness, correlation/logging; validate each runtime independently.
## Stage 2 - Recovery vertical slice
ApplicationProfile -> persistence -> API -> SvelteKit -> audit -> tests.
## Stage 3 - Deterministic assessment
Policy contracts -> .NET rules -> findings -> evidence traceability -> UI -> contract tests.
## Stage 4 - Grounded briefing
Provider interface -> fake provider -> tools -> evidence bundle -> structured brief -> citation validation -> approval -> evaluation.
## Stage 5 - Modernization Advisor
Current-state schema -> deterministic risk model -> option catalog -> generated roadmap -> review/approval -> export.
## Stage 6 - Engineering Workspace
Code-review read-only flow -> static tools -> findings/diff -> test drafts -> documentation drafts -> approvals.
## Stage 7 - Governance
ADR workflow -> architecture review checklist -> standards -> immutable versions -> diagram metadata.
## Stage 8 - Agent Platform
Catalog metadata -> versions -> tool allowlists -> schemas -> security tiers -> lifecycle -> promotion approval.
## Stage 9 - Evaluation
Datasets -> runners -> prompt versions -> metrics -> failure taxonomy -> dashboards -> promotion gates.
## Stage 10 - Hardening
OIDC seam, RBAC, CSRF/CORS, limits, idempotency, workers, fault tests, accessibility, telemetry, scans.
## Stage 11 - Demonstration
Synthetic seed, scripted demo, printable PDF, test evidence, threat model, public-repo review.

For every stage: plan; approve one TODO; implement; test; review; fix; validate milestone; document evidence.
