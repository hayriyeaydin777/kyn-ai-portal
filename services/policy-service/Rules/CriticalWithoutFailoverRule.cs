using PolicyService.Contracts;

namespace PolicyService.Rules;

/// <summary>Flags high/critical applications with no failover dependency documented.</summary>
public sealed class CriticalWithoutFailoverRule : IPolicyRule
{
    private static readonly HashSet<string> HighCriticalityLevels = new(StringComparer.OrdinalIgnoreCase)
    {
        "high",
        "critical"
    };

    public string RuleId => "R002";

    public IEnumerable<Finding> Evaluate(PolicyRequestV1 request)
    {
        var isHighCriticality = HighCriticalityLevels.Contains(request.Criticality);
        var hasFailover = request.Dependencies.Any(
            d => string.Equals(d.DependencyType, "failover", StringComparison.OrdinalIgnoreCase)
        );

        if (isHighCriticality && !hasFailover)
        {
            yield return new Finding(
                RuleId,
                FindingSeverity.High,
                $"Application criticality is '{request.Criticality}' but no failover dependency is documented.",
                new[] { nameof(request.Criticality), nameof(request.Dependencies) }
            );
        }
    }
}
