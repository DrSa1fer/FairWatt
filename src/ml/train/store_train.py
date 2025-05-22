import joblib

def store_model_train(model):
    joblib.dump(model, "model.joblib")

def store_scaler_train(model):
    joblib.dump(model, "scaler.joblib")
