from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AnalyticsRaw(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int
    insect_type: str
    city: str
    source: str
    processed_at: datetime
    created_at: datetime
    treatment: str
    price: Optional[float]
    comment: Optional[str]

    executor_id: int
    executor_name: str
    executor_phone: Optional[str]

    recorded_at: datetime = Field(default_factory=datetime.utcnow)
