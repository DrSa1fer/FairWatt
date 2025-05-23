import json
import pandas as pd

from pathlib import Path
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline

from ..data.ml_jb import load_model_train
from ..data.ml_jb import load_scaler_train

from ..features.build_features import build_features

def _test_dataset() -> pd.DataFrame:
    with open(Path("../data/test/dataset_test.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

def test():
    X, y = _test_dataset()

    scaler = load_scaler_train()
    model = load_model_train()

    pipeline = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    y_pred = pipeline.predict(X)

    print("MSE:", mean_squared_error(y, y_pred))
    print("MAR:", mean_absolute_error(y, y_pred))
    print("R^2:", r2_score(y, y_pred))
