from celery import Celery

celery_app = Celery(
    "reminders",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.timezone = "UTC"




