from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from pydantic import constr

class UserBase(SQLModel):
    username: str

class UserCreate(UserBase):
    password: constr(min_length=6)
    is_admin: bool = False

    class Config:
        from_attributes = True

class UserLogin(SQLModel):
    username: str
    password: str

class TokenResponse(SQLModel):
    access_token: str
    token_type: str

class UserRead(UserBase):
    id: UUID
    is_admin: bool

    class Config:
        from_attributes = True

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_admin: bool = False




