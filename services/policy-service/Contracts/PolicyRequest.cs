namespace PolicyService.Contracts;

public sealed record DependencyInput(string Name, string DependencyType, string Criticality);

public sealed record PolicyRequestV1(
    string ApplicationName,
    string Criticality,
    IReadOnlyList<DependencyInput> Dependencies
);
