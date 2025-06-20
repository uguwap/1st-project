from pydantic import BaseModel
from typing import Dict

class AnalyticsSummaryV2(BaseModel):
    total_requests: int
    avg_price: float
    top_cities: Dict[str, float]
    top_executors: Dict[str, float]



