from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID
from datetime import datetime, timedelta

from app.database.session import get_db
from app.models.request import Request, RequestCreate, RequestRead, RequestUpdate
from app.models.completed_request import CompletedRequest
from app.models.reminder import Reminder
from app.models.reminder_archive import ReminderArchive
from app.models.user import User
from app.tasks.send_reminder_task import send_reminder
from app.api.auth import get_current_user
from ml.predict_comment import predict_comment
from app.kafka.producer import send_request_completed_event
router = APIRouter(prefix="/requests", tags=["Заявки"])


@router.post("", response_model=RequestRead)
async def create_request(
    request_data: RequestCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    data = request_data.dict(exclude={"status", "comment"})

    comment = predict_comment(
        insect_type=data["insect_type"],
        treatment=data["treatment"],
        city=data["city"],
        source=data["source"]
    )

    new_request = Request(
        **data,
        comment=comment,
        user_id=user.id,
        created_at=datetime.utcnow(),
        status=False
    )

    session.add(new_request)
    await session.commit()
    await session.refresh(new_request)

    return new_request



@router.get("/{request_id}", response_model=RequestRead)
async def get_request(
    request_id: UUID,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    request = await session.get(Request, request_id)
    if not request or request.user_id != user.id:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request


@router.patch("/{request_id}", response_model=RequestRead)
async def update_request(
    request_id: UUID,
    request_data: RequestUpdate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_request = await session.get(Request, request_id)
    if not db_request or db_request.user_id != user.id:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    update_fields = request_data.dict(exclude_unset=True)
    old_status = db_request.status

    for key, value in update_fields.items():
        setattr(db_request, key, value)

    await session.commit()
    await session.refresh(db_request)

    if update_fields.get("status") is True and old_status is False:

        archived = CompletedRequest(
            city=db_request.city,
            processed_at=db_request.processed_at,
            client_phone=db_request.client_phone,
            insect_type=db_request.insect_type,
            treatment=db_request.treatment,
            source=db_request.source,
            address=db_request.address,
            comment=db_request.comment,
            price=db_request.price,
            created_at=datetime.utcnow(),
            original_request_id=db_request.id
        )
        session.add(archived)
        await session.commit()

        remind_at = datetime.utcnow() + timedelta(days=10)
        new_reminder = Reminder(
            request_id=db_request.id,
            remind_at=remind_at
        )
        session.add(new_reminder)
        await session.commit()

        send_reminder.delay(str(new_reminder.id))
        send_request_completed_event(db_request, executor=user)

    return db_request
