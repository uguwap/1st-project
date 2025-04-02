
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class RequestBase(SQLModel):
    title: str
    city: str
    processed_at: datetime
    price: float
    insect_type: str
    treatment: str
    source: str
    status: str = Field(default="В работе") # в работе | завершено | отменено

class RequestCreate(RequestBase):
    pass

class RequestUpdate(RequestBase):
    title: Optional[str] = None
    city: Optional[str] = None
    processed_at: Optional[datetime] = None
    price: Optional[float] = None
    insect_type: Optional[str] = None
    treatment: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None

class RequestRead(RequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Request(RequestBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)



