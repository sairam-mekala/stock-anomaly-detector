import pandas as pd
from typing import List

class AnomalyEvent:
    def __init__(self, symbol: str, timestamp: pd.Timestamp, price: float, deviation: float):
        self.symbol = symbol
        self.timestamp = timestamp
        self.price = price
        self.deviation = deviation  # number of sigma away from rolling mean

    def __repr__(self):
        return (f"AnomalyEvent(symbol={self.symbol}, timestamp={self.timestamp}, "
                f"price={self.price}, deviation={self.deviation:.2f}σ)")

class AnomalyDetector:
    def __init__(self, window: int = 20, sigma_thresh: float = 2.0):
        """
        window: rolling window size (number of bars)
        sigma_thresh: threshold in standard deviations to flag anomaly
        """
        self.window = window
        self.sigma_thresh = sigma_thresh

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure df has no missing values, sorted by datetime, and compute:
         - rolling mean of 'close'
         - rolling std of 'close'
         - deviation = (close - mean) / std
        """
        # 1. Drop rows with any NaNs
        df = df.dropna(subset=["datetime", "close"])

        # 2. Sort by datetime
        df = df.sort_values("datetime").reset_index(drop=True)

        # 3. Compute rolling stats on 'close'
        df["rolling_mean"] = df["close"].rolling(window=self.window).mean()
        df["rolling_std"] = df["close"].rolling(window=self.window).std()

        # 4. Compute number of sigma deviations
        df["deviation"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]

        return df

    def detect(self, symbol: str, df: pd.DataFrame) -> List[AnomalyEvent]:
        """
        Given preprocessed df, return list of AnomalyEvent where |deviation| > threshold.
        """
        df = self.preprocess(df)
        # Filter only rows where rolling_std is non-zero and deviation exceeds threshold
        mask = df["rolling_std"].notna() & (df["rolling_std"] > 0) & (df["deviation"].abs() > self.sigma_thresh)

        events = []
        for _, row in df[mask].iterrows():
            evt = AnomalyEvent(
                symbol=symbol,
                timestamp=row["datetime"],
                price=row["close"],
                deviation=row["deviation"]
            )
            events.append(evt)

        return events
