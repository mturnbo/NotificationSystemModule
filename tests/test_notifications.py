import pytest
from notification import NotificationService, NotificationFactory, NotificationProvider
from notification.providers import EmailProvider, SMSProvider, SlackProvider, DiscordProvider


def test_email_provider(capsys):
    EmailProvider().send("hello")
    assert capsys.readouterr().out == "EMAIL: hello\n"


def test_sms_provider(capsys):
    SMSProvider().send("hello")
    assert capsys.readouterr().out == "SMS: hello\n"


def test_slack_provider(capsys):
    SlackProvider().send("hello")
    assert capsys.readouterr().out == "SLACK: hello\n"


def test_discord_provider(capsys):
    DiscordProvider().send("hello")
    assert capsys.readouterr().out == "DISCORD: hello\n"


def test_service_delegates_to_provider(capsys):
    NotificationService(EmailProvider()).notify("test message")
    assert capsys.readouterr().out == "EMAIL: test message\n"


def test_service_swaps_provider(capsys):
    NotificationService(SMSProvider()).notify("test message")
    assert capsys.readouterr().out == "SMS: test message\n"


@pytest.mark.parametrize("key,cls", [
    ("email", EmailProvider),
    ("sms", SMSProvider),
    ("slack", SlackProvider),
    ("discord", DiscordProvider),
])
def test_factory_returns_correct_type(key, cls):
    assert isinstance(NotificationFactory.create(key), cls)


def test_factory_case_insensitive():
    assert isinstance(NotificationFactory.create("EMAIL"), EmailProvider)


def test_factory_unknown_provider():
    with pytest.raises(ValueError, match="Unknown provider"):
        NotificationFactory.create("carrier_pigeon")


def test_new_provider_satisfies_contract(capsys):
    class PushProvider(NotificationProvider):
        def send(self, message: str) -> None:
            print(f"PUSH: {message}")

    NotificationService(PushProvider()).notify("ping")
    assert capsys.readouterr().out == "PUSH: ping\n"
