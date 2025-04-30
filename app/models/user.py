from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import constr


class UserBase(SQLModel):
    username: str
    phone: str = Field(..., regex=r"^8\d{10}$")


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: constr(min_length=6)

    class Config:
        from_attributes = True


class UserLogin(SQLModel):
    username: str
    password: str


class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True





