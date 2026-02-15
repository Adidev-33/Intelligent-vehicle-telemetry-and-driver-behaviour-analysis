# Intelligent Vehicle Telemetry & AI Driving Analysis System

A real-time AI-powered Vehicle Telemetry Analysis (VTA) system built for
Raspberry Pi using OBD-II data.

This system: - Streams live vehicle telemetry - Classifies driving
behavior using Machine Learning - Trains online while running - Provides
AI confidence scores - Explains driving classification decisions -
Automatically detects supported OBD commands - Dynamically adjusts RPM
scale - Runs on Raspberry Pi

------------------------------------------------------------------------

# Features

## Real-Time Telemetry

-   Speed
-   RPM
-   Throttle Position
-   Engine Temperature
-   Live Graphs (Chart.js)
-   Dynamic RPM scaling

## AI-Based Driving Classification

Driving Modes: - Smooth - Normal - Aggressive - Rash

## Online Machine Learning

-   Uses SGDClassifier
-   Feature scaling via StandardScaler
-   Incremental retraining every 60 seconds
-   Automatically improves with more data

## Explainable AI

Displays why a driving mode was chosen: - High RPM usage - Sudden
acceleration - Rapid throttle input - Stable driving parameters

## Raspberry Pi Optimized

-   Lightweight ML model
-   No GPU required
-   Minimal CPU usage

------------------------------------------------------------------------

## Project Structure

```
VTA/
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # SSE API for live telemetry stream
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   │
│   │   ├── models/                # Saved ML models (ignored in git)
│   │   │   └── driver_ml_model.pkl
│   │   │
│   │   ├── feature_engineering.py # Feature extraction logic
│   │   ├── explainability.py      # AI explanation logic
│   │   ├── inference.py           # Real-time prediction
│   │   └── online_trainer.py      # Online ML training pipeline
│   │
│   ├── obd/
│   │   ├── __init__.py
│   │   ├── obd_connection.py      # Bluetooth OBD connection
│   │   ├── obd_logger.py          # CSV logging
│   │   └── obd_reader.py          # Telemetry loop + AI integration
│   │
│   └── main.py                    # Flask app entry point
│
├── static/
│   ├── css/
│   │   └── style.css              # Dashboard styling
│   │
│   └── js/
│       └── dashboard.js           # Live dashboard logic (Chart.js)
│
├── templates/
│   ├── index.html                 # Landing page
│   ├── dashboard.html             # Live telemetry dashboard
│   └── about.html                 # About page
│
├── data/
│   ├── raw/
│   │   └── obd_log.csv            # Raw telemetry logs (auto-generated)
│   │
│   └── training_data.csv          # AI training dataset
│
├── config.py                      # Global configuration
├── requirements.txt               # Python dependencies
├── generate_sample_dataset.py     # Synthetic dataset generator
├── .gitignore                     # Git ignored files
└── README.md                      # Project documentation
```

#  Installation (Raspberry Pi)

## 1 Install dependencies

sudo apt update sudo apt install python3-pip python3-venv bluetooth

## 2 Setup project
```
git clone `<your-repo>`{=html} cd VTA python3 -m venv venv source
venv/bin/activate pip install -r requirements.txt
```

## 3 Pair OBD Device
```
bluetoothctl scan on pair XX:XX:XX:XX:XX trust XX:XX:XX:XX:XX quit (Only once)

Bind device: sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX
```
## 4 Run Application
```
python -m src.main
```
Open browser: http://`<raspberry-pi-ip>`{=html}:5000
------------------------------------------------------------------------

# Sample Dataset Generation

If real driving data cannot be collected:
```
python generate_sample_dataset.py
```
Then delete old model
```
rm src/ai/models/driver_ml_model.pkl
```
Restart app.

------------------------------------------------------------------------

# Future Improvements

-   Replace SGD with RandomForest
-   Add LSTM time-series prediction
-   Add driver risk score (0--100 scale)
-   Add confusion matrix dashboard
-   Add model drift detection
-   Add performance analytics page
-   Add cloud sync support
-   Add multi-driver comparison