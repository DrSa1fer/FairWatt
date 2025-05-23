from sklearn.pipeline import Pipeline

from .data.ml_jb import load_model, store_model, store_scaler
from .data.ml_jb import load_scaler
from .features.build_features import build_features


def predict(data : list) -> list[float]:
    X, _ = build_features(data)

    scaler = load_scaler()
    model = load_model()

    pipeline = Pipeline(steps =[
        ("preprocessor", scaler),
        ("regressor", model)
    ])

    return pipeline.predict(X)
