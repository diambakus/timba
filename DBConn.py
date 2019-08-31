import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


engine = sqlalchemy.create_engine('mysql+mysqlconnector://timba:timbapa55@localhost/timbadb', echo=True)


def get_engine():
    return engine


Base = declarative_base()


def get_base():
    return Base


Base.metadata.create_all(engine)