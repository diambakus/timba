#!/usr/bin/env python3.6

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser


def read_database_config(filename='/home/diambakus/PycharmProjects/timba/config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


config_db = read_database_config()
engine = sqlalchemy.create_engine('mysql+mysqlconnector://'+config_db['user']+':'+config_db['password']+'@'+
                                  config_db['host']+'/'+config_db['database'], echo=True)


def get_engine():
    return engine


Base = declarative_base()


def get_base():
    return Base


Base.metadata.create_all(engine)
