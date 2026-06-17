# Notification System Module

Companion code for the Medium article **"Building An Extensible System in Python"** — part of a series on object-oriented design.

The module demonstrates how abstract classes, composition, the Strategy Pattern, and the Factory Pattern work together to build a notification system that can be extended without modifying existing code.

## Structure

```
notification/
├── base.py              # NotificationProvider ABC
├── providers/
│   ├── email.py         # EmailProvider
│   ├── sms.py           # SMSProvider
│   ├── slack.py         # SlackProvider
│   └── discord.py       # DiscordProvider
├── service.py           # NotificationService (composition)
└── factory.py           # NotificationFactory
tests/
└── test_notifications.py
main.py                  # Demo script
```

## Usage

### Direct instantiation (Strategy Pattern)

```python
from notification import NotificationService
from notification.providers import EmailProvider, SMSProvider

service = NotificationService(EmailProvider())
service.notify("Your report is ready.")
# EMAIL: Your report is ready.

service = NotificationService(SMSProvider())
service.notify("Your report is ready.")
# SMS: Your report is ready.
```

### Factory (create from config or string)

```python
from notification import NotificationService, NotificationFactory

provider = NotificationFactory.create("slack")
service = NotificationService(provider)
service.notify("Deployment completed successfully.")
# SLACK: Deployment completed successfully.
```

### Adding a new channel (no existing code changes required)

```python
from notification import NotificationProvider, NotificationService

class TeamsProvider(NotificationProvider):
    def send(self, message: str) -> None:
        # TODO: replace with real Microsoft Teams API call
        print(f"TEAMS: {message}")

service = NotificationService(TeamsProvider())
service.notify("New PR opened for review.")
# TEAMS: New PR opened for review.
```

## Running the demo

```bash
python main.py
```

## Running tests

```bash
python -m pytest tests/ -v
```

## Concepts covered

| Pattern | Where |
|---|---|
| Abstract Classes | `notification/base.py` |
| Multiple Implementations | `notification/providers/` |
| Composition | `notification/service.py` |
| Strategy Pattern | `main.py` |
| Factory Pattern | `notification/factory.py` |
| Open/Closed Principle | New providers extend without modifying core |
