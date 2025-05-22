import pandas as pd
from sklearn.pipeline import Pipeline

from ..train.load_train import load_model_train
from ..train.load_train import load_scaler_train


def predict(data : pd.DataFrame) -> list[float]:
    scaler = load_scaler_train()
    model = load_model_train()

    pipeline = Pipeline(steps =[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    return pipeline.predict(data)