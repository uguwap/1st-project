import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle


df = pd.read_csv("ml/dataset/dataset.csv", encoding="utf-8")


df = df.dropna(subset=["comment"])


X = df[["insect_type", "treatment", "city", "source"]]
y = df["comment"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["insect_type", "treatment", "city", "source"]),
    ]
)


model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=200))
])


model.fit(X_train, y_train)


with open("ml/training/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Модель обучена и сохранена: ml/training/model.pkl")
