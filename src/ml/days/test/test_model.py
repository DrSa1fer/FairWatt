import json

import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline

from ..data.ml_jb import load_model
from ..data.ml_jb import load_scaler

from ..features.build_features import build_features

def _test_dataset() -> (np.array, pd.DataFrame):
    with open(Path("../data/test/raw_test.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

def test():
    X, y = _test_dataset()

    scaler = load_scaler()
    model = load_model()

    pipeline = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    y_pred = pipeline.predict(X)

    print("MSE:", mean_squared_error(y, y_pred))
    print("MAR:", mean_absolute_error(y, y_pred))
    print("R^2:", r2_score(y, y_pred))
