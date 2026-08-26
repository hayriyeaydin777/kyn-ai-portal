# Use ASP.NET Core for a focused policy service

## Status
Accepted

## Decision
The .NET 10 service evaluates versioned deterministic readiness rules and has no direct database access. Fold it into FastAPI if independence is not justified.

## Consequences
Implementation and tests must make this decision visible. Exceptions require an ADR update.
