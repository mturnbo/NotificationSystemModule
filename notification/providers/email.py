from notification.base import NotificationProvider


class EmailProvider(NotificationProvider):
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"EMAIL: {message}")
