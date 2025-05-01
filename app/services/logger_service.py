from datetime import datetime
from uuid import UUID
from typing import Optional
from app.models.bot_logs import BotLog
from sqlalchemy.ext.asyncio import AsyncSession

async def log_event(
    session: AsyncSession,
    event_type: str,
    user_id: Optional[UUID] = None,
    chat_id: Optional[int] = None,
    payload: Optional[str] = None
):
    log = BotLog(
        event_type=event_type,
        user_id=user_id,
        chat_id=chat_id,
        message=payload,
        created_at=datetime.utcnow()
    )
    session.add(log)
    await session.commit()