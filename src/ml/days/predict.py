import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

from .data.ml_jb import load_model
from .data.ml_jb import load_scaler

class Data(BaseModel):
    residentsCount  : int | None
    roomsCount      : int | None
    totalArea       : float | None
    consumption     : list[float | None]

def _build_features(data: list[Data]) -> np.array:
    result = dict()

    result["Residents"] = [d.residentsCount for d in data]
    result["Residents_has"] = [d.residentsCount is not None for d in data]

    result["Rooms"] = [d.roomsCount for d in data]
    result["Rooms_has"] = [d.roomsCount is not None for d in data]

    result["Square"] = [d.totalArea for d in data]
    result["Square_has"] = [d.totalArea is not None for d in data]

    for i in range(0, 24):
        result[f"consumption_{i+1}"]      = [d.consumption[i] for d in data]
        result[f"consumption_{i+1}_has"]  = [d.consumption[i] is not None for d in data]

    return pd.DataFrame(result).to_numpy()

def predict(data : list[Data]) -> list[float]:
    return Pipeline(steps =[
        ("preprocessor", load_scaler()),
        ("regressor", load_model())
    ]).predict(_build_features(data))

