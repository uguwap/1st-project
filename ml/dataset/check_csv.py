import pandas as pd

df = pd.read_csv("ml/dataset/dataset.csv")
print("Датасет загружен:")
print(df.head(10))
print("Столбцы:", df.columns.tolist())
print("Кол-во строк:", len(df))

