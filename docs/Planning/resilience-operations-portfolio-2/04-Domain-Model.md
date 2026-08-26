# 04. Domain Model

Bounded contexts: Recovery Planning, Readiness Assessment, AI Assistance, and Platform Operations.

Aggregate roots:

- ApplicationProfile: name, description, criticality, owners, recovery objectives, lifecycle, version, timestamps.
- Dependency: application target, type, criticality, owner, recovery sequence.
- EvidenceArtifact: synthetic evidence metadata, classification, freshness, source reference, content hash.
- ReadinessAssessment: application, policy version, status, score, timestamps, correlation ID.
- Finding: rule ID, severity, explanation, evidence IDs, remediation hint, status.
- OrchestrationRun: assessment, intent, provider/model, prompt version, status, tokens, timing, correlation ID.
- GeneratedBrief: executive and engineering summaries, cited findings, questions, limitations, approval status.

Invariants: objectives are positive; updates use optimistic concurrency; findings cite rules and evidence; generated claims resolve to evidence IDs; rejected briefs are immutable; side effects require approval.
