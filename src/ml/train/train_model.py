import json
import pandas as pd

from pathlib import Path
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from ..data.ml_jb import load_model_train
from ..data.ml_jb import load_scaler_train
from ..data.ml_jb import store_model_train
from ..data.ml_jb import store_scaler_train

from ..features.build_features import build_features

def _train_dataset() -> pd.DataFrame:
    with open(Path("../data/train/dataset_train.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

def train() -> None:
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

    X, y = _train_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=37)

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("MSE:", mean_squared_error(y_test, y_pred))
    print("MAR:", mean_absolute_error(y_test, y_pred))
    print("R^2:", r2_score(y_test, y_pred))

    store_scaler_train(scaler)
    store_model_train(model)
