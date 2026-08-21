from fastapi import FastAPI

from app.logging_config import configure_logging
from app.middleware.correlation import correlation_id_middleware
from app.routers import (
    applications,
    approvals,
    assessments,
    briefs,
    code_reviews,
    dependencies,
    evidence,
    health,
    modernization_cases,
    modernization_recommendations,
    test_generations,
)

configure_logging()

app = FastAPI(title="Resilience Operations & AI Engineering Portal API")

app.middleware("http")(correlation_id_middleware)
app.include_router(health.router)
app.include_router(applications.router)
app.include_router(dependencies.router)
app.include_router(evidence.router)
app.include_router(assessments.router)
app.include_router(briefs.router)
app.include_router(approvals.router)
app.include_router(modernization_cases.router)
app.include_router(modernization_recommendations.router)
app.include_router(code_reviews.router)
app.include_router(test_generations.router)
