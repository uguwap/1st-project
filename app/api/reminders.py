from fastapi import APIRouter, Depends, Query
from sqlmodel import select, and_
from typing import Optional, List
from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reminder import Reminder
from app.database.session import get_db
from fastapi import HTTPException
from app.models.reminder import Reminder, ReminderUpdate
router = APIRouter(prefix="/reminders", tags=["reminders"])

@router.get("/", response_model=List[Reminder])
async def get_reminders(
    status: Optional[str] = Query(None),
    contact_date: Optional[date] = Query(None),
    request_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    global query
    query: select(Reminder)
    filters = []

    if status:
        filters.append(Reminder.status == status)
    if contact_date:
        filters.append(Reminder.contact_date == contact_date)
    if request_id:
        filters.append(Reminder.request_id == request_id)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execure(query)
    return result.scalars().all()

@router.patch("/{reminder_id}", response_model=Reminder)
async def update_reminder(
    reminder_id: UUID,
    data: ReminderUpdate,
    db: AsyncSession = Depends(get_db)
):
    reminder = await db.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Напоминание не найдено")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reminder, key, value)

    await db.commit()
    await db.refresh(reminder)
    return reminder