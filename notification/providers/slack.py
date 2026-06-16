from notification.base import NotificationProvider
from notification.decorators import logged


class SlackProvider(NotificationProvider):
    @logged
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"SLACK: {message}")
