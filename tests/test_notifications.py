import pytest
from unittest.mock import MagicMock
from notification import NotificationService, NotificationFactory, NotificationProvider
from notification.providers import EmailProvider, SMSProvider, SlackProvider, DiscordProvider


def test_email_provider_send_does_not_raise():
    EmailProvider(recipients=["test@example.com"]).send("hello")


def test_sms_provider(capsys):
    SMSProvider().send("hello")
    assert capsys.readouterr().out == "SMS: hello\n"


def test_slack_provider(capsys):
    SlackProvider().send("hello")
    assert capsys.readouterr().out == "SLACK: hello\n"


def test_discord_provider_send_does_not_raise():
    webhook = "https://discord.com/api/webhooks/123456789/abcDEF"
    DiscordProvider(webhook_urls=[webhook]).send("hello")


def test_service_delegates_to_provider():
    provider = MagicMock(spec=NotificationProvider)
    NotificationService(provider).notify("test message")
    provider.send.assert_called_once_with("test message")


def test_service_swaps_provider(capsys):
    NotificationService(SMSProvider()).notify("test message")
    assert capsys.readouterr().out == "SMS: test message\n"


@pytest.mark.parametrize("key,cls,kwargs", [
    ("email", EmailProvider, {"recipients": ["test@example.com"]}),
    ("sms", SMSProvider, {}),
    ("slack", SlackProvider, {}),
    ("discord", DiscordProvider, {"webhook_urls": ["https://discord.com/api/webhooks/123456789/abcDEF"]}),
])
def test_factory_returns_correct_type(key, cls, kwargs):
    assert isinstance(NotificationFactory.create(key, **kwargs), cls)


def test_factory_case_insensitive():
    assert isinstance(NotificationFactory.create("EMAIL", recipients=["test@example.com"]), EmailProvider)


def test_factory_unknown_provider():
    with pytest.raises(ValueError, match="Unknown provider"):
        NotificationFactory.create("carrier_pigeon")


def test_new_provider_satisfies_contract(capsys):
    class PushProvider(NotificationProvider):
        def send(self, message: str) -> None:
            print(f"PUSH: {message}")

    NotificationService(PushProvider()).notify("ping")
    assert capsys.readouterr().out == "PUSH: ping\n"
