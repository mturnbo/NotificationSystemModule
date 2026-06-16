import re

import requests

from notification.base import NotificationProvider
from notification.decorators import logged

WEBHOOK_PATTERN = re.compile(r"^https://discord(app)?\.com/api/webhooks/\d+/.+$")
MAX_MESSAGE_LENGTH = 2000


class DiscordProvider(NotificationProvider):
    def __init__(self, webhook_urls: list[str]):
        self.validate_recipients(webhook_urls)
        self.recipients = webhook_urls

    def validate_recipients(self, recipients: list[str]) -> None:
        for url in recipients:
            if not WEBHOOK_PATTERN.match(url):
                raise ValueError(f"Invalid Discord webhook URL: {url}")

    @logged
    def send(self, message: str) -> None:
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message exceeds Discord's {MAX_MESSAGE_LENGTH}-char limit")
        for url in self.recipients:
            response = requests.post(url, json={"content": message})
            response.raise_for_status()
