from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import ConfigDict

class CompletedRequest(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    original_request_id: UUID

    city: str
    processed_at: datetime
    client_phone: str
    insect_type: str
    treatment: str
    source: str
    address: str
    comment: str | None = None
    price: int

    created_at: datetime = Field(default_factory=datetime.utcnow)

class CompletedRequestRead(SQLModel):
    id: UUID
    original_request_id: UUID
    city: str
    processed_at: datetime
    client_phone: str
    insect_type: str
    treatment: str
    source: str
    address: str
    comment: str | None = None
    price: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



