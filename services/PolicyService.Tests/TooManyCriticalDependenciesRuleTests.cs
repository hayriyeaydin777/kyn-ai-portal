using PolicyService.Contracts;
using PolicyService.Rules;
using Xunit;

namespace PolicyService.Tests;

public class TooManyCriticalDependenciesRuleTests
{
    private readonly TooManyCriticalDependenciesRule _rule = new();

    [Fact]
    public void Evaluate_MoreThanThresholdCriticalDependencies_ReturnsFinding()
    {
        var dependencies = Enumerable
            .Range(1, 3)
            .Select(i => new DependencyInput($"Dependency {i}", "service", "critical"))
            .ToArray();
        var request = new PolicyRequestV1("Northstar Claims Service", "medium", dependencies);

        var findings = _rule.Evaluate(request).ToList();

        Assert.Single(findings);
        Assert.Equal(FindingSeverity.Medium, findings[0].Severity);
    }

    [Fact]
    public void Evaluate_AtOrBelowThreshold_ReturnsNoFinding()
    {
        var dependencies = new[]
        {
            new DependencyInput("Dependency 1", "service", "critical"),
            new DependencyInput("Dependency 2", "service", "critical")
        };
        var request = new PolicyRequestV1("Northstar Claims Service", "medium", dependencies);

        var findings = _rule.Evaluate(request).ToList();

        Assert.Empty(findings);
    }
}
