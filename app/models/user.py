from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4


class UserBase(SQLModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserRead(UserBase):
    id: UUID
    is_admin: bool

    class Config:
        from_attributes = True


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_admin: bool = False




