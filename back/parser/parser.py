import re
from logging import getLogger
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from httpx import AsyncClient

from config import Config
from db.base import create_pool
from db.dao import HolderDao
from db.models import News

logger = getLogger(__name__)


class Parser:
    def __init__(self, config: Config, dao: HolderDao, http_client: AsyncClient):
        self.config = config
        self.dao = dao
        self.http_client = http_client

    async def run(self):
        logger.info('Parsing started!')
        news_ids = await self._parse_last_news_ids()
        await self._filter_old_news_ids(news_ids)
        if not news_ids:
            logger.info('There are no new news!')
            return

        for news_id in news_ids:
            await self._parse_and_save_news_by_id(news_id)
        logger.info(f'Parsing complete! New news: {len(news_ids)}')

    async def _parse_last_news_ids(self) -> set[int]:
        """ find and return ids for the last news """
        limit = self.config.parser.news_limit
        response = await self.http_client.get(self.config.parser.main_uri)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list_div = soup.find('div', class_='news-list short')

        if not news_list_div:
            return []

        news_items = news_list_div.find_all('a', class_='news-item')
        news_ids = set()
        for item in news_items:
            if len(news_ids) >= limit:
                break
            if not item.find(class_='border'):
                news_id = re.findall(r'(\d+)\.html$', item['href'])
                news_ids.add(int(news_id[0]))
        return news_ids

    async def _filter_old_news_ids(self, news_ids: set[int]):
        old_ids = await self.dao.news.get_many(News.news_id.in_(news_ids), get_only=News.news_id)
        news_ids.difference_update(old_ids)

    async def _parse_and_save_news_by_id(self, news_id: int):
        uri = self.config.parser.news_uri.format(id=news_id)
        response = await self.http_client.get(uri)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='article-title').text.strip()
        news_block = soup.find('div', class_='article-text')
        img_el = news_block.find('img')
        if img_el:
            img_link = urljoin(self.config.parser.main_uri, img_el['src'])
        else:
            img_link = None

        text_el = news_block.find("span", class_="article-body")
        article_text = ' '.join(p.get_text(strip=True) for p in text_el.find_all("p"))
        news = News(
            news_id=news_id,
            title=title,
            image=img_link,
            text=article_text
        )
        self.dao.session.add(news)


async def launch_parser(config: Config):
    """ Init and launches parser, makes commit at the end of parsing """
    pool = create_pool(config.db)
    async with httpx.AsyncClient(timeout=10) as http_client:
        async with pool() as db_session:
            parser = Parser(config=config,
                            dao=HolderDao(db_session),
                            http_client=http_client)
            await parser.run()
            await db_session.commit()
