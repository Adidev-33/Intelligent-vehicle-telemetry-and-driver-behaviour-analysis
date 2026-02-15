import threading
import time
import pandas as pd
import joblib
import os

from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from config import TRAIN_DATA_PATH

MODEL_DIR = "src/ai/models"
MODEL_PATH = os.path.join(MODEL_DIR, "driver_ml_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

ALL_CLASSES = ["Smooth", "Normal", "Aggressive", "Rash"]

_model_lock = threading.Lock()

online_model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", SGDClassifier(
        loss="log_loss",
        class_weight="balanced",
        max_iter=1000,
        tol=1e-3
    ))
])

def load_model():
    global online_model

    if os.path.exists(MODEL_PATH):
        online_model = joblib.load(MODEL_PATH)
        print("[AI] Loaded existing model.")
    else:
        print("[AI] No saved model. Waiting for training data.")

def training_loop():
    global online_model

    while True:
        try:
            if not os.path.exists(TRAIN_DATA_PATH):
                time.sleep(10)
                continue

            df = pd.read_csv(TRAIN_DATA_PATH)

            if len(df) < 100:
                time.sleep(10)
                continue

            X = df[[
                "speed",
                "rpm",
                "throttle_pos",
                "acceleration",
                "delta_throttle"
            ]]

            y = df["label"]

            with _model_lock:
                online_model.fit(X, y)
                joblib.dump(online_model, MODEL_PATH)

            print("[AI] Model trained safely with", len(df), "samples")

        except Exception as e:
            print("[AI] Training error:", e)

        time.sleep(60)

def start_online_training():
    load_model()
    threading.Thread(target=training_loop, daemon=True).start()
