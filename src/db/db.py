from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()


def build_db_url():
    url = os.getenv("POSTGRES_URL", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    database = os.getenv("POSTGRES_DB", "")
    return f"postgresql://{user}:{password}@{url}:{port}/{database}"


@contextmanager
def get_session() -> Session:
    engine = sa.create_engine(build_db_url())
    local_session = sessionmaker(bind=engine)
    session = local_session()
    try:
        yield session
    finally:
        session.close()
