import logging
from pathlib import Path

import yaml
import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    logger_conf_path = Path('config/logging.yaml')
    log_path = Path('logs')
    # Отключение всех существующих логгеров

    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.disabled = True

    try:
        log_path.mkdir(exist_ok=True)
        with logger_conf_path.open("r", encoding='utf-8') as f:
            logging_config = yaml.safe_load(f)
            logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("logging config file not found, use basic config")
