from .providers import EmailProvider, SMSProvider, SlackProvider, DiscordProvider


class NotificationFactory:
    @staticmethod
    def create(provider_type: str, **kwargs):
        providers = {
            "email": EmailProvider,
            "sms": SMSProvider,
            "slack": SlackProvider,
            "discord": DiscordProvider,
        }
        provider_class = providers.get(provider_type.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_type}")
        return provider_class(**kwargs)
