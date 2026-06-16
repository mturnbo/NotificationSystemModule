import functools
import logging

logger = logging.getLogger("notification")


def logged(send):
    """Wrap a provider's send() to log attempts, successes, and failures."""

    @functools.wraps(send)
    def wrapper(self, message: str) -> None:
        provider_name = type(self).__name__
        logger.info("Sending via %s: %s", provider_name, message)
        try:
            result = send(self, message)
        except Exception:
            logger.exception("Failed to send via %s", provider_name)
            raise
        logger.info("Sent successfully via %s", provider_name)
        return result

    return wrapper
