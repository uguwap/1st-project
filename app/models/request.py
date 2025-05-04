from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class RequestBase(SQLModel):
    city: str
    processed_at: datetime
    client_phone: str
    insect_type: str
    treatment: str
    source: str
    status: bool = Field(default=False)
    address: str
    comment: Optional[str] = Field(default=None)
    price: int

class Request(RequestBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RequestCreate(RequestBase):
    pass


class RequestUpdate(SQLModel):
    city: Optional[str] = None
    processed_at: Optional[datetime] = None
    client_phone: Optional[str] = None
    insect_type: Optional[str] = None
    treatment: Optional[str] = None
    source: Optional[str] = None
    status: Optional[bool] = None
    address: Optional[str] = None
    comment: Optional[str] = None
    price: Optional[int] = None


class RequestRead(RequestBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

