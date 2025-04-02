from email.mime import application

from fastapi import FastAPI, Query, Depends
from fastapi import FastAPI
from app.api.v1 import router as requests_router
from app.api.auth import router as auth_router
from app.api.reminders import router as reminders_router

app = FastAPI(
    title="Заявки",
    version="1.0.0"
)

app.include_router(requests_router)
app.include_router(auth_router)

app.include_router(reminders_router)
















