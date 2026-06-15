from .base import NotificationProvider


class NotificationService:
    def __init__(self, provider: NotificationProvider):
        self.provider = provider

    def notify(self, message: str) -> None:
        self.provider.send(message)
