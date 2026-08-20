namespace PolicyService.Contracts;

public enum FindingSeverity
{
    Low,
    Medium,
    High,
    Critical
}

public sealed record Finding(
    string RuleId,
    FindingSeverity Severity,
    string Message,
    IReadOnlyList<string> EvidenceFields
);

public sealed record PolicyResponseV1(IReadOnlyList<Finding> Findings);
