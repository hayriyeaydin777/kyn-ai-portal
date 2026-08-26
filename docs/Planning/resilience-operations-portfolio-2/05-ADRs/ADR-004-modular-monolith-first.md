# Start with a modular monolith

## Status
Accepted

## Decision
Keep primary modules in one FastAPI deployable; extract only with scaling, security, ownership, or release-independence evidence.

## Consequences
Implementation and tests must make this decision visible. Exceptions require an ADR update.
