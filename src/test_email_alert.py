from alerter import EmailAlerter

if __name__ == "__main__":
    alerter = EmailAlerter()
    subject = "[TEST] Anomaly Alert Test Email"
    body = "📈 Symbol: TEST\nTime: 2025-07-07 13:45\nPrice: 999.99\nDeviation: +3.00σ"
    
    print("Sending test email...")
    alerter.send(subject, body)
    print("✅ Test email sent!")
