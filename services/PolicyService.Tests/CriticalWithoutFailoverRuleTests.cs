using PolicyService.Contracts;
using PolicyService.Rules;
using Xunit;

namespace PolicyService.Tests;

public class CriticalWithoutFailoverRuleTests
{
    private readonly CriticalWithoutFailoverRule _rule = new();

    [Theory]
    [InlineData("high")]
    [InlineData("critical")]
    public void Evaluate_HighCriticalityWithoutFailover_ReturnsFinding(string criticality)
    {
        var request = new PolicyRequestV1(
            "Northstar Claims Service",
            criticality,
            new[] { new DependencyInput("Aurora Message Bus", "messaging", "medium") }
        );

        var findings = _rule.Evaluate(request).ToList();

        Assert.Single(findings);
        Assert.Equal(FindingSeverity.High, findings[0].Severity);
    }

    [Fact]
    public void Evaluate_HighCriticalityWithFailover_ReturnsNoFinding()
    {
        var request = new PolicyRequestV1(
            "Northstar Claims Service",
            "critical",
            new[] { new DependencyInput("Backup Region", "failover", "high") }
        );

        var findings = _rule.Evaluate(request).ToList();

        Assert.Empty(findings);
    }

    [Fact]
    public void Evaluate_LowCriticalityWithoutFailover_ReturnsNoFinding()
    {
        var request = new PolicyRequestV1("Atlas Messaging Service", "low", Array.Empty<DependencyInput>());

        var findings = _rule.Evaluate(request).ToList();

        Assert.Empty(findings);
    }
}
