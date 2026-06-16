import pytest
from unittest.mock import patch, MagicMock

SMTP_ENV = {
    "SMTP_HOST": "smtp.testmail.app",
    "SMTP_PORT": "587",
    "SMTP_USER": "test-api-key",
    "SMTP_PASSWORD": "test-api-key",
    "SMTP_FROM": "ns.sender@inbox.testmail.app",
}


@pytest.fixture(autouse=True)
def smtp_env(monkeypatch):
    for key, value in SMTP_ENV.items():
        monkeypatch.setenv(key, value)


@pytest.fixture(autouse=True)
def mock_smtp_connection(request):
    """Patch smtplib.SMTP for all tests except integration tests."""
    if request.node.get_closest_marker("integration"):
        yield
        return
    instance = MagicMock()
    with patch("notification.providers.email.smtplib.SMTP") as mock_cls:
        mock_cls.return_value.__enter__ = MagicMock(return_value=instance)
        mock_cls.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_cls
