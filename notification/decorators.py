import functools
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),                    # Print to console
        logging.FileHandler("notifications.log")    # Save to file
    ]
)

logger = logging.getLogger("notification")


def logged(send):
    """Wrap a provider's send() to log attempts, successes, and failures."""

    @functools.wraps(send)
    def wrapper(self, message: str) -> None:
        provider_name = type(self).__name__
        recipients = getattr(self, "recipients", "unknown")
        logger.info(
            "Sending %s bytes via %s to %s",
            len(message.encode('utf-8')), provider_name, recipients,
        )
        try:
            result = send(self, message)
        except Exception:
            logger.exception("Failed to send via %s", provider_name)
            raise
        logger.info("Sent successfully via %s", provider_name)
        return result

    return wrapper
