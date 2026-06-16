from notification.base import NotificationProvider
from notification.decorators import logged


class SMSProvider(NotificationProvider):
    @logged
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"SMS: {message}")
