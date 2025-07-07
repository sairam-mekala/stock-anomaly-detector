from data_client import DataClient

if __name__ == "__main__":
    c = DataClient()
    df = c.get_historical("AAPL", "2025-07-03", "2025-07-05")
    print("Columns:", df.columns.tolist())
    print("HEAD:\n", df.head())
