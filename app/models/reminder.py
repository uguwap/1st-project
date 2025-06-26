from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class ReminderBase(SQLModel):
    request_id: UUID
    remind_at: datetime
    is_sent: bool = False

class Reminder(ReminderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReminderCreate(ReminderBase):
    pass

class ReminderRead(ReminderBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
