from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class ReminderArchiveBase(SQLModel):
    request_id: UUID
    remind_at: datetime
    sent_at: datetime
    message: str

class ReminderArchive(ReminderArchiveBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    model_config = ConfigDict(from_attributes=True)