from data_client import DataClient
from detector import AnomalyDetector

if __name__ == "__main__":
    client = DataClient()
    detector = AnomalyDetector(window=20, sigma_thresh=2.0)

    # Fetch 1 day of 5-minute data for AAPL (last week)
    df = client.get_historical("AAPL", "2025-07-01", "2025-07-07")
    events = detector.detect("AAPL", df)

    if not events:
        print("No anomalies detected.")
    else:
        print("Detected anomalies:")
        for e in events:
            print(" ", e)
