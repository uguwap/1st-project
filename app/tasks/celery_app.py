from celery import Celery
from app.core.config import settings
from app.tasks.send_reminder_task import send_reminder

celery = Celery(
    "study",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
)

celery.conf.task_routes = {
    "app.tasks.send_reminder_task.send_reminder": {"queue": "reminders"}
}

