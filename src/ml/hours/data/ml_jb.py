import joblib

def load_model():
    return joblib.load("model-bh.joblib")

def store_model(model):
    joblib.dump(model, "model-bh.joblib")

def load_scaler():
    return joblib.load("scaler-bh.joblib")
def store_scaler(model):
    joblib.dump(model, "scaler-bh.joblib")