__all__ = (
    'repository'
)

from app.config.settings import settings
match settings.db_type:
    case 'sql':
        from .repositories import alchemy_repository as repository