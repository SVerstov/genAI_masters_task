import os

import logging.config

from pydantic import BaseModel

from config.structures import ConfigBranch, ConfigBase

logger = logging.getLogger(__name__)


class AppConfig(ConfigBranch):
    fast_api_port: int


class DBConfig(ConfigBranch):
    type: str
    connector: str
    url: str
    # host: str
    # port: int
    login: str
    password: str
    name: str
    show_echo: bool


class ParserConfig(ConfigBranch):
    parser_period_sec: int


class Config(ConfigBase):
    """ Подключать ветки конфига (класс от ConfigBranch) сюда"""
    dev_mode: bool

    app: AppConfig
    db: DBConfig
    parser: ParserConfig

    def after_load(self):
        self.dev_mode = bool(os.getenv('DEV_MODE'))
