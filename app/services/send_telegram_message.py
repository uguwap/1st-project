import requests
from app.core.config import settings

def send_telegram_message(chat_id: int, text: str) -> None:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram error: {response.text}")

