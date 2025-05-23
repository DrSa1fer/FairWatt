from sklearn.pipeline import Pipeline

from .data.ml_jb import load_model
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
