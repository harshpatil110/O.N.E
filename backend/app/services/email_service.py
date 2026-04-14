import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailService:
    def __init__(self):
        self.gmail_address = os.getenv("GMAIL_ADDRESS")
        self.gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.hr_email = os.getenv("HR_EMAIL")

    def send_email(self, to: str, subject: str, html_body: str, cc: list = None) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.gmail_address
            msg["To"] = to
            if cc:
                msg["Cc"] = ", ".join(cc)
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_address, self.gmail_app_password)
                recipients = [to] + (cc or [])
                server.sendmail(self.gmail_address, recipients, msg.as_string())
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
