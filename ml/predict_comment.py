import pickle
import pandas as pd
from pathlib import Path
from typing import Literal

MODEL_PATH = Path("ml/training/model.pkl")
if not MODEL_PATH.exists():
    raise FileNotFoundError("Модель не найдена. Обучите её сначала.")


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_comment(
    insect_type: str,
    treatment: str,
    city: str,
    source: str
) -> str:
    """
    Возвращает ориентировочный комментарий на основе полей заявки
    """
    df = pd.DataFrame([{
        "insect_type": insect_type,
        "treatment": treatment,
        "city": city,
        "source": source
    }])
    prediction = model.predict(df)
    return prediction[0]