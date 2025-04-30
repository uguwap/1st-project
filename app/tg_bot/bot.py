import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from app.core.config import settings
from app.models.user import User
from app.models.telegram_profile import TelegramProfile
from app.database.session import AsyncSessionLocal
from sqlalchemy.future import select
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

waiting_for_login = set()


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    chat_id = message.chat.id
    waiting_for_login.add(chat_id)
    await message.answer("👋 Привет! Введите ваш логин (username) или номер телефона...")


@dp.message(F.text)
async def handle_login_input(message: Message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in waiting_for_login:
        return

    async with AsyncSessionLocal() as session:
        stmt = select(User).where((User.username == text) | (User.phone == text))
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❌ Пользователь не найден. Попробуйте ещё раз.")
            return

        stmt = select(TelegramProfile).where(TelegramProfile.user_id == user.id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

        if profile:
            await message.answer("⚠️ Telegram уже привязан к этому аккаунту.")
            return

        new_profile = TelegramProfile(
            user_id=user.id,
            chat_id=chat_id,
            username=message.from_user.username,
            created_at=datetime.utcnow()
        )
        session.add(new_profile)
        await session.commit()

        await message.answer("✅ Telegram успешно привязан к вашей учётной записи!")
        waiting_for_login.remove(chat_id)


async def main():
    print("🤖 Bot started...")
    await dp.start_polling(bot)



