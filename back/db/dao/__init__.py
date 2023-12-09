from sqlalchemy.ext.asyncio import AsyncSession

from db.dao.base import BaseDAO
from db.dao.parser import NewsDAO


class HolderDao:
    """ Главный DAO. Подключать новые сюда"""

    def __init__(self, session: AsyncSession):
        self.news = NewsDAO

    async def commit(self):
        await self.session.commit()


__all__ = [BaseDAO, HolderDao]
