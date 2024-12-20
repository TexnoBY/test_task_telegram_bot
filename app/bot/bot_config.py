import os


class BotSettings:
    BOT_NAME: str = os.environ.get("BOT_NAME", "BOT_NAME")
    API_ID: int = os.environ.get("API_ID", 'API_ID')
    API_HASH: str = os.environ.get("API_HASH", "API_HASH")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "BOT_TOKEN")


bot_settings = BotSettings()