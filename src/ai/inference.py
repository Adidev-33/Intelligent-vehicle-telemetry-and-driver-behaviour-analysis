import numpy as np
import pandas as pd
from src.ai.online_trainer import online_model, _model_lock

FEATURE_COLUMNS = [
    "speed",
    "rpm",
    "throttle_pos",
    "acceleration",
    "delta_throttle"
]

def predict_behavior(features):
    with _model_lock:
        try:
            X = pd.DataFrame([features], columns=FEATURE_COLUMNS)

            proba = online_model.predict_proba(X)[0]
            idx = np.argmax(proba)
            label = online_model.classes_[idx]
            confidence = round(float(max(proba)) * 100, 2)

        except:
            label = "Normal"
            confidence = 0.0

    return label, confidence
