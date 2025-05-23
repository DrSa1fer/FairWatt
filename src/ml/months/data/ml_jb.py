from pathlib import Path

import joblib

def load_model():
    return joblib.load(Path("model-bm.joblib"))

def store_model(model):
    joblib.dump(model, Path("model-bm.joblib"))


def load_scaler():
    return joblib.load(Path("scaler-bm.joblib"))

def store_scaler(model):
    joblib.dump(model, Path("scaler-bm.joblib"))
