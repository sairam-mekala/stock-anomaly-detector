import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # loads EMAIL_* and RECEIVER_EMAIL

class EmailAlerter:
    def __init__(self):
        self.host = os.getenv("EMAIL_HOST")
        self.port = int(os.getenv("EMAIL_PORT", 587))
        self.user = os.getenv("EMAIL_USER")
        self.pwd  = os.getenv("EMAIL_PASS")
        self.to   = os.getenv("RECEIVER_EMAIL")
        if not all([self.host, self.port, self.user, self.pwd, self.to]):
            raise ValueError("Email credentials not fully set in .env")

    def send(self, subject: str, body: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = self.user
        msg["To"]      = self.to
        msg.set_content(body)

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.user, self.pwd)
            smtp.send_message(msg)
