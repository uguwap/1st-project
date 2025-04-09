import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import user, request, client, reminder

import asyncio
from app.database.session import engine
from app.database.database import BaseMeta

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseMeta.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())