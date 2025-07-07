import time
from datetime import datetime, timedelta
from alerter import EmailAlerter
from data_client import DataClient
from detector import AnomalyDetector

def main():
    # 1) Configuration
    SYMBOLS = ["AAPL", "TSLA", "INFY"]
    WINDOW = 20            # number of bars for rolling stats
    SIGMA_THRESH = 0.01     # how many std devs to flag
    INTERVAL = "5m"        # polling interval
    FETCH_PERIOD = "1d"    # how much history to fetch each poll

    client = DataClient()
    detector = AnomalyDetector(window=WINDOW, sigma_thresh=SIGMA_THRESH)
    alerter  = EmailAlerter()
    
    print(f"[{datetime.now()}] Starting real‑time monitor for {SYMBOLS}.")
    print("Will poll every", INTERVAL, "and flag deviations >", SIGMA_THRESH, "σ.\n")

    # 2) Infinite polling loop
    try:
        while True:
            poll_time = datetime.now()
            print(f"[{poll_time}] Polling data...")

            for sym in SYMBOLS:
                # 3) Fetch the last FETCH_PERIOD of data at 5m intervals
                #    Note: yfinance supports period strings like "1d","5d"
                try:
                    df = client.get_historical(sym,
                        start=(poll_time - timedelta(days=1)).strftime("%Y-%m-%d"),
                        end=poll_time.strftime("%Y-%m-%d"))
                except ValueError as e:
                    print(f"  ⚠️  Skipping {sym}: {e}")
                    continue

                # 4) Detect anomalies
                events = detector.detect(sym, df)

                # 5) Print new anomaly events
                if events:
                    subject = f"[ALERT] {sym} anomalies detected"
                    lines = []
                    print(f"  ➤ {sym} anomalies:")
                    for e in events:
                        line = (f"{e.timestamp.strftime('%Y-%m-%d %H:%M')} "
                                f"price={e.price:.2f}, dev={e.deviation:.2f}σ")
                        lines.append(line)
                        print(f"      • {line}")
                    # send email
                    body = "\n".join(lines)
                    alerter.send(subject, body)
                    print(f"  ✉️  Email alert sent for {sym}")
                else:
                    print(f"  • {sym}: no anomalies.")

            # 6) Sleep until next interval
            mins = int(INTERVAL.rstrip("m"))
            print(f"\nSleeping for {mins} minutes...\n")
            time.sleep(mins * 60)

    except KeyboardInterrupt:
        print("\nMonitor stopped by user. Goodbye!")

if __name__ == "__main__":
    main()
