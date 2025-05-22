import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from ..train.load_train import load_scaler_train, load_model_train
from ..train.store_train import store_scaler_train, store_model_train


def train(X : pd.DataFrame, y : pd.DataFrame):
    scaler = StandardScaler()
    model = RandomForestRegressor(n_estimators=10, max_depth=25)

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

def retrain(X : pd.DataFrame, y : pd.DataFrame):
    scaler = load_scaler_train()
    model = load_model_train()

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