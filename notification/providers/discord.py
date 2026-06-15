from notification.base import NotificationProvider


class DiscordProvider(NotificationProvider):
    def send(self, message: str) -> None:
        # TODO: replace print with real API call
        print(f"DISCORD: {message}")
