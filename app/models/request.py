from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class RequestBase(SQLModel):
    title: str
    city: str
    processed_at: datetime
    client_price: float
    final_price: Optional[float] = None
    insect_type: str
    treatment: str
    source: str
    status: str = Field(default="В работе")
    phone: str
    address: str
    description: Optional[str] = None


class Request(RequestBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RequestCreate(RequestBase):
    pass


class RequestRead(RequestBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RequestUpdate(SQLModel):
    title: Optional[str] = None
    city: Optional[str] = None
    processed_at: Optional[datetime] = None
    client_price: Optional[float] = None
    final_price: Optional[float] = None
    insect_type: Optional[str] = None
    treatment: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None