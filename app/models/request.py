from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class RequestBase(SQLModel):
    title: str # надо сделать что то с этим полем, чтобы название заявки, отображало ее сущность. Например: город и цена или тип насекомы и город, чтобы клиент сам не называл заявку так как хочет, а это было видно только у админа (исполнителя заявки)
    city: str
    processed_at: datetime # тоже сомнительно, клиент это не должен указывать, это у нас указывает админ так же как и источник и способ обработки
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