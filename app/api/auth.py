from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.database.session import AsyncSessionLocal


router = APIRouter(prefix="/auth", tags=["Аутентификация"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_exists = await db.execute(select(User).where(User.username == data.username))
    if user_exists.scalar():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        is_admin=data.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.username == data.username))
    user = query.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные данные")

    token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}



