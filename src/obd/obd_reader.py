import time
import threading
import obd
import os
import pandas as pd

from config import POLL_INTERVAL, TRAIN_DATA_PATH
from src.obd.obd_connection import create_connection
from src.obd.obd_logger import log_to_csv
from src.ai.feature_engineering import extract_features, rule_based_label
from src.ai.inference import predict_behavior
from src.ai.explainability import explain

latest_telemetry = {}
_lock = threading.Lock()

connection = create_connection()
supported = connection.supported_commands

AVAILABLE = {}
for cmd in supported:
    if cmd.name in ["RPM", "SPEED", "THROTTLE_POS", "COOLANT_TEMP"]:
        AVAILABLE[cmd.name] = cmd

previous_speed = 0
previous_throttle = 0
max_rpm_observed = 0


def append_training_data(features, label):
    os.makedirs("data", exist_ok=True)

    row = dict(zip(
        ["speed","rpm","throttle_pos","acceleration","delta_throttle"],
        features
    ))
    row["label"] = label

    df = pd.DataFrame([row])

    if not os.path.exists(TRAIN_DATA_PATH):
        df.to_csv(TRAIN_DATA_PATH, index=False)
    else:
        df.to_csv(TRAIN_DATA_PATH, mode='a', header=False, index=False)


def obd_loop():
    global previous_speed, previous_throttle, max_rpm_observed

    while True:
        temp = {}

        for name, cmd in AVAILABLE.items():
            try:
                response = connection.query(cmd)
                if not response.is_null():
                    temp[name.lower()] = response.value.magnitude
                else:
                    temp[name.lower()] = 0
            except:
                temp[name.lower()] = 0

        speed = temp.get("speed", 0)
        rpm = temp.get("rpm", 0)
        throttle = temp.get("throttle_pos", 0)

        features = extract_features(
            speed, rpm, throttle,
            previous_speed, previous_throttle,
            POLL_INTERVAL
        )

        # Track dynamic max RPM
        if rpm > max_rpm_observed:
            max_rpm_observed = rpm

        # Bootstrapping label (NOT prediction)
        initial_label = rule_based_label(features)

        # Save rule-based labeled data
        append_training_data(features, initial_label)

        # Predict using AI model
        label, confidence = predict_behavior(features)
        reasons = explain(features)

        temp.update({
            "driving_mode": label,
            "ai_confidence": confidence,
            "explanation": reasons,
            "max_rpm": max_rpm_observed
        })

        previous_speed = speed
        previous_throttle = throttle

        log_to_csv(temp)

        with _lock:
            latest_telemetry.update(temp)

        time.sleep(POLL_INTERVAL)


def start_obd_reader():
    threading.Thread(target=obd_loop, daemon=True).start()


def get_latest_telemetry():
    with _lock:
        return dict(latest_telemetry)
