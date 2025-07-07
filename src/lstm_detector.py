import os
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from detector import AnomalyEvent

class LSTMDetector:
    def __init__(self,
                 model_path: str = "../model/lstm_model.h5",
                 scaler_path: str = "../model/scaler.npy",
                 threshold_path: str = "../model/threshold.npy",
                 window: int = 20):
        # Load trained model
        # self.model = load_model(model_path)
        self.model = load_model(model_path, compile=False)
        # Load scaler and threshold
        scale_ = np.load(scaler_path)
        self.scaler = MinMaxScaler()
        self.scaler.scale_ = scale_
        self.threshold = float(np.load(threshold_path))
        self.window = window

    def detect(self, symbol: str, df: pd.DataFrame) -> list:
        """
        Fetch latest data for 'symbol', build sequences,
        compute reconstruction MSE, and flag anomalies.
        """
        # 1. Get the 'close' column and scale
        prices = df["close"].values.reshape(-1,1)
        scaled = self.scaler.transform(prices)

        # 2. Build sequences
        seqs = []
        for i in range(len(scaled) - self.window):
            seqs.append(scaled[i:i+self.window])
        X = np.array(seqs)

        if len(X) == 0:
            return []

        # 3. Reconstruct and compute MSE per sequence
        X_pred = self.model.predict(X, verbose=0)
        mse = np.mean(np.power(X_pred - X, 2), axis=(1,2))

        # 4. Any sequences with mse > threshold are anomalies
        events = []
        times = df["datetime"].iloc[self.window:].tolist()
        for t, e in zip(times, mse):
            if e > self.threshold:
                price = df.loc[df["datetime"] == t, "close"].values[0]
                deviation = (e - np.mean(mse)) / np.std(mse)
                events.append(AnomalyEvent(symbol, t, price, deviation))
        return events
