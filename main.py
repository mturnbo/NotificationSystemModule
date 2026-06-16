from notification import NotificationService, NotificationFactory
from notification.providers import EmailProvider, SMSProvider

# Step 4: Use Different Strategies — direct instantiation
email_service = NotificationService(EmailProvider(recipients=["user@example.com"]))
email_service.notify("Your report is ready.")

sms_service = NotificationService(SMSProvider())
sms_service.notify("Your report is ready.")

# Step 5: Factory — create from a string (e.g. from config)
provider = NotificationFactory.create("slack")
service = NotificationService(provider)
service.notify("Deployment completed successfully.")

# Step 6: Extensibility — Discord added without touching existing code
discord_service = NotificationService(NotificationFactory.create("discord"))
discord_service.notify("New PR opened for review.")
