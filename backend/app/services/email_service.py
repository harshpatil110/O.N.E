import smtplib
import logging
import os
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service for sending automated emails via Gmail SMTP.
    """
    def __init__(self):
        self.gmail_address = os.getenv("GMAIL_ADDRESS")
        self.gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.hr_email = os.getenv("HR_EMAIL")

    async def send_email(self, to: str, subject: str, html_body: str, cc: list = None) -> bool:
        """
        Sends an HTML email to the specified recipient asynchronously.
        """
        return await asyncio.to_thread(self._send_email_sync, to, subject, html_body, cc)

    def _send_email_sync(self, to: str, subject: str, html_body: str, cc: list = None) -> bool:
        """
        Synchronous helper for send_email.
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

    async def send_onboarding_email(self, recipient_name: str, recipient_email: str) -> bool:
        """
        Sends a specific welcome onboarding email.
        """
        subject = "Welcome to Nexus Tech - Your Onboarding Package"
        html_body = f"""
        <html>
            <body>
                <h1>Welcome to Nexus Tech, {recipient_name}!</h1>
                <p>We are thrilled to have you join our engineering team at Nexus Tech.</p>
                <p>I am your O.N.E (Onboarding Navigation Entity) assistant. I'll be guiding you through your first few days.</p>
                <p>Your journey has already started in our portal. Please head back to the chat to see your interactive checklist.</p>
                <br>
                <p>Best regards,<br>The O.N.E Team at Nexus Tech</p>
            </body>
        </html>
        """
        return await self.send_email(recipient_email, subject, html_body)
