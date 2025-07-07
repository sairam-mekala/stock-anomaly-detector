import yfinance as yf
import pandas as pd

class DataClient:
    def __init__(self):
        pass

    def get_historical(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetch historical 5-minute interval data for a given symbol
        """
        df = yf.download(tickers=symbol, start=start, end=end, interval="5m", progress=False)
        df = df.reset_index()
        df = df.rename(columns={
            "Datetime": "datetime",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        })
        return df[["datetime", "open", "high", "low", "close", "volume"]]
