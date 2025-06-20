from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import Optional

from datetime import datetime

from app.database.session import get_db
from app.models.analytics_raw import AnalyticsRaw
from app.schemas.analyticsv2 import AnalyticsSummaryV2

router = APIRouter()

@router.get("/summary_v2", response_model=AnalyticsSummaryV2)
def get_summary_v2(
        city: Optional[str] = Query(None),
        executor: Optional[str] = Query(None),
        date_from: Optional[datetime] = Query(None),
        date_to: Optional[datetime] = Query(None),
        session: Session = Depends(get_db),
):

    query = select(AnalyticsRaw)

    if city:
        query = query.where(AnalyticsRaw.city == city)
    if executor:
        query = query.where(AnalyticsRaw.executor == executor)
    if date_from:
        query = query.where(AnalyticsRaw.processed_at >= date_from)
    if date_to:
        query = query.where(AnalyticsRaw.processed_at <= date_to)

    rows = session.exec(query).all()

    total_requests = len(rows)
    avg_price = round(sum([r.price or 0 for r in rows]) / total_requests, 2) if total_requests else 0

    top_cities = {}
    for row in rows:
        if row.city:
            top_cities[row.city] = top_cities.get(row.city, 0) + 1
    sorted_cities = dict(sorted(top_cities.items(), key=lambda x: x[1], reverse=True)[:3])

    top_executors = {}
    for row in rows:
        if row.executor_name:
            top_executors[row.executor_name] = top_executors.get(row.executor_name, 0) + 1
    sorted_executors = dict(sorted(top_executors.items(), key=lambda x: x[1], reverse=True)[:3])

    return AnalyticsSummaryV2(
        total_requests=total_requests,
        avg_price=avg_price,
        top_cities=sorted_cities,
        top_executors=sorted_executors
    )


