from data_client import DataClient

if __name__ == "__main__":
    c = DataClient()
    # df = c.get_historical("AAPL", "2024-07-01", "2024-07-03")
    df = c.get_historical("AAPL", "2025-07-03", "2025-07-05")

    if df.empty:
        print("❌ No data returned. Make sure the date range includes recent WEEKDAYS within the last 60 days.")
    else:
        print("✅ Data fetch successful. Here's the last 5 rows:")
        print(df.tail())
