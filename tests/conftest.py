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


@pytest.fixture
def mock_smtp():
    """Direct access to the patched SMTP class and connection instance."""
    with patch("notification.providers.email.smtplib.SMTP") as mock:
        instance = MagicMock()
        mock.return_value.__enter__ = MagicMock(return_value=instance)
        mock.return_value.__exit__ = MagicMock(return_value=False)
        yield mock, instance


@pytest.fixture(autouse=True)
def mock_discord_post(request):
    """Patch requests.post for all tests except integration tests."""
    if request.node.get_closest_marker("integration"):
        yield
        return
    with patch("notification.providers.discord.requests.post") as mock_post:
        mock_post.return_value.raise_for_status = MagicMock()
        yield mock_post
