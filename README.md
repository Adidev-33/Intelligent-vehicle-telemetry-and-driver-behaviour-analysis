# ?? Intelligent Vehicle Telemetry & AI Driving Analysis System

A real-time AI-powered Vehicle Telemetry Analysis (VTA) system built for
Raspberry Pi using OBD-II data.

This system: - Streams live vehicle telemetry - Classifies driving
behavior using Machine Learning - Trains online while running - Provides
AI confidence scores - Explains driving classification decisions -
Automatically detects supported OBD commands - Dynamically adjusts RPM
scale - Runs on Raspberry Pi

------------------------------------------------------------------------

# ?? Features

## ?? Real-Time Telemetry

-   Speed
-   RPM
-   Throttle Position
-   Engine Temperature
-   Live Graphs (Chart.js)
-   Dynamic RPM scaling

## ?? AI-Based Driving Classification

Driving Modes: - Smooth - Normal - Aggressive - Rash

## ?? Online Machine Learning

-   Uses SGDClassifier
-   Feature scaling via StandardScaler
-   Incremental retraining every 60 seconds
-   Automatically improves with more data

## ?? Explainable AI

Displays why a driving mode was chosen: - High RPM usage - Sudden
acceleration - Rapid throttle input - Stable driving parameters

## ?? Raspberry Pi Optimized

-   Lightweight ML model
-   No GPU required
-   Minimal CPU usage

------------------------------------------------------------------------

# ?? Project Architecture

VTA/ ¦ +-- src/ ¦ +-- api/ ? Flask API (SSE stream) ¦ +-- ai/ ? ML
pipeline ¦ ¦ +-- models/ ? Saved models ¦ ¦ +-- inference.py ¦ ¦ +--
online_trainer.py ¦ ¦ +-- explainability.py ¦ ¦ +--
feature_engineering.py ¦ ¦ ¦ +-- obd/ ? OBD connection & logging ¦ +--
main.py ? Application entry point ¦ +-- static/ ? CSS & JS +--
templates/ ? HTML pages +-- data/ ? Raw + training data +-- config.py
+-- requirements.txt

------------------------------------------------------------------------

# ?? Installation (Raspberry Pi)

## 1?? Install dependencies

sudo apt update sudo apt install python3-pip python3-venv bluetooth

## 2?? Setup project

git clone `<your-repo>`{=html} cd VTA python3 -m venv venv source
venv/bin/activate pip install -r requirements.txt

## 3?? Pair OBD Device

bluetoothctl scan on pair XX:XX:XX:XX:XX trust XX:XX:XX:XX:XX quit

Bind device: sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX

## 4?? Run Application

python -m src.main

Open browser: http://`<raspberry-pi-ip>`{=html}:5000

------------------------------------------------------------------------

# ?? Sample Dataset Generation

If real driving data cannot be collected:

python generate_sample_dataset.py

Then delete old model: rm src/ai/models/driver_ml_model.pkl

Restart app.

------------------------------------------------------------------------

# ?? Future Improvements

-   Replace SGD with RandomForest
-   Add LSTM time-series prediction
-   Add driver risk score (0--100 scale)
-   Add confusion matrix dashboard
-   Add model drift detection
-   Add performance analytics page
-   Add cloud sync support
-   Add multi-driver comparison

------------------------------------------------------------------------

# ? Disclaimer

This is a research/demo system. Not intended for safety-critical
automotive control.

------------------------------------------------------------------------

# ????? Author

Intelligent Vehicle Telemetry System\
Built using Flask + OBD + Machine Learning\
Optimized for Raspberry Pi
