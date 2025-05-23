import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.ml.months.data.ml_jb import store_model
from src.ml.months.data.ml_jb import store_scaler
from src.ml.months.features.build_features import build_features


def _load_dataset() -> (np.array, pd.DataFrame):
    with open(Path("data/train/rate_train.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

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
