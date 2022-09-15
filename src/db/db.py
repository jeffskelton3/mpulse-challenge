from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


def build_db_url():
    connection_url = build_connection_url()
    database = get_db_name()
    return f"{connection_url}/{database}"


def get_db_name():
    database = os.getenv("POSTGRES_DB", "")
    env = os.getenv("ENV", "")
    if env == "test":
        return f"{database}_test"
    else:
        return database


def build_connection_url():
    url = os.getenv("POSTGRES_URL", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    return f"postgresql://{user}:{password}@{url}:{port}"


@contextmanager
def get_session() -> Session:
    engine = sa.create_engine(build_db_url())
    local_session = sessionmaker(bind=engine)
    session = local_session()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()
