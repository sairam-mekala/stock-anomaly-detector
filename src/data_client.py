import yfinance as yf
import pandas as pd

class DataClient:
    def __init__(self):
        pass

    def get_historical(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetch historical 5-minute interval data for a given symbol.
        Handles MultiIndex columns returned by yfinance.
        """
        df = yf.download(tickers=symbol, start=start, end=end, interval="5m", progress=False)

        if df.empty:
            raise ValueError(f"No data returned. Check symbol and date range: {start} to {end}")

        # 1) Bring the index into a column
        df = df.reset_index()

        # 2) If there is a MultiIndex on columns, drop the second level entirely
        if isinstance(df.columns, pd.MultiIndex):
            # This turns [('open','AAPL'),...] → ['open','high',...]
            df.columns = df.columns.droplevel(1)

        # 3) Rename to consistent lowercase names
        df = df.rename(columns={
            "Datetime": "datetime",
            "datetime": "datetime",
            "Open": "open",
            "open": "open",
            "High": "high",
            "high": "high",
            "Low": "low",
            "low": "low",
            "Close": "close",
            "close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
            "volume": "volume"
        })

        # 4) Return only the six key columns
        return df[["datetime", "open", "high", "low", "close", "volume"]]
