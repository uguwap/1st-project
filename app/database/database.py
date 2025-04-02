from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



DB_HOST = "192.168.0.100"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

async_db = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sync_dp = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(async_db)

async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

class BaseMeta(DeclarativeBase):
    pass



