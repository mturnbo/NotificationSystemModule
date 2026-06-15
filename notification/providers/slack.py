from notification.base import NotificationProvider


class SlackProvider(NotificationProvider):
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"SLACK: {message}")
