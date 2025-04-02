from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
import datetime

class ClientBase(SQLModel):
    name: str
    phone: int
    address: str
    city: str
    source: Optional[str] = None


class Client(ClientBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.datetime.now)


class ClientRead(ClientBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True



