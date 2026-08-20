using PolicyService.Contracts;

namespace PolicyService.Rules;

public interface IPolicyRule
{
    string RuleId { get; }

    IEnumerable<Finding> Evaluate(PolicyRequestV1 request);
}
