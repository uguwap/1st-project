from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import date


class ReminderBase(SQLModel):
    request_id: UUID
    contact_date: date
    status: str = "Ожидает"


class Reminder(ReminderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class ReminderUpdate(ReminderBase):
    status: str










class ReminderRead(ReminderBase):
    id: UUID

    class Config:
        from_attributes = True

