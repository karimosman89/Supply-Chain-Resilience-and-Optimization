from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configure the database URL from environment or use default
database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/test_db')
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
try:
    from models.models import Base  # Import your models here
    target_metadata = Base.metadata
except ImportError as e:
    print(f"Warning: Could not import models: {e}")
    print("Creating fallback Base metadata...")
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    target_metadata = Base.metadata
except Exception as e:
    print(f"Error importing models: {e}")
    print("Creating fallback Base metadata...")
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    
    # Always use synchronous operations for consistency with models
    engine = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    with engine.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
