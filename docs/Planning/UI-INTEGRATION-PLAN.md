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
| UI-P1-3 | Adopt shadcn-svelte (bits-ui@0.21 + tailwind-variants, Svelte-4 compatible) + lucide-svelte icon set across `Sidebar.svelte`/header; add `Footer.svelte`; wire top-bar search for real against `listApplications` (Cmd/Ctrl+K, dropdown of matches); notifications/help/profile stay visual-only dropdowns; add sidebar collapse toggle | ⬜ No | ✅ done |

## Phase 2 — Recovery Readiness

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P2-1 | Applications list | `/applications` (exists) | `applications` router (exists) | ✅ done |
| UI-P2-2 | Application detail | `/applications/[id]` (exists) | existing routers | ✅ done |
| UI-P2-3 | Dependencies | `/applications/[id]/dependencies` | `dependencies` router (exists) | ✅ done |
| UI-P2-4 | Evidence | `/applications/[id]/evidence` | `evidence` router (exists) | ✅ done |
| UI-P2-5 | Findings | `/applications/[id]/findings` | `assessments` router (exists — findings are its output) | ✅ done |
| UI-P2-6 | Runbooks | `/applications/[id]/runbooks` | none exists — **stub with static sample runbook cards** | ⏸️ stub only |

## Phase 3 — AI Workspace

| ID | Page | Route | Backend | Status |
|---|---|---|---|---|
| UI-P3-1 | Brief Generator | `/workspace/brief-generator` | `briefs` router (exists) | ✅ done |
| UI-P3-2 | Modernization Advisor | `/applications/[id]/modernization` (exists) | `modernization_cases`/`modernization_recommendations` (exists) | ✅ done |
| UI-P3-3 | Code Review | `/workspace/code-review` | `code_reviews` router (exists) | ✅ done |
| UI-P3-4 | Test Generator | `/workspace/test-generator` | `test_generations` router (exists) | ✅ done |
| UI-P3-5 | Documentation | `/workspace/documentation` | `documentation_drafts` router (exists) | ✅ done |
| UI-P3-6 | Prompt Lab | `/workspace/prompt-lab` | none exists — **stub, client-side only, no persistence** | ⏸️ stub only |
| UI-P3-7 | Workspace Home dashboard (replaces old placeholder `/workspace` demo form) | `/workspace` | none — **stub, static sample Recent Runs/Approval Queue/Provider Status/Quick Stats/System Notice**, real links to the 5 built tools above | ✅ done |

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

## Phase 7 — Workspace Home visual polish

Pixel-level pass on `/workspace` (typography, color, icons, buttons) plus two
new floating UI affordances now that the shell has a sticky header/footer.
No backend involved — visual/UX only.

