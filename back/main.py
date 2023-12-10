from typing import Union

from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy import desc, select
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run

from config import Config, setup_logging
from db import News
from db.base import create_pool
from db.dao import HolderDao
from periodic_tasks import init_scheduler

app = FastAPI()


def get_config(request: Request) -> Config:
    return request.app.state.config


def get_dao(request: Request) -> HolderDao:
    return request.state.dao


@app.middleware("http")
async def add_dao_and_config_middleware(request: Request, call_next):
    """ Adds dao to request, wraps fastapi functions in a context manager.
    Get it like this: dao: HolderDao = request.state.dao
    """
    pool = create_pool(app.state.config.db)
    async with pool() as session:
        dao = HolderDao(session)
        request.state.dao = dao
        response = await call_next(request)
        await session.commit()
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/get_news")
async def get_news(limit: int = 5,
                   config: Config = Depends(get_config),
                   dao: HolderDao = Depends(get_dao)):
    news = await dao.news.get_many(order_by=News.id, _desc=True, limit=config.parser.news_limit)
    return [{
        'news_id': item.news_id,
        'image': item.image,
        'title': item.title,
        'text': item.text,
        'parsed_at': item.parsed_at
    }
        for item in news
    ]


@app.on_event("startup")
def startup_event():
    config = Config()
    init_scheduler(config=config)
    app.state.config = config


if __name__ == '__main__':
    setup_logging()
    run(app, host="0.0.0.0", port=5000)
