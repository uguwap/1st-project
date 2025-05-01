import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.models.telegram_profile import TelegramProfile
from app.services.logger_service import log_event

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

router = Router()
dp = Dispatcher()
dp.include_router(router)

# Стартовая клавиатура
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Стартуем!")]
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Жми кнопку — не стесняйся"
)

# Клавиатура после старта
action_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привязать Telegram")]
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Выбирай, что делаем"
)

@router.message(CommandStart())
async def start_handler(message: Message):
    async for session in get_db():
        await log_event(
            session=session,
            event_type="start",
            chat_id=message.chat.id,
            payload="/start"
        )
    await message.answer(
        "Здарова, старина! Готов к делу? Жми кнопку ниже и поехали.",
        reply_markup=start_keyboard
    )

@router.message(F.text == "Стартуем!")
async def show_actions(message: Message):
    await message.answer("Чего изволишь?", reply_markup=action_keyboard)

@router.message(F.text == "Привязать Telegram")
async def request_login_input(message: Message):
    await message.answer("Кидай свой номер телефона")

@router.message(F.text.regexp(r"^8\d{10}$|^[a-zA-Z0-9_]+$"))
async def handle_login_input(message: Message):
    login_input = message.text.strip()

    async for session in get_db():
        stmt = select(User).where((User.username == login_input) | (User.phone == login_input))
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            await log_event(
                session=session,
                event_type="login_failed",
                chat_id=message.chat.id,
                payload=f"Пользователь {login_input} не найден"
            )
            await message.answer("Такого пользователя у нас нет. Попробуй снова.")
            return

        existing = await session.execute(
            select(TelegramProfile).where(TelegramProfile.user_id == user.id)
        )
        if existing.scalar_one_or_none():
            await log_event(
                session=session,
                event_type="already_linked",
                user_id=user.id,
                chat_id=message.chat.id,
                payload="Telegram уже привязан ранее"
            )
            await message.answer("Этот Telegram уже привязан к учётке. Всё под контролем.")
            return

        profile = TelegramProfile(
            user_id=user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            created_at=message.date.replace(tzinfo=None)
        )
        session.add(profile)
        await session.commit()

        await log_event(
            session=session,
            event_type="login_success",
            user_id=user.id,
            chat_id=message.chat.id,
            payload=f"Telegram привязан как {message.from_user.username}"
        )

    await message.answer("Красавчик! Telegram успешно привязан, ожидай напоминаний по заявкам!")

@router.message()
async def fallback_handler(message: Message):
    async for session in get_db():
        await log_event(
            session=session,
            event_type="unknown_command",
            chat_id=message.chat.id,
            payload=message.text
        )
    await message.answer("Я только по кнопкам. Не неси хуйню.")

async def main():
    print("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())