from notification.base import NotificationProvider


class EmailProvider(NotificationProvider):
    def __init__(self, recipients: list[str]):
        self.recipients = recipients

    def send(self, message: str) -> None:
        # TODO: replace print with real SMTP call
        print(f"EMAIL to {self.recipients}: {message}")
