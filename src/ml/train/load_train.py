import joblib

def load_model_train():
    return joblib.load("model.joblib")

def load_scaler_train():
    return joblib.load("scaler.joblib")
