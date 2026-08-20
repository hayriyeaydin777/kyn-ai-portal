using System.Text.Json.Serialization;
using PolicyService.Contracts;
using PolicyService.Rules;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter());
});
builder.Services.AddSingleton<IEnumerable<IPolicyRule>>(
    new IPolicyRule[]
    {
        new MissingDependenciesRule(),
        new CriticalWithoutFailoverRule(),
        new TooManyCriticalDependenciesRule()
    }
);
builder.Services.AddSingleton<PolicyEngine>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapPost(
    "/v1/assessments/evaluate",
    (PolicyRequestV1 request, PolicyEngine engine) =>
    {
        if (string.IsNullOrWhiteSpace(request.ApplicationName))
        {
            return Results.BadRequest(new { title = "Invalid request", detail = "ApplicationName is required." });
        }

        return Results.Ok(engine.Evaluate(request));
    }
);

app.Run();

public partial class Program { }
