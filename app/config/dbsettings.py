from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DBSettings:
    db_type: str = 'sql'
    db: str = 'sqlite'
    db_host: [str | None] = 'localhost'
    db_port: [str | None] = None
    db_name: str = 'db.sqlite3'

    echo = True

    def get_db_url(self):
        if self.db_type == 'sql' and self.db == 'sqlite':
            return f'sqlite+aiosqlite:///{BASE_DIR}/{self.db_name}'


class BotSettings:
    BOT_NAME: str

    API_ID: int
    API_HASH: str
    BOT_TOKEN: str


db_settings = DBSettings()
bot_settings = BotSettings()
