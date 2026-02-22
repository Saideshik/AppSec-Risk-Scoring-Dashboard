from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

from app.db import Base  # noqa
from app import models  # noqa: F401

config = context.config
fileConfig(config.config_file_name)

def get_url() -> str:
    return os.environ["DATABASE_URL"]

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
