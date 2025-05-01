from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from datetime import datetime, timedelta, date

from app.database.session import get_db
from app.models.request import Request
from app.models.completed_request import CompletedRequest

router = APIRouter(prefix="/analytics", tags=["Аналитика"])


@router.get("/summary")
async def get_summary(
    session: AsyncSession = Depends(get_db)
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    total_requests = await session.execute(select(func.count()).select_from(Request))
    total_completed = await session.execute(select(func.count()).select_from(CompletedRequest))

    today_created = await session.execute(
        select(func.count()).select_from(Request).where(func.date(Request.created_at) == today)
    )
    today_completed = await session.execute(
        select(func.count()).select_from(CompletedRequest).where(func.date(CompletedRequest.created_at) == today)
    )

    week_created = await session.execute(
        select(func.count()).select_from(Request).where(Request.created_at >= start_of_week)
    )
    week_completed = await session.execute(
        select(func.count()).select_from(CompletedRequest).where(CompletedRequest.created_at >= start_of_week)
    )

    return {
        "total_requests": total_requests.scalar(),
        "completed_requests": total_completed.scalar(),
        "today": {
            "created": today_created.scalar(),
            "completed": today_completed.scalar(),
        },
        "this_week": {
            "created": week_created.scalar(),
            "completed": week_completed.scalar(),
        }
    }


@router.get("/filter")
async def filter_requests(
    city: str = Query(None),
    insect_type: str = Query(None),
    source: str = Query(None),
    treatment: str = Query(None),
    from_date: date = Query(None),
    to_date: date = Query(None),
    only_completed: bool = Query(False),
    sort_by: str = Query("created_at", description="Поле для сортировки: created_at, city, price и т.д."),
    sort_desc: bool = Query(True, description="True — по убыванию, False — по возрастанию"),
    offset: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(50, ge=1, le=100, description="Сколько записей вернуть"),
    session: AsyncSession = Depends(get_db)
):
    model = CompletedRequest if only_completed else Request
    stmt = select(model)

    if city:
        stmt = stmt.where(model.city == city)
    if insect_type:
        stmt = stmt.where(model.insect_type == insect_type)
    if source:
        stmt = stmt.where(model.source == source)
    if treatment:
        stmt = stmt.where(model.treatment == treatment)
    if from_date:
        stmt = stmt.where(model.created_at >= from_date)
    if to_date:
        stmt = stmt.where(model.created_at <= to_date)

    # Сортировка
    sort_column = getattr(model, sort_by, None)
    if sort_column is not None:
        stmt = stmt.order_by(sort_column.desc() if sort_desc else sort_column.asc())

    # Пагинация
    stmt = stmt.offset(offset).limit(limit)

    results = await session.execute(stmt)
    return results.scalars().all()