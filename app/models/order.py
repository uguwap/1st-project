import uuid
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr, computed_field, BaseModel
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, Relationship, SQLModel
import datetime

if TYPE_CHECKING:
    pass

class OrderBase(SQLModel):
    status: str
    city: str
    insect_type: str
    source: Optional[str]
    date: datetime.date

class Order(OrderBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    phone: str
    address: str




