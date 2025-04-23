from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class ClientSource(str, Enum):
    site = "site"
    call = "call"
    ad = "ad"
    referral = "referral"

class ClientBase(SQLModel):
    name: str
    phone: str
    address: str
    city: str
    source: Optional[ClientSource] = None

class Client(ClientBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ClientRead(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True






