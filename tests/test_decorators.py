import logging
import pytest
from notification.providers import EmailProvider, SMSProvider


def test_logged_send_logs_attempt_and_success(caplog):
    with caplog.at_level(logging.INFO, logger="notification"):
        SMSProvider().send("hello")

    messages = [r.message for r in caplog.records]
    assert any("Sending via SMSProvider" in m and "hello" in m for m in messages)
    assert any("Sent successfully via SMSProvider" in m for m in messages)


def test_logged_send_logs_failure_and_reraises(caplog, mock_smtp):
    mock_cls, _ = mock_smtp
    mock_cls.side_effect = ConnectionError("smtp unreachable")

    with caplog.at_level(logging.INFO, logger="notification"):
        with pytest.raises(ConnectionError):
            EmailProvider(recipients=["a@example.com"]).send("hello")

    messages = [r.message for r in caplog.records]
    assert any("Sending via EmailProvider" in m for m in messages)
    assert any("Failed to send via EmailProvider" in m for m in messages)
    assert not any("Sent successfully" in m for m in messages)
