# 07. API Specifications

Use `/v1`, OpenAPI, resource-oriented URLs, validation, stable problem-details errors, correlation IDs, idempotency for critical creates, optimistic concurrency, pagination, authorization, and redacted logs.

```text
POST   /v1/applications
GET    /v1/applications
GET    /v1/applications/{applicationId}
PATCH  /v1/applications/{applicationId}
POST   /v1/applications/{applicationId}/dependencies
GET    /v1/applications/{applicationId}/dependencies
POST   /v1/applications/{applicationId}/evidence
POST   /v1/applications/{applicationId}/assessments
GET    /v1/assessments/{assessmentId}
GET    /v1/assessments/{assessmentId}/findings
POST   /v1/assessments/{assessmentId}/briefs
GET    /v1/orchestration-runs/{runId}
GET    /v1/briefs/{briefId}
POST   /v1/briefs/{briefId}/approval-decisions
GET    /health/live
GET    /health/ready
```

The policy service exposes `POST /v1/policies/evaluate`, accepting a versioned application/dependency/evidence contract and returning deterministic findings with rule IDs, severity, explanations, and evidence IDs.
