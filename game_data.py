import pandas as pd

data_ai = pd.read_csv("game_data.csv")
print(data_ai.head())
print(data_ai.describe())

data_ai = data_ai.drop_duplicates()
print(data_ai.describe())