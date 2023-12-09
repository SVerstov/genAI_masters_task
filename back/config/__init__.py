import os
from contextlib import suppress

from .conf_loader import Config
from .logger_loader import setup_logging

with suppress(FileNotFoundError):
    with open("../.env") as f:
        line = f.readline()
        while line:
            k, v = line.split("=", 1)
            os.environ[k] = v.strip()
            line = f.readline()

config = Config()
