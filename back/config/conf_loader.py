import os

import logging.config

from pydantic import BaseModel

from config.structures import ConfigBranch, ConfigBase

logger = logging.getLogger(__name__)


class DBConfig(ConfigBranch):
    type: str
    connector: str
    host_and_port: str
    login: str
    password: str
    name: str
    show_echo: bool

    @property
    def uri(self) -> str:
        return f"{self.type}+{self.connector}://{self.login}:{self.password}@{self.host_and_port}/{self.name}"


class ParserConfig(ConfigBranch):
    parse_interval_sec: int
    main_uri: str
    news_uri: str
    news_limit: int


class Config(ConfigBase):
    """ Подключать ветки конфига (класс от ConfigBranch) сюда"""
    dev_mode: bool

    db: DBConfig
    parser: ParserConfig

    def after_load(self):
        self.dev_mode = bool(os.getenv('DEV'))
