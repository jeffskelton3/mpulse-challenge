import os
import warnings

import alembic
import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from alembic import command
from sqlalchemy_utils import database_exists

from src.db.db import Base, build_connection_url


@pytest.fixture(scope="session")
def connection(request):
    connection_url = build_connection_url()
    database = f'{os.getenv("POSTGRES_DB", "")}_test'
    if not database_exists(f"{connection_url}/{database}"):
        engine = create_engine(connection_url)
        session = sessionmaker(bind=engine)()
        session.connection().connection.set_isolation_level(0)
        session.execute(f"CREATE DATABASE {database}")
        session.connection().connection.set_isolation_level(1)
        session.close()

    engine = create_engine(f"{connection_url}/{database}")

    return engine.connect()


# @pytest.fixture(scope="session")
# def session(connection):
#     engine = connection.engine
#     session = sessionmaker(bind=engine)()
#     return session


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request, apply_migrations):
    """Setup test database.

    Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    Base.metadata.bind = connection
    Base.metadata.create_all()

    def teardown():
        Base.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture
def db_session(connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()
