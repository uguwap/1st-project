from typing import List, Optional, TYPE_CHECKING
from pydantic import EmailStr, computed_field, BaseModel
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, Relationship, SQLModel
import datetime
import uuid

class UserBase(SQLModel):
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True

class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)



