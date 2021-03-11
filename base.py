# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import scoped_session
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if (config['database']["engine"] == "sqlite"):
    _DB_URI = 'sqlite:///' + \
        config['database']["database"]+'.sqlite'+"?check_same_thread=False"

engine = create_engine(_DB_URI)


#Session = sessionmaker(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()
