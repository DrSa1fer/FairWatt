import json
from pathlib import Path

from days.predict import predict as dp
from hours.predict import predict as hp
from months.predict import predict as mp, Data as md
from src.ml.months.train.train_model import train

class Hour():
    pass

def predict_by_hours(data : list[dict]) -> list[float]:
    pass

class Day(md):
    pass

def predict_by_days(data : list[dict]) -> list[float]:
    pass

class Month():
    pass

def predict_by_months(data : list[Day]) -> list[float]:
    return mp(data)
