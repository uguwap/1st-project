from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.models.user import User, UserCreate, UserLogin, UserRead, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_db, get_current_user
router = APIRouter(prefix="/auth", tags=["Аутентификация"]) # админский вход


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


@router.post("/login", response_model=TokenResponse)

async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Неверные данные")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные данные")

    token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user # Для получения текущего пользователя, пока оставлю так.
    # Чтобы какая у него роль





