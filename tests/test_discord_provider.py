import pytest
import requests
from notification.providers import DiscordProvider

VALID_WEBHOOK = "https://discord.com/api/webhooks/123456789/abcDEF-ghiJKL"


def test_send_posts_to_webhook_url(mock_discord_post):
    DiscordProvider(webhook_urls=[VALID_WEBHOOK]).send("Hello")
    mock_discord_post.assert_called_once_with(VALID_WEBHOOK, json={"content": "Hello"})


def test_send_posts_to_all_webhooks(mock_discord_post):
    webhooks = [VALID_WEBHOOK, "https://discord.com/api/webhooks/987654321/xyz"]
    DiscordProvider(webhook_urls=webhooks).send("Hello")
    assert mock_discord_post.call_count == 2


def test_send_raises_status_errors(mock_discord_post):
    mock_discord_post.return_value.raise_for_status.side_effect = requests.HTTPError("boom")
    with pytest.raises(requests.HTTPError):
        DiscordProvider(webhook_urls=[VALID_WEBHOOK]).send("Hello")


def test_send_rejects_message_over_2000_chars(mock_discord_post):
    with pytest.raises(ValueError, match="2000-char limit"):
        DiscordProvider(webhook_urls=[VALID_WEBHOOK]).send("x" * 2001)
    mock_discord_post.assert_not_called()


def test_send_allows_message_at_2000_chars(mock_discord_post):
    DiscordProvider(webhook_urls=[VALID_WEBHOOK]).send("x" * 2000)
    mock_discord_post.assert_called_once()


@pytest.mark.parametrize("invalid_url", [
    "https://example.com/not-a-webhook",
    "https://discord.com/api/webhooks/not-numeric/abc",
    "discord.com/api/webhooks/123/abc",
    "https://discordapp.com/api/webhooks/",
])
def test_invalid_webhook_url_raises(invalid_url):
    with pytest.raises(ValueError, match="Invalid Discord webhook URL"):
        DiscordProvider(webhook_urls=[invalid_url])


def test_valid_discordapp_domain_does_not_raise(mock_discord_post):
    url = "https://discordapp.com/api/webhooks/123456789/abcDEF"
    DiscordProvider(webhook_urls=[url]).send("Hello")
