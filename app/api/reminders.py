from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.session import get_db
from app.models.reminder import Reminder, ReminderRead

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.get("/", response_model=list[ReminderRead])
def get_all_reminders(session: Session = Depends(get_db)):
    reminders = session.exec(select(Reminder)).all()
    return reminders


@router.get("/{reminder_id}", response_model=ReminderRead)
def get_reminder(reminder_id: str, session: Session = Depends(get_db)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder
