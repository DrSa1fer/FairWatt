import joblib

def load_model():
    return joblib.load("model-bd.joblib")
def store_model(model):
    joblib.dump(model, "model-bd.joblib")
def load_scaler():
    return joblib.load("scaler-bd.joblib")
def store_scaler(model):
    joblib.dump(model, "scaler-bd.joblib")
