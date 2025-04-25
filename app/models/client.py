from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import validator


class ClientSource(str, Enum):
    site = "site"
    call = "call"
    ad = "ad"
    referral = "referral"

class ClientBase(SQLModel):
    phone: str
    source: Optional[ClientSource] = None
    verification_code: Optional[str] = None
    verified: Optional[bool] = False

    @validator("phone")
    def validate_phone_format(cls, value):
        if not value.isdigit() or len(value) != 11 or not value.startswith("8"):
            raise ValueError("Номер телефона должен быть в формате 8123456789")
        return value


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






