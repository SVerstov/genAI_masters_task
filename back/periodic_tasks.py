from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config
from parser import launch_parser

from logging import getLogger

logger = getLogger(__name__)


def init_scheduler(config: Config):
    """ Periodic task controller """

    scheduler_async = AsyncIOScheduler()

    scheduler_async.add_job(
        func=launch_parser,
        trigger='interval',
        seconds=config.parser.parse_interval_sec,
        next_run_time=datetime.now(),
        kwargs={'config': config}
    )
    logger.warning('BEFORE LAUNCH')
    scheduler_async.start()
