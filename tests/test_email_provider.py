import pytest
from notification.providers import EmailProvider


def test_send_connects_to_configured_host(mock_smtp):
    mock_cls, _ = mock_smtp
    EmailProvider(recipients=["a@example.com"]).send("Hello")
    mock_cls.assert_called_once_with("smtp.testmail.app", 587)


def test_send_uses_starttls(mock_smtp):
    _, instance = mock_smtp
    EmailProvider(recipients=["a@example.com"]).send("Hello")
    instance.starttls.assert_called_once()


def test_send_authenticates(mock_smtp):
    _, instance = mock_smtp
    EmailProvider(recipients=["a@example.com"]).send("Hello")
    instance.login.assert_called_once_with("test-api-key", "test-api-key")


def test_send_addresses_all_recipients(mock_smtp):
    _, instance = mock_smtp
    recipients = ["a@example.com", "b@example.com"]
    EmailProvider(recipients=recipients).send("Hello")
    args = instance.sendmail.call_args
    assert args[0][1] == recipients


def test_send_includes_message_in_body(mock_smtp):
    _, instance = mock_smtp
    EmailProvider(recipients=["a@example.com"]).send("Hello world")
    raw_message = instance.sendmail.call_args[0][2]
    assert "Hello world" in raw_message


def test_send_uses_first_line_as_subject(mock_smtp):
    _, instance = mock_smtp
    EmailProvider(recipients=["a@example.com"]).send("Subject line\nBody text")
    raw_message = instance.sendmail.call_args[0][2]
    assert "Subject: Subject line" in raw_message


def test_missing_env_var_raises(monkeypatch):
    monkeypatch.delenv("SMTP_HOST")
    with pytest.raises(KeyError):
        EmailProvider(recipients=["a@example.com"])


@pytest.mark.parametrize("invalid_recipient", [
    "not-an-email",
    "missing-domain@",
    "@missing-local.com",
    "no-at-sign.com",
    "spaces in@address.com",
])
def test_invalid_email_address_raises(invalid_recipient):
    with pytest.raises(ValueError, match="Invalid email address"):
        EmailProvider(recipients=[invalid_recipient])


def test_invalid_email_among_valid_recipients_raises():
    with pytest.raises(ValueError, match="Invalid email address"):
        EmailProvider(recipients=["good@example.com", "not-an-email"])


def test_valid_email_addresses_do_not_raise(mock_smtp):
    EmailProvider(recipients=["a@example.com", "b.c@sub.example.co.uk"]).send("Hello")
