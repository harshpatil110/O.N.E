import smtplib
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service for sending automated emails via Gmail SMTP.
    
    Attributes:
        gmail_address (str): The sender's Gmail address from environment variables.
        gmail_app_password (str): The Gmail app-specific password.
        hr_email (str): The recipient HR email address.
    """
    def __init__(self):
        self.gmail_address = os.getenv("GMAIL_ADDRESS")
        self.gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.hr_email = os.getenv("HR_EMAIL")

    def send_email(self, to: str, subject: str, html_body: str, cc: list = None) -> bool:
        """
        Sends an HTML email to the specified recipient.

        Args:
            to (str): Primary recipient email.
            subject (str): Subject line of the email.
            html_body (str): The HTML content of the email.
            cc (list, optional): List of CC recipient emails. Defaults to None.

        Returns:
            bool: True if sent successfully, False otherwise.
        """
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
            logger.info(f"Email sent successfully to {to}")
            return True
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            return False
