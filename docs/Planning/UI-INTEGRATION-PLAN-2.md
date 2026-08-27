# Workspace UI Completion Plan

This plan continues the `/workspace` visual pass from `UI-INTEGRATION-PLAN.md`.
It groups related visual work into reviewable milestones so the remaining work is
validated as coherent screens, not individual pixel changes.

## Working Rules

- Reference: `docs/Designs/ai-workspace.png`.
- Preserve existing routes and sample-data behavior unless a task explicitly
  changes navigation.
- Complete each milestone with `npm run check`, `npm run test:unit`, and a
  desktop plus narrow-viewport browser review.
- Record a screenshot comparison and remaining deltas before starting the next
  milestone.

## Completed In This Change

- [x] Restore dark sidebar palette and add a clock-based unavailable-item cue
  with an accessible `Coming soon` hover tooltip.
- [x] Rework Workspace Home typography to use semibold headings and values.
- [x] Activate the Prompt Lab card visually and align it with teal tool styling.
- [x] Add an outlined split control for `New AI Run` and position it before
  Workspace settings.
- [x] Put Recent AI Runs and Approval Queue in a balanced desktop two-column
  layout, compact table metrics, outline status/risk badges, and align first
  columns with card headers.
- [x] Rework Provider Status, Usage Today, Quick Stats, and System Notice toward
  the reference layout and palette.
- [x] Align floating controls and replace the assistant popover trigger with a
  deterministic local open/close state.

## Milestone A: Workspace Desktop Baseline

- [ ] Capture a fixed desktop viewport screenshot of `/workspace` and compare
  it side-by-side with the reference.
- [ ] Tune global surface colors, card borders, shadows, and spacing as one
  shared visual system.
- [ ] Verify card title, body, label, and action type scales across all dashboard
  sections.
- [ ] Confirm tool card heights, icon tile sizes, and launch controls align as a
  single row.

## Milestone B: Dashboard Data Panels

- [ ] Finalize Recent AI Runs and Approval Queue column widths, truncation, row
  heights, and badge rendering at the agreed desktop viewport.
- [ ] Finalize Provider Status two-panel proportions and narrow-card fallback.
- [ ] Finalize Quick Stats tile density, cyan sparklines, and readable delta
  labels without clipping.
- [ ] Finalize System Notice inner panel contrast and floating assistant clearance.

## Milestone C: Responsive Workspace

- [ ] Validate the tool-card grid, action row, tables, and lower dashboard cards
  at narrow, tablet, and desktop widths.
- [ ] Ensure no table content, header action, tooltip, popup, or floating button
  overflows or obscures content.
- [ ] Define intentional responsive table behavior: compact columns or a safe
  scroll container where all data must remain visible.
- [ ] Verify collapsed and expanded sidebar behavior at each viewport.

## Milestone D: Interaction Polish

- [ ] Validate all `Coming soon` clock tooltips on pointer hover and keyboard
  focus; keep the arrow cursor for unavailable items.
- [ ] Verify the New AI Run split menu opens, closes, and keeps focus correctly.
- [ ] Verify the assistant opens/closes repeatedly, closes on Escape, and never
  overlaps the scroll control, footer, or popup content.
- [ ] Verify scroll-button direction and visibility at top, mid-page, and bottom.

## Milestone E: Final Regression Pass

- [ ] Run `npm run check`.
- [ ] Run `npm run test:unit`.
- [ ] Review `/workspace` against the reference at desktop and narrow widths.
- [ ] Review existing `/applications`, `/governance`, and Workspace tool routes
  for shared-primitive regressions.
- [ ] Update this plan with accepted deviations and completion state.