from fastapi import FastAPI

from app.routers import health

app = FastAPI(title="Resilience Operations & AI Engineering Portal API")

app.include_router(health.router)
