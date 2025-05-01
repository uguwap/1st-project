import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from app.core.config import settings
from app.models.completed_request import CompletedRequest

# Словарь нормализации для обработки (гель, газ и тд)
TREATMENT_NORMALIZER = {
    "гель от дихлофоса 45": "гель",
    "гелем": "гель",
    "газ 2.0": "газ",
    "жидкость + капли": "жидкость",
    "аэрозольный": "аэрозоль",
    "порошок и ловушки": "приманки",
    "дымовая шашка": "дым",
    # дополню своими значениями из реальной практики
}



def normalize_treatment(value: str) -> str:
    if not value:
        return "неизвестно"
    value = value.lower().strip()
    return TREATMENT_NORMALIZER.get(value, value)



engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



async def export_dataset():
    async with async_session() as session:
        stmt = select(CompletedRequest)
        result = await session.execute(stmt)
        requests = result.scalars().all()

        data = [
            {
                "city": r.city,
                "insect_type": r.insect_type,
                "source": r.source,
                "treatment": normalize_treatment(r.treatment),
                "comment": r.comment,
                "price": r.price,
                "processed_day": r.processed_at.weekday(),  # 0 (понедельник) – 6 (воскресенье)
                "processed_hour": r.processed_at.hour        # 0–23
            }
            for r in requests
        ]

        df = pd.DataFrame(data)
        df.to_csv("ml/dataset/dataset.csv", index=False, encoding="utf-8")
        print("Датасет сохранён: ml/dataset/dataset.csv")



if __name__ == "__main__":
    asyncio.run(export_dataset())