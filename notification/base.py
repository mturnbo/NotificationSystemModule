from abc import ABC, abstractmethod


class NotificationProvider(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

    def validate_recipients(self, recipients: list[str]) -> None:
        """Validate recipient format for this provider. No-op by default —
        providers override this with their own format rules (email address,
        phone number, channel name, etc.) and call it from __init__."""
        pass
