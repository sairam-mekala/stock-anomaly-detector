import pandas as pd
import pytest
from data_client import DataClient
from detector import AnomalyDetector, AnomalyEvent

def test_historical_fetch():
    client = DataClient()
    df = client.get_historical("AAPL", "2025-07-03", "2025-07-05")
    assert not df.empty
    assert "datetime" in df.columns
    assert "close" in df.columns

def test_preprocess_and_detect():
    # Create synthetic data: 25 bars with a spike at index 20
    times = pd.date_range("2025-07-01", periods=25, freq="5min")
    closes = list(range(100, 125))
    closes[20] = 200  # outlier spike
    df = pd.DataFrame({"datetime": times, "close": closes})
    
    det = AnomalyDetector(window=10, sigma_thresh=2.0)
    pre = det.preprocess(df)
    assert "rolling_mean" in pre.columns and "rolling_std" in pre.columns
    events = det.detect("FAKE", df)
    assert any(isinstance(e, AnomalyEvent) for e in events)
    assert any(e.price == 200 for e in events)
