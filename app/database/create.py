import asyncio
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.database.database import BaseMeta

async def add_sample():
    async with AsyncSessionLocal() as session:
        user = User(username="admin", hashed_password="hashed", is_admin=True)
        session.add(user)
        await session.commit()

asyncio.run(add_sample())