# 04. Domain Model
Bounded contexts: Recovery Planning, Assessment, Modernization Advisory, Engineering Assistance, Architecture Governance, Agent Management, AI Evaluation, Platform Operations.

Key aggregates: ApplicationProfile, Dependency, EvidenceArtifact, ReadinessAssessment, Finding, ModernizationCase, ModernizationRecommendation, CodeReviewRun, GeneratedTestSuite, DocumentationDraft, ArchitectureDecision, ArchitectureReview, AgentDefinition, AgentVersion, PromptVersion, EvaluationDataset, EvaluationRun, OrchestrationRun, ApprovalDecision, AuditEvent.

Invariants: synthetic inputs only; deterministic facts remain separate from generated recommendations; unknown citations are rejected; generated patches/tests/docs are drafts; accepted ADRs are immutable versions; agent tools are allowlisted; consequential actions require approval.
