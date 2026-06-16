import os
import smtplib
from email.mime.text import MIMEText

from notification.base import NotificationProvider


class EmailProvider(NotificationProvider):
    def __init__(self, recipients: list[str]):
        self.recipients = recipients
        self.host = os.environ["SMTP_HOST"]
        self.port = int(os.environ["SMTP_PORT"])
        self.user = os.environ["SMTP_USER"]
        self.password = os.environ["SMTP_PASSWORD"]
        self.from_addr = os.environ["SMTP_FROM"]

    def send(self, message: str) -> None:
        msg = MIMEText(message)
        msg["Subject"] = message.splitlines()[0]
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.recipients)

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.from_addr, self.recipients, msg.as_string())
