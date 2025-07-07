# Real‑time Stock Price Anomaly Detector

**What it does:**
Continuously monitors intraday stock prices (5-minute bars) for unusual spikes or drops (greater than 2σ from a 20-period rolling mean) and sends email alerts when anomalies are detected.

---

## Quickstart

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/stock-anomaly-detector.git
   cd stock-anomaly-detector
   ```

2. Set up the Python environment

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1    # Windows PowerShell
   pip install -r requirements.txt
   ```

3. Configure environment variables

   Create or update the `.env` file in the project root with the following entries:

   ```text
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your.email@gmail.com
   EMAIL_PASS=yourAppPasswordHere
   RECEIVER_EMAIL=recipient@example.com
   ```

4. Run the real-time monitor

   ```bash
   python .\src\run_monitor.py
   ```

---

## Architecture

```
src/
├── common.py       # Shared types (AnomalyEvent)
├── data_client.py  # Yahoo Finance ingestion via yfinance
├── detector.py     # Rolling-statistics anomaly detection
├── alerter.py      # SMTP email alert implementation
└── run_monitor.py  # Orchestration loop for polling and alerts
```

---

## Why Rolling Statistics?

This project uses a rolling mean and standard deviation approach (±2σ) to detect anomalies. This method is highly interpretable, fast, and reliable for real-time price monitoring.

While more complex models like LSTM-based autoencoders can be used for detecting non-linear or hidden patterns in time series data, they require more data, training time, and tuning. For real-time anomaly detection in intraday stock prices, rolling statistics strike a strong balance between simplicity, speed, and accuracy.

Future enhancements may explore deep learning–based models for prediction or anomaly detection, if required by use case.

---

## Email Alerts

- Sends one email per symbol per polling interval if anomalies are detected.
- Subject uses the format `[ALERT] <SYMBOL> anomalies detected`.
- Body lists timestamps, prices, and deviation values.

---

## Tests

Run unit tests to verify data fetching and anomaly detection logic:

```bash
pytest -q
```

---

## Configuration Options

Modify the following settings in `src/run_monitor.py`:

- `SYMBOLS`: list of ticker symbols to monitor.
- `WINDOW`: rolling window size for computing mean and standard deviation.
- `SIGMA_THRESH`: number of standard deviations for flagging anomalies.
- `INTERVAL`: polling interval (e.g., "5m").

---

## Two Detection Approaches

This project supports two independent anomaly-detection strategies:

1. **Statistical Approach (Rolling Mean + Std Dev)**  
   Flags a price as an anomaly when the absolute deviation from the rolling mean exceeds the configured sigma threshold.

2. **LSTM Autoencoder (AI/ML Approach)**  
   Uses a trained LSTM autoencoder to learn normal price sequence patterns and flags anomalies based on high reconstruction error. Enable this mode by setting `USE_LSTM = True` in `src/run_monitor.py`.

---

## Customization

- To add other alert channels, extend or modify the `alerter.py` module.
- To adjust data frequency or source, update `data_client.py` accordingly.
