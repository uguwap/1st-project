from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.request import RequestCreate, RequestRead, RequestUpdate, Request
from app.database.session import AsyncSessionLocal
from typing import Optional
from sqlalchemy import select, and_, cast, String, func
from app.models.client import Client
from app.core.dependencies import get_admin_user
from app.tasks.reminderclient import send_feedback_reminder
from datetime import timedelta, datetime
router = APIRouter(prefix="/requests", tags=["Заявки"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=RequestRead)
async def create_request(data: RequestCreate, db: AsyncSession = Depends(get_db)):
    new_request = Request(**data.dict())
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request

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
        filters.append(func.lower(Request.insect_type).like(f"%{insect_type}%"))
    if source:
        filters.append(func.lower(Request.source).like(f"%{source}%"))

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{request_id}", response_model=RequestRead)
async def get_request(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(Request, request_id)
    if not result:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return result

@router.patch("/{request_id}", response_model=RequestRead)
async def update_request(
        request_id: int,
        data: RequestUpdate,
        db: AsyncSession = Depends(get_db)
):

    req = await db.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    old_status = req.status

    for field, value in data.dict(exclude_unset=True).items():
        setattr(req, field, value)

    if data.status == "Завершено" and old_status != "Завершено":
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

    if data.status == "Завершено" and old_status != "Завершено":
        # Планируем задачу через 10 дней
        eta = datetime.utcnow() + timedelta(days=10)
        send_feedback_reminder.apply_async((req.phone,), eta=eta)

    return req

@router.delete("/{request_id}")
async def delete_request(request_id: int, db: AsyncSession = Depends(get_db), _ = Depends(get_admin_user)):
    req = await db.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    await db.delete(req)
    await db.commit()
    return {"detail": "Заявка удалена"}

