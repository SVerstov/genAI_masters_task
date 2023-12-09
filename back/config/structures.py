import os
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel
import yaml

from pydantic.functional_validators import model_validator
from logging import getLogger

from typing import Self

logger = getLogger(__name__)


class ConfigBranch(BaseModel):
    """
    Базовый класс для веток конфига с автоматической загрузкой параметров по аннотациям
    Также берёт данные из переменных окружения, если в конфиге переменная выглядит так: ${SOME_ENV_VAR}
    """

    @model_validator(mode='before')
    @classmethod
    def check_data(cls, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('{$') and value.endswith('}'):
                param_name = value.lstrip('{$').rstrip('}')
                data[key] = os.getenv(param_name)
        return data

    @model_validator(mode='after')
    def launch_after_load(self):
        self.after_load()
        return self

    def after_load(self):
        # Переопределить если нужны дополнительные действия с конфигом
        pass


@dataclass
class ConfigBase:
    conf_path_prod: Path = Path("config/config.yaml")
    conf_path_dev: Path = Path("config/config.dev.yaml")

    def after_load(self):
        # Переопределить если нужны дополнительные действия с конфигом
        pass

    def __init__(self, custom_path: Path = None):
        if custom_path:
            self.conf_path = custom_path
        else:
            self.conf_path = self.conf_path_dev if os.getenv('DEV_MODE') else self.conf_path_prod

        with open(self.conf_path, 'r', encoding='utf-8') as f:
            config_dct = yaml.safe_load(f)

            for attr, config_branch in self.__annotations__.items():
                if issubclass(config_branch, ConfigBranch):
                    self.__setattr__(attr, config_branch.model_validate(config_dct[attr]))
        self.after_load()
