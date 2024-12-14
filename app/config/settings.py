from pathlib import Path

BASE_DIR = Path().parent.parent.parent

class Settings:
    db_type: str = 'sql'
    db: str = 'sqlite'
    db_host: [str | None] = 'localhost'
    db_port: [str | None] = None
    db_name: str = 'db.sqlite3'

    echo = True

    def get_db_url(self):
        # if self.db_type == 'sql' and self.db_type == 'sqlite':
        return f'sqlite+aiosqlite:///{BASE_DIR}/{self.db_name}'

settings = Settings()