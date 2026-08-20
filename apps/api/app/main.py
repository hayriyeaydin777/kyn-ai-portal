from fastapi import FastAPI

from app.logging_config import configure_logging
from app.middleware.correlation import correlation_id_middleware
from app.routers import health

configure_logging()

app = FastAPI(title="Resilience Operations & AI Engineering Portal API")

app.middleware("http")(correlation_id_middleware)
app.include_router(health.router)
