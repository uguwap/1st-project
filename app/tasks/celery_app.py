from celery import Celery
from app.core.config import settings

celery_app = Celery(
    main="app",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL
)

celery_app.conf.timezone = "UTC"
