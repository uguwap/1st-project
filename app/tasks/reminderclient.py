from app.tasks.celery_app import celery_app
from datetime import datetime

@celery_app.task
def send_feedback_reminder(phone: str):
    print(f"[{datetime.now()}] Напоминание отправлено клиенту: {phone}")
    # TODO: здесь логика отправки WhatsApp/Telegram

