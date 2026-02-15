import csv
import os
from datetime import datetime
from config import CSV_LOG_PATH

os.makedirs("data/raw", exist_ok=True)

def log_to_csv(data):
    file_exists = os.path.isfile(CSV_LOG_PATH)

    with open(CSV_LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp"] + list(data.keys()))
        if not file_exists:
            writer.writeheader()
        row = {"timestamp": datetime.now().isoformat()}
        row.update(data)
        writer.writerow(row)
