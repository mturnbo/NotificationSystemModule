from notification.base import NotificationProvider


class SMSProvider(NotificationProvider):
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"SMS: {message}")
