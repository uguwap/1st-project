from celery import shared_task
from sqlmodel import Session, select
from datetime import datetime

from app.database.session import sync_engine
from app.models.reminder import Reminder
from app.models.reminder_archive import ReminderArchive
from app.models.request import Request
from app.models.telegram_profile import TelegramProfile
from app.services.send_telegram_message import send_telegram_message


@shared_task
def send_reminder(reminder_id: str):
    print("Celery получил задачу!")

    with Session(sync_engine) as session:
        # Получаем напоминание
        reminder = session.get(Reminder, reminder_id)
        if not reminder or reminder.is_sent:
            return

        # Получаем заявку
        request = session.exec(
            select(Request).where(Request.id == reminder.request_id)
        ).first()
        if not request:
            return

        # Получаем TelegramProfile исполнителя
        tg_profile = session.exec(
            select(TelegramProfile).where(TelegramProfile.user_id == request.user_id)
        ).first()

        if not tg_profile:
            print("Telegram-профиль не найден. Напоминание не отправлено.")
            return

        # Формируем сообщение
        message = (
            f"Напоминание исполнителю:\n"
            f"Город: {request.city}\n"
            f"Адрес: {request.address}\n"
            f"Телефон клиента: {request.client_phone}"
        )

        # Отправляем в Telegram
        send_telegram_message(chat_id=tg_profile.chat_id, text=message)

        # Обновляем флаг is_sent
        reminder.is_sent = True
        session.add(reminder)

        # Архивируем
        archive = ReminderArchive(
            request_id=request.id,
            remind_at=reminder.remind_at,
            sent_at=datetime.utcnow(),
            message=message
        )
        session.add(archive)
        session.commit()
