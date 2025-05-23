import json
from pathlib import Path

from days.predict import predict as dp
from hours.predict import predict as hp
from months.predict import predict as mp, Data as md
from src.ml.months.train.train_model import train

class Hour():
    pass

def predict_by_hours(data : list[dict]) -> list[float]:
    return hp(data)

class Day(md):
    pass

def predict_by_days(data : list[dict]) -> list[float]:
    return dp(data)

class Month():
    pass

def predict_by_months(data : list[Day]) -> list[float]:
    return mp(data)


train()

with open(Path("months/data/train/raw_train.json"), "r") as f:
    data = json.load(f)[:10:]

days = [
    Day(residentsCount=2, totalArea=100, roomsCount=10, consumption=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
    Day(residentsCount=2, totalArea=100, roomsCount=10, consumption=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
]
print(predict_by_months(days))