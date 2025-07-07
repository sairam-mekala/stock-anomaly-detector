import os
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

# 1. Parameters
SYMBOL = "AAPL"
START = "2025-06-01"
END   = "2025-07-01"
INTERVAL = "5m"
WINDOW = 20               # sequence length for LSTM
BATCH_SIZE = 32
EPOCHS = 20
MODEL_PATH = "../model/lstm_model.h5"
SCALER_PATH = "../model/scaler.npy"
THRESH_PATH = "../model/threshold.npy"

# 2. Fetch data
df = yf.download(SYMBOL, start=START, end=END, interval=INTERVAL, progress=False)
df = df["Close"].dropna().values.reshape(-1, 1)

# 3. Scale data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df)

# 4. Create sequences
def create_sequences(data, window):
    seqs = []
    for i in range(len(data) - window):
        seqs.append(data[i:i+window])
    return np.array(seqs)

X = create_sequences(data_scaled, WINDOW)

# 5. Build LSTM autoencoder
inputs = Input(shape=(WINDOW, 1))
encoded = LSTM(64, activation="relu")(inputs)
decoded = RepeatVector(WINDOW)(encoded)
decoded = LSTM(64, activation="relu", return_sequences=True)(decoded)
decoded = TimeDistributed(Dense(1))(decoded)
model = Model(inputs, decoded)
model.compile(optimizer="adam", loss="mse")

# 6. Train
es = EarlyStopping(monitor="loss", patience=3, restore_best_weights=True)
model.fit(X, X, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[es], verbose=1)

# 7. Compute reconstruction error on training set
X_pred = model.predict(X)
mse = np.mean(np.power(X_pred - X, 2), axis=(1,2))
# threshold = mean + 3*std
threshold = np.mean(mse) + 3 * np.std(mse)

# 8. Save model, scaler, threshold
os.makedirs("../model", exist_ok=True)
model.save(MODEL_PATH)
np.save(SCALER_PATH, scaler.scale_)
np.save(THRESH_PATH, threshold)

print(f"Model saved to {MODEL_PATH}")
print(f"Threshold: {threshold:.6f}")
