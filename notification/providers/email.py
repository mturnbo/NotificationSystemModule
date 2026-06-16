import os
import re
import smtplib
from email.mime.text import MIMEText
from notification.base import NotificationProvider
from notification.decorators import logged

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailProvider(NotificationProvider):
    def __init__(self, recipients: list[str]):
        self.validate_recipients(recipients)
        self.recipients = recipients
        self.host = os.environ["SMTP_HOST"]
        self.port = int(os.environ["SMTP_PORT"])
        self.user = os.environ["SMTP_USER"]
        self.password = os.environ["SMTP_PASSWORD"]
        self.from_addr = os.environ["SMTP_FROM"]

    def validate_recipients(self, recipients: list[str]) -> None:
        for recipient in recipients:
            if not EMAIL_PATTERN.match(recipient):
                raise ValueError(f"Invalid email address: {recipient}")

    @logged
    def send(self, message: str) -> None:
        msg = MIMEText(message)
        msg["Subject"] = message.splitlines()[0]
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.recipients)

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.from_addr, self.recipients, msg.as_string())
