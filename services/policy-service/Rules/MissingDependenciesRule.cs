using PolicyService.Contracts;

namespace PolicyService.Rules;

/// <summary>Flags applications with no documented dependencies, which blocks recovery planning.</summary>
public sealed class MissingDependenciesRule : IPolicyRule
{
    public string RuleId => "R001";

    public IEnumerable<Finding> Evaluate(PolicyRequestV1 request)
    {
        if (request.Dependencies.Count == 0)
        {
            yield return new Finding(
                RuleId,
                FindingSeverity.Medium,
                "No dependencies documented for this application.",
                new[] { nameof(request.Dependencies) }
            );
        }
    }
}
