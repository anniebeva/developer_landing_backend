import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings
from app.database.base import Base
from app.models import *

# Alembic Config object
config = context.config


# Use database URL from .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without database connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations with database connection.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
            )
        )

        await connection.run_sync(lambda sync_connection: context.run_migrations())


def run_async_migrations():
    asyncio.run(run_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async_migrations()
