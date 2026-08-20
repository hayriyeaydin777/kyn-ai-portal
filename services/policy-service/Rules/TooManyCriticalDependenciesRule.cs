using PolicyService.Contracts;

namespace PolicyService.Rules;

/// <summary>Flags applications with more than two critical dependencies (coordinated-failure risk).</summary>
public sealed class TooManyCriticalDependenciesRule : IPolicyRule
{
    private const int Threshold = 2;

    public string RuleId => "R003";

    public IEnumerable<Finding> Evaluate(PolicyRequestV1 request)
    {
        var criticalCount = request.Dependencies.Count(
            d => string.Equals(d.Criticality, "critical", StringComparison.OrdinalIgnoreCase)
        );

        if (criticalCount > Threshold)
        {
            yield return new Finding(
                RuleId,
                FindingSeverity.Medium,
                $"{criticalCount} critical dependencies increase coordinated-failure risk.",
                new[] { nameof(request.Dependencies) }
            );
        }
    }
}
