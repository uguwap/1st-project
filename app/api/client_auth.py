import code

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime, timedelta

from app.models.client import Client
from app.database.session import get_db
from app.core.security import create_access_token

verification_codes = {} # пока временно тут коды, потом редис

router = APIRouter(prefix="/client", tags=["Клиенты"])

@router.post("/send-code")
async def send_verification_code(phone: str, db: AsyncSession = Depends(get_db)):
    if not phone.startswith("8") or len(phone) != 11 or not phone.isdigit():
        raise HTTPException(status_code=400, detail="Неверный формат номера")

    code = str(uuid4().int)[:4]
    verification_codes[phone] = {
        "code": code,
        "expires": datetime.now() + timedelta(minutes=5),
    }

    # TODO: Вызывать Celery-задачу для отправки через Telegram

    return {"message": "Код отправлен", "debug_code": code}



@router.post("verify-code")
async def verify_code(phone: str, code: str, db: AsyncSession = Depends(get_db)):
    data = verification_codes.get(phone)
    if not data or data["code"] != code or datetime.utcnow() > data["expires"]:
        raise HTTPException(status_code=400, detail= "Неверный или просроченный код")

    result = await db.execute(select(Client).where(Client.phone==phone))
    client = result.scalar_one_or_none()

    if not client:
        client = Client(phone=phone, name="Не указано")
        db.add(client)
        await db.commit()
        await db.refresh(client)

    token = create_access_token({"sub":str(client.id), "role": "client"})
    return {"access_token": token, "token_type": "bearer"}








