'''
    Alembic main migration logic
'''
from sqlalchemy import create_engine
from alembic import context

from bootstrap import Container


def run_migrations_offline() -> None:
    '''
        Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.
    '''
    url = Container.instance().config.data.db.url_sync()
    context.configure(url=f'postgresql+psycopg://{url}')

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    '''
        Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.
    '''
    url = Container.instance().config.data.db.url_sync()
    connectable = create_engine(f'postgresql+psycopg://{url}')

    with connectable.connect() as connection:
        context.configure(connection=connection)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
