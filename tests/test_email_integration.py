"""
Integration tests for EmailProvider against TestMail.app.

Requires a populated .env file (copy .env.example and fill in credentials).
Run with: pytest -m integration -v

TestMail.app setup:
  1. Sign up at https://testmail.app (free tier: 100 emails/month)
  2. Copy your API key and namespace from the dashboard
  3. SMTP: host=smtp.testmail.app, port=587, user=<api-key>, password=<api-key>
  4. Inbox addresses: <namespace>.<tag>@inbox.testmail.app
"""
import os
import time

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module", autouse=True)
def require_smtp_env():
    if not os.environ.get("SMTP_HOST"):
        pytest.skip("SMTP credentials not set — copy .env.example to .env to run integration tests")


def _poll_testmail(api_key: str, namespace: str, tag: str, subject: str, timeout: int = 15):
    url = "https://api.testmail.app/api/json"
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(url, params={"apikey": api_key, "namespace": namespace, "tag": tag, "limit": 5})
        resp.raise_for_status()
        emails = resp.json().get("emails", [])
        for email in emails:
            if email.get("subject") == subject:
                return email
        time.sleep(2)
    return None


def test_email_arrives_in_testmail_inbox():
    from notification.providers import EmailProvider

    api_key = os.environ["TESTMAIL_API_KEY"]
    namespace = os.environ["TESTMAIL_NAMESPACE"]
    tag = "integration-test"
    recipient = f"{namespace}.{tag}@inbox.testmail.app"
    subject = f"Integration test {int(time.time())}"

    EmailProvider(recipients=[recipient]).send(f"{subject}\nThis is the body.")

    email = _poll_testmail(api_key, namespace, tag, subject)
    assert email is not None, f"Email with subject '{subject}' did not arrive within 15 seconds"
    assert subject in email["subject"]