| ID | Task | Backend needed? | Status |
|---|---|---|---|
| UI-P7-1 | Typography: add a proper webfont (Inter, self-hosted via `@fontsource` — no external CDN calls) replacing the `Avenir Next` stack; define a small consistent type scale (page title / card title / body / label) in `tailwind.config.cjs` and apply it across Sidebar, AppHeader, Footer, and the Workspace Home page | ⬜ No | ✅ done |
| UI-P7-2 | Color system: extend `tailwind.config.cjs` with named accent tokens per tool (rocket/code/checklist/doc/scale/chat) and neutral surface tokens, replacing ad-hoc `bg-*-100 text-*-600` combinations sprinkled through the dashboard | ⬜ No | ⏸️ deferred — gradient tiles/pills use inline Tailwind combos for now, works visually |
| UI-P7-3 | Tool cards: redesign the 6 icon tiles as larger rounded-2xl gradient/solid tiles with soft shadow, and restyle "Launch" as a tinted pill button per tool's accent color (rounded-full, hover state), matching the reference screenshot | ⬜ No | ✅ done |
| UI-P7-4 | Restyle shared `ui/card`, `ui/table`, `ui/badge` primitives (spacing, border, header weight/tracking) for consistent polish across Recent AI Runs, Approval Queue, Provider Status, Quick Stats, and System Notice | ⬜ No | ⏸️ deferred — not started |
| UI-P7-5 | Add a floating scroll-to-top/bottom button, bottom-right of `<main>`'s scroll area — only visible once content is scrollable, direction flips based on scroll position, smooth-scrolls on click | ⬜ No | ✅ done (`ScrollFab.svelte`) |
| UI-P7-6 | Add a floating "AI assistant" launcher bubble, bottom-right (stacked with the scroll button) — subtle idle animation, opens a stub popover with a static sample greeting (visual only, no real chat wiring yet, labelled as such) | ⬜ No | ✅ done (`AssistantBubble.svelte`, built with Melt UI v2's `Popover` builder) |
| UI-P7-7 | Evaluate whether Quick Stats sparklines need a more polished look than the current hand-rolled inline SVG; if so, adopt a lightweight Svelte-4-compatible option (e.g. Chart.js via `<canvas>`, framework-agnostic) — only swap if it's a clear visual improvement, otherwise keep the current `Sparkline.svelte` | ⬜ No | ⏸️ deferred — kept `Sparkline.svelte`, looks fine at current size |
| UI-P7-8 | Validate: `npm run check`, `npm run test:unit`, and a visual pass in the browser across expanded/collapsed sidebar and scrolled states | ⬜ No | ✅ done |

Note: the app was upgraded to **Svelte 5.56 + Vite 6 + bits-ui v2** (from the
Svelte-4-only stack used earlier in this plan) as a prerequisite for this
phase, unblocking `mode-watcher`, `melt` (Melt UI v2), `daisyui`, and
`@fontsource/inter`.

### Phase 7 follow-up fixes (post-review)

| ID | Task | Backend needed? | Status |
|---|---|---|---|
| UI-P7-9 | Header: right-align search + status/notification/help/avatar as one right-hand cluster (was stretching full-width); shrink header height/icon sizes to match reference density | ⬜ No | ✅ done |
| UI-P7-10 | Layout: drop `mx-auto max-w-7xl` centering on `<main>` (caused a growing empty gutter/misaligned scrollbar once the sidebar collapsed); content now spans full available width with consistent padding | ⬜ No | ✅ done |
| UI-P7-11 | Floating buttons: removed daisyUI classes that fought with fixed sizing on `ScrollFab`/`AssistantBubble` (caused off-center icons); fixed a missing `relative` on the assistant trigger that made its ping-pulse ring render off-position | ⬜ No | ✅ done |
| UI-P7-12 | Footer: added the shield-check brand icon, `\|` separators between version/copyright and between nav links, left-aligned text (was missing icon and used a plain `·` dot) | ⬜ No | ✅ done |
| UI-P7-13 | Cards/buttons: reduced `Card` radius (`rounded-xl`→`rounded-lg`) + added `overflow-hidden`; reduced `CardTitle` weight/size; changed tool-card "Launch" buttons from `rounded-full` pills to `rounded-lg`, matching the reference's rectangular buttons | ⬜ No | ✅ done |
| UI-P7-14 | Section icons: added a small colored icon badge next to each dashboard card title (Recent AI Runs, Approval Queue, Provider Status, Quick Stats) matching the reference; added the missing robot avatar to the Provider Status card | ⬜ No | ✅ done |
| UI-P7-15 | Quick Stats charts: current per-stat `Sparkline.svelte` (hand-rolled inline SVG) kept — revisit only if a richer chart (e.g. layerchart, now viable on Svelte 5) is explicitly requested | ⬜ No | ⏸️ deferred, no action needed unless requested |

### Phase 7 second follow-up (card content deep-dive)

| ID | Task | Backend needed? | Status |
|---|---|---|---|
| UI-P7-16 | Badge/status text: removed `uppercase` from the shared `Badge` component and the sidebar "Soon" pill — status/risk values now render in their natural case ("Completed", "Failed", "High", "Soon") instead of all-caps, matching the reference | ⬜ No | ✅ done |
| UI-P7-17 | Provider Status card: restructured into a two-column layout — provider icon/name/model/environment on the left, a bordered "Usage Today" sub-panel (Requests/Tokens/Avg latency/Error rate) on the right — matching the reference instead of one stacked column | ⬜ No | ✅ done |
| UI-P7-18 | Quick Stats: removed the per-tile border box for a cleaner, borderless grid matching the reference | ⬜ No | ✅ done |
| UI-P7-19 | Approval Queue: replaced individually-bordered row boxes with a plain divided list (border only between rows), matching the reference's list style | ⬜ No | ✅ done |
| UI-P7-20 | System Notice: removed the teal-tinted background/border for a neutral card background, matching the reference | ⬜ No | ✅ done |

## Working agreement for this plan

1. Pick the next `⬜` task top-to-bottom within a phase.
2. If it says "stub only" — build UI with inline sample data, label it clearly,
   do not touch the API.
3. If it reuses an existing router — wire real data via `$lib/api.ts`, same
   pattern as `applications`/`governance` pages today.
4. Update this file's status column after each task lands.
