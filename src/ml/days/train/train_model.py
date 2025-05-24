import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ..data.ml_jb import load_model
from ..data.ml_jb import store_model, load_scaler
from ..data.ml_jb import store_scaler
from ..features.build_features2 import build_features2


def _load_dataset() -> (np.array, pd.DataFrame):
    with open(Path("days/data/raw_data_iot.json"), "r") as f:
        data = json.load(f)

    return build_features2(data)

def train() -> None:
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

    X, y = _load_dataset()

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X, y)

    store_scaler(scaler)
    store_model(model)


def retrain() -> None:
    scaler = load_scaler()
    model = load_model()

    X, y = _load_dataset()

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X, y)

    store_scaler(scaler)
    store_model(model)
