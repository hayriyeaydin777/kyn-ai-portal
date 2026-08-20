using PolicyService.Contracts;

namespace PolicyService.Rules;

public sealed class PolicyEngine
{
    private readonly IReadOnlyList<IPolicyRule> _rules;

    public PolicyEngine(IEnumerable<IPolicyRule> rules)
    {
        _rules = rules.ToList();
    }

    public PolicyResponseV1 Evaluate(PolicyRequestV1 request)
    {
        var findings = _rules.SelectMany(rule => rule.Evaluate(request)).ToList();
        return new PolicyResponseV1(findings);
    }
}
