import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DBSettings:
    DB_TYPE: str = os.environ.get("DB_TYPE", 'sql')
    DB: str = os.environ.get("DB", 'sqlite')
    DB_HOST: [str | None] = os.environ.get("DB_HOST", 'localhost')
    DB_PORT: [str | None] = os.environ.get("DB_PORT", None)
    DB_NAME: str = os.environ.get("DB_NAME", 'db.sqlite3')

    DB_ECHO: bool = os.environ.get("DB_ECHO", True)

    def get_db_url(self):
        if self.DB_TYPE == 'sql' and self.DB == 'sqlite':
            return f'sqlite+aiosqlite:///{BASE_DIR}/{self.DB_NAME}'

db_settings = DBSettings()
