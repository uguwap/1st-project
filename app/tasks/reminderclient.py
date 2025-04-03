from app.tasks.celery_app import celery_app
from datetime import datetime
import requests
from app.core.config import settings

@celery_app.task
def send_feedback_reminder(phone: str):
    message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Напоминание отправлено клиенту: {phone}"

    # Telegram
    telegram_url = (
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )
    telegram_data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(telegram_url, data=telegram_data)
        response.raise_for_status()
        print("Telegram: сообщение отправлено.")
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

    # WhatsApp
    whatsapp_payload = {
        "phone": phone,
        "body": message,
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            f"{settings.WHATSAPP_API_URL}?token={settings.WHATSAPP_API_TOKEN}",
            json=whatsapp_payload,
            headers=headers,
        )
        response.raise_for_status()
        print("WhatsApp: сообщение отправлено.")
    except Exception as e:
        print(f"Ошибка WhatsApp: {e}")
