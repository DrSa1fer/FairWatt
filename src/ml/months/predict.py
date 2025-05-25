import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

from .data.ml_jb import load_model
from .data.ml_jb import load_scaler

class Data(BaseModel):
    buildingType    : int
    residentsCount  : int | None
    roomsCount      : int | None
    totalArea       : float | None
    consumption     : dict[str, float | None]

def _build_features(data: list[Data]) -> np.array:
    result = dict()

    result["buildingType"] = [
        0 if d.buildingType == "Частный" else
        1 if d.buildingType == "Прочий" else
        2 for d in data
    ]

    result["residentsCount"]     = [d.residentsCount for d in data]
    result["residentsCount_has"] = [d.residentsCount is not None for d in data]

    result["roomsCount"]         = [d.roomsCount for d in data]
    result["roomsCount_has"]     = [d.roomsCount is not None for d in data]

    result["totalArea"]          = [d.totalArea for d in data]
    result["totalArea_has"]      = [d.totalArea is not None for d in data]

    for i in range(0, 12):
        result[f"consumption_{i+1}"]     = [d.consumption.get(i, 0) for d in data]
        result[f"consumption_{i+1}_has"] = [d.consumption.get(i, None) is not None for d in data]

    return pd.DataFrame(result).to_numpy()

def predict(data : list[Data]) -> list[float]:
    return Pipeline(steps =[
        ("preprocessor", load_scaler()),
        ("regressor", load_model())
    ]).predict(_build_features(data))
