from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.base import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    text = Column(String, nullable=False)
    parsed_at = Column(DateTime, default=datetime.now())
