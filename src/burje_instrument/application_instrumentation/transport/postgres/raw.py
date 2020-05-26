import os

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def make_engine(conn_string=None) -> Engine:
    if conn_string is None:
        conn_string = os.environ.get('BURJE_TRANSPORT_POSTGRESQL_CONN_STRING')
    return create_engine(f'postgresql://{conn_string}', )


def create_tables(engine):
    Base.metadata.create_all(engine)


engine = make_engine()
session = sessionmaker(bind=engine)()
