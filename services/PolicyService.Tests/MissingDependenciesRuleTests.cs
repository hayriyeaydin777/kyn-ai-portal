using PolicyService.Contracts;
using PolicyService.Rules;
using Xunit;

namespace PolicyService.Tests;

public class MissingDependenciesRuleTests
{
    private readonly MissingDependenciesRule _rule = new();

    [Fact]
    public void Evaluate_NoDependencies_ReturnsFinding()
    {
        var request = new PolicyRequestV1("Northstar Claims Service", "medium", Array.Empty<DependencyInput>());

        var findings = _rule.Evaluate(request).ToList();

        Assert.Single(findings);
        Assert.Equal("R001", findings[0].RuleId);
        Assert.Equal(FindingSeverity.Medium, findings[0].Severity);
    }

    [Fact]
    public void Evaluate_HasDependencies_ReturnsNoFinding()
    {
        var request = new PolicyRequestV1(
            "Northstar Claims Service",
            "medium",
            new[] { new DependencyInput("Synthetic Identity Provider", "auth", "medium") }
        );

        var findings = _rule.Evaluate(request).ToList();

        Assert.Empty(findings);
    }
}
