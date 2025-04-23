from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import Optional, List
from uuid import UUID
from datetime import timedelta, datetime
from fastapi import Path
from app.models import User
from app.models.request import RequestCreate, RequestRead, RequestUpdate, Request
from app.models.client import Client
from app.core.dependencies import get_db, get_admin_user, convert_uuid, get_current_user
from app.tasks.reminderclient import send_feedback_reminder

router = APIRouter(prefix="/requests", tags=["Заявки"])


@router.post("/", response_model=RequestRead)
async def create_request(
    data: RequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    new_request = Request(
        **data.dict(),
        final_price=data.client_price,
        user_id=current_user.id
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request

@router.patch("/{request_id}", response_model=RequestRead) # обновление финальной цены
async def update_price(
        request_id: UUID,
        final_price: float,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_admin_user)
):
    req = await db.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    req.final_price = final_price
    await db.commit()
    await db.refresh(req)
    return req

@router.get("/my", response_model=list[RequestRead])
async def get_my_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Request).where(Request.user_id == current_user.id))
    return result.scalars().all()


@router.get("/stats/monthly-total")
async def get_monthly_total(
    db: AsyncSession = Depends(get_db)
):
    today = datetime.utcnow()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    result = await db.execute(
        select(func.sum(Request.final_price))
        .where(
            Request.status == "Завершено",
            Request.created_at >= start_of_month
        )
    )
    total = result.scalar() or 0
    return {"total": total}

@router.get("/", response_model=list[RequestRead])
async def list_requests(
    status: Optional[str] = None,
    city: Optional[str] = None,
    insect_type: Optional[str] = None,
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Request)
    filters = []

    if status:
        filters.append(Request.status == status)
    if city:
        filters.append(func.lower(Request.city).like(f"%{city.lower()}%"))
    if insect_type:
        filters.append(func.lower(Request.insect_type).like(f"%{insect_type.lower()}%"))
    if source:
        filters.append(func.lower(Request.source).like(f"%{source.lower()}%"))

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{request_id}", response_model=RequestRead)
async def get_request(
    request_id: str,
    db: AsyncSession = Depends(get_db)
):
    uuid = convert_uuid(request_id)
    result = await db.get(Request, uuid)
    if not result:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return result


@router.patch("/{request_id}", response_model=RequestRead)
async def update_request(
    request_id: UUID,
    data: RequestUpdate,
    db: AsyncSession = Depends(get_db)
):
    uuid = convert_uuid(request_id)
    req = await db.get(Request, uuid)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    old_status = req.status

    for field, value in data.dict(exclude_unset=True).items():
        setattr(req, field, value)

    is_completed = data.status == "Завершено" and old_status != "Завершено"
    if is_completed:
        client = Client(
            name=req.insect_type,
            phone=req.phone,
            address=req.address,
            city=req.city,
            source=req.source,
        )
        db.add(client)

    await db.commit()
    await db.refresh(req)

    if is_completed:
        eta = datetime.utcnow() + timedelta(days=10)
        send_feedback_reminder.apply_async((req.phone,), eta=eta)

    return req


@router.delete("/{request_id}")
async def delete_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_admin_user)
):
    req = await db.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    await db.delete(req)
    await db.commit()
    return {"detail": "Заявка удалена"}

