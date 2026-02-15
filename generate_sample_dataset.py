import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

rows = []

def random_float(a, b):
    return round(random.uniform(a, b), 2)

# -------- SMOOTH --------
for _ in range(500):
    speed = random_float(0, 50)
    rpm = random_float(800, 1800)
    throttle = random_float(5, 25)
    acceleration = random_float(-2, 2)
    delta_throttle = random_float(-3, 3)

    rows.append([speed, rpm, throttle, acceleration, delta_throttle, "Smooth"])

# -------- NORMAL --------
for _ in range(500):
    speed = random_float(20, 80)
    rpm = random_float(1500, 3000)
    throttle = random_float(20, 50)
    acceleration = random_float(-5, 5)
    delta_throttle = random_float(-5, 5)

    rows.append([speed, rpm, throttle, acceleration, delta_throttle, "Normal"])

# -------- AGGRESSIVE --------
for _ in range(500):
    speed = random_float(40, 120)
    rpm = random_float(3000, 5000)
    throttle = random_float(50, 85)
    acceleration = random_float(5, 12)
    delta_throttle = random_float(5, 15)

    rows.append([speed, rpm, throttle, acceleration, delta_throttle, "Aggressive"])

# -------- RASH --------
for _ in range(500):
    speed = random_float(30, 130)
    rpm = random_float(3500, 6000)
    throttle = random_float(60, 100)
    acceleration = random_float(12, 25)
    delta_throttle = random_float(15, 40)

    rows.append([speed, rpm, throttle, acceleration, delta_throttle, "Rash"])

df = pd.DataFrame(rows, columns=[
    "speed",
    "rpm",
    "throttle_pos",
    "acceleration",
    "delta_throttle",
    "label"
])

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("data/training_data.csv", index=False)

print("Balanced training dataset created with", len(df), "samples")
