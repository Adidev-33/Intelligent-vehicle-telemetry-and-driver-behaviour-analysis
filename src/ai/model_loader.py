import joblib
import torch
from src.ai.lstm_model import DrivingLSTM

ml_model = joblib.load("src/ai/driver_ml_model.pkl")

lstm_model = DrivingLSTM()
lstm_model.load_state_dict(torch.load("src/ai/lstm_model.pt", map_location="cpu"))
lstm_model.eval()
