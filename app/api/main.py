from fastapi import FastAPI
from app.api.requests import router as requests_router
from app.api.auth import router as auth_router
from app.api.reminders import router as reminders_router
from app.api.analytics import router as analytics_router
from app.api.ml import router as ml_router
from app.api.analytics_v2 import router as analytics_v2_router
app = FastAPI(
    title="Study Project API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
app.include_router(analytics_router)
# /requests
app.include_router(requests_router)

# /auth
app.include_router(auth_router)

# /reminders
app.include_router(reminders_router)

app.include_router(ml_router)

app.include_router(analytics_v2_router)


















