import sqlalchemy

from backend.database.db import engine


def dep_session() -> sqlalchemy.orm.Session:
    with engine.Session(future=True) as session:
        yield session