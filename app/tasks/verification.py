from app.tasks.celery_app import celery_app
from app.core.config import settings
import requests

@celery_app.task
def send_verification_code_task(phone:str, code:str):
    message = f"Ваш код подтверждения {code}"

    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
    }






