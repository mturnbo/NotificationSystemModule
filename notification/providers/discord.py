import re

from notification.base import NotificationProvider
from notification.decorators import logged

WEBHOOK_PATTERN = re.compile(r"^https://discord(app)?\.com/api/webhooks/\d+/.+$")


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
        # TODO: replace print with real API call
        print(f"DISCORD to {self.recipients}: {message}")
