# UI Integration Plan

Source of truth for building out the pages implied by `docs/Designs/` mockups,
one page/group at a time, with minimal backend work and minimal token spend per
task. Each row below is one approval-sized unit of work (one TODO ID).

## Ground rules (read before starting any task)

- **Reuse existing API routers first.** Only add a new backend endpoint/model
  when there is truly no existing data to show.
- **No backend yet? Stub it.** Render the page with static/hardcoded sample data
  and a visible `(sample data)` note, rather than building a new model + router
  + migration for a page that's cosmetic-only right now. Backend can be added
  later as its own separate task.
- **One page per task.** Don't build a whole nav group in one pass — implement,
  validate (`npm run check` + a quick visual check), stop, get approval, move on.
- **Reuse the shell.** Every new page uses the existing `+layout.svelte` /
  `Sidebar.svelte` shell — no new layout patterns.
- **Keep existing routes working.** `/applications`, `/applications/[id]`,
  `/governance`, `/workspace` must keep working after the sidebar restructure.

## Status legend

`⬜ not started` · `🟨 in progress` · `✅ done` · `⏸️ deferred (needs new backend)`

## Phase 1 — Sidebar restructure

| ID | Task | Backend needed? | Status |
|---|---|---|---|
| UI-P1-1 | Restructure `Sidebar.svelte` into 6 grouped sections (Recovery Readiness, AI Workspace, Architecture, Agent Platform, Evaluation, Operations) per mockups, linking to routes below (create as they land) | ⬜ No | ✅ done |
| UI-P1-2 | Add top-bar search input (non-functional placeholder for now) + icon stubs (notifications/help/settings/user) | ⬜ No | ✅ done |

## Phase 2 — Recovery Readiness

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P2-1 | Applications list | `/applications` (exists) | `applications` router (exists) | ✅ done |
| UI-P2-2 | Application detail | `/applications/[id]` (exists) | existing routers | ✅ done |
| UI-P2-3 | Dependencies | `/applications/[id]/dependencies` | `dependencies` router (exists) | ✅ done |
| UI-P2-4 | Evidence | `/applications/[id]/evidence` | `evidence` router (exists) | ⬜ |
| UI-P2-5 | Findings | `/applications/[id]/findings` | `assessments` router (exists — findings are its output) | ⬜ |
| UI-P2-6 | Runbooks | `/applications/[id]/runbooks` | none exists — **stub with static sample runbook cards** | ⏸️ stub only |

## Phase 3 — AI Workspace

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P3-1 | Brief Generator | `/workspace/brief-generator` | `briefs` router (exists) | ⬜ |
| UI-P3-2 | Modernization Advisor | `/applications/[id]/modernization` (exists) | `modernization_cases`/`modernization_recommendations` (exists) | ✅ done |
| UI-P3-3 | Code Review | `/workspace/code-review` | `code_reviews` router (exists) | ⬜ |
| UI-P3-4 | Test Generator | `/workspace/test-generator` | `test_generations` router (exists) | ⬜ |
| UI-P3-5 | Documentation | `/workspace/documentation` | `documentation_drafts` router (exists) | ⬜ |
| UI-P3-6 | Prompt Lab | `/workspace/prompt-lab` | none exists — **stub, client-side only, no persistence** | ⏸️ stub only |

## Phase 4 — Architecture

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P4-1 | ADR Assistant | `/architecture/adr-assistant` | `architecture_decisions` router (exists) | ⬜ |
| UI-P4-2 | Architecture Review | `/architecture/review` | `architecture_reviews` router (exists) | ⬜ |
| UI-P4-3 | Diagrams | `/architecture/diagrams` | `diagrams` router (exists) | ⬜ |
| UI-P4-4 | Governance (existing page) | `/governance` (exists) | existing routers | ✅ done — keep as-is or fold into UI-P4-1/2 |

## Phase 5 — Agent Platform

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P5-1 | Agent Catalog (list) | `/agents` | `agents` router (exists) | ⬜ |
| UI-P5-2 | Agent Details | `/agents/[id]` | `agents`/`agent_versions` routers (exist) | ⬜ |

## Phase 6 — Evaluation & Operations (mostly stubs)

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P6-1 | AI Metrics | `/evaluation/metrics` | none exists — **stub with static sample metrics** | ⏸️ stub only |
| UI-P6-2 | Observability | `/evaluation/observability` | none exists — **stub** | ⏸️ stub only |
| UI-P6-3 | Approvals | `/operations/approvals` | `approvals` router (exists) | ⬜ |
| UI-P6-4 | Audit Log | `/operations/audit-log` | `AuditEvent` model exists, **no GET router yet** — smallest real backend add in this plan (one read-only endpoint) | ⏸️ needs 1 new endpoint |
| UI-P6-5 | Policies | `/operations/policies` | policy-service is a separate .NET service, not proxied to web — **stub for now** | ⏸️ stub only |
| UI-P6-6 | Settings | `/operations/settings` | none exists — **stub, static form, no save** | ⏸️ stub only |

## Working agreement for this plan

1. Pick the next `⬜` task top-to-bottom within a phase.
2. If it says "stub only" — build UI with inline sample data, label it clearly,
   do not touch the API.
3. If it reuses an existing router — wire real data via `$lib/api.ts`, same
   pattern as `applications`/`governance` pages today.
4. Update this file's status column after each task lands.
