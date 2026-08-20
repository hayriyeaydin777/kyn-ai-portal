using PolicyService.Contracts;
using PolicyService.Rules;
using Xunit;

namespace PolicyService.Tests;

public class PolicyEngineTests
{
    [Fact]
    public void Evaluate_IsDeterministic_SameInputSameOutput()
    {
        var engine = new PolicyEngine(
            new IPolicyRule[]
            {
                new MissingDependenciesRule(),
                new CriticalWithoutFailoverRule(),
                new TooManyCriticalDependenciesRule()
            }
        );
        var request = new PolicyRequestV1("Northstar Claims Service", "critical", Array.Empty<DependencyInput>());

        var first = engine.Evaluate(request);
        var second = engine.Evaluate(request);

        Assert.Equal(first.Findings.Count, second.Findings.Count);
        Assert.Equal(
            first.Findings.Select(f => f.RuleId).OrderBy(id => id),
            second.Findings.Select(f => f.RuleId).OrderBy(id => id)
        );
    }

    [Fact]
    public void Evaluate_CombinesFindingsFromAllRules()
    {
        var engine = new PolicyEngine(
            new IPolicyRule[] { new MissingDependenciesRule(), new CriticalWithoutFailoverRule() }
        );
        var request = new PolicyRequestV1("Northstar Claims Service", "critical", Array.Empty<DependencyInput>());

        var response = engine.Evaluate(request);

        Assert.Equal(2, response.Findings.Count);
        Assert.Contains(response.Findings, f => f.RuleId == "R001");
        Assert.Contains(response.Findings, f => f.RuleId == "R002");
    }
}
