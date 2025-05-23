import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.ml.hours.data.ml_jb import load_scaler, load_model
from src.ml.months.data.ml_jb import store_model_train_by_hours
from src.ml.months.data.ml_jb import store_scaler_train_by_hours
from src.ml.months.features.build_features import build_days_features
from src.ml.months.features.build_features import build_features


def _hours_dataset() -> (np.array, pd.DataFrame):
    with open(Path("data/train/rate_train.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

def train_by_hours() -> None:
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

    X, y = _days_dataset()

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X, y)

    store_scaler_train_by_hours(scaler)
    store_model_train_by_hours(model)


def _days_dataset() -> (np.array, pd.DataFrame):
    with open(Path("data/train/rate_train.json"), "r") as f:
        data = json.load(f)

    return build_days_features(data)

def train_by_days() -> None:
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

    X, y = _days_dataset()

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X, y)

    store_scaler_train_by_hours(scaler)
    store_model_train_by_hours(model)

def _months_dataset() -> (np.array, pd.DataFrame):
    with open(Path("data/train/rate_train.json"), "r") as f:
        data = json.load(f)

    return build_features(data)

def train_by_months() -> None:
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

    X, y = _months_dataset()

    model = Pipeline(steps=[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    model.fit(X, y)

    store_scaler_train_by_hours(scaler)
    store_model_train_by_hours(model)



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
