# 11. AI Engineering Workspace
## Capabilities
Code Review, Test Generator, and Documentation Generator.
## Code Review
Read-only source input; static-analysis tool results; security, maintainability, performance, and testing findings; suggested patch; human-selected acceptance only.
## Test Generator
Generate unit, integration, and boundary-case drafts from approved source/contracts. Execution occurs only in an isolated test environment after approval.
## Documentation Generator
Create versioned README, API notes, sequence descriptions, and architecture notes with source references.
## Controls
Secret detection, size limits, supported-language allowlist, no repository write by default, schema validation, safe rendering, prompt-injection defense, audit, provider telemetry.
## Evidence
Each suggestion links to source lines, tool results, standards, or test behavior. Model confidence is not treated as correctness.
