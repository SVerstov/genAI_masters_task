from sqlalchemy.ext.asyncio import AsyncSession

from db.dao.base import BaseDAO
from db.models import News


class NewsDAO(BaseDAO[News]):
    def __init__(self, session: AsyncSession):
        super().__init__(News, session)
