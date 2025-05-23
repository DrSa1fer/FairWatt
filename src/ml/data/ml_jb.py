import joblib

def load_model_train():
    return joblib.load("model.joblib")

def load_scaler_train():
    return joblib.load("scaler.joblib")

def store_model_train(model):
    joblib.dump(model, "model.joblib")

def store_scaler_train(model):
    joblib.dump(model, "scaler.joblib")
