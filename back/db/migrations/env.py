import asyncio
import logging.config
import os
from pathlib import Path

import yaml
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import create_engine

from config import Config
from db.base import Base


def make_db_url() -> str:
    config = Config()
    db = config.db
    url = f"{db.type}+{db.connector}://{db.login}:{db.password}@{db.host_and_port}/{db.name}"
    return url


db_url = make_db_url()
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
logging.config.fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        create_engine(
            url=db_url,
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
