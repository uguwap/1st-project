from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import date


class OrderBase(SQLModel):
    status: str
    city: str
    insect_type: str
    source: Optional[str] = None
    date: date


class Order(OrderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    phone: str
    address: str

class OrderRead(OrderBase):
    id: UUID
    phone: int
    address: str

    class Config:
        from_attributes = True






