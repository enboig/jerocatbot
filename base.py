# coding=utf-8

#from sqlalchemy import *
import pymysql
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator

SIZE = 256

# class TextPickleType(TypeDecorator):

#     impl = sqlalchemy.Text(SIZE)

#     def process_bind_param(self, value, dialect):
#         if value is not None:
#             value = json.dumps(value)

#         return value

#     def process_result_value(self, value, dialect):
#         if value is not None:
#             value = json.loads(value)
#         return value

        
from sqlalchemy.orm import scoped_session
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if (config['database']["engine"] == "sqlite"):
    _DB_URI = 'sqlite:///' + \
        config['database']["database"]+'.sqlite'+"?check_same_thread=False"
elif (config['database']["engine"] == "mariadb"):
    _DB_URI = "mariadb+pymsql://"+config['database']["user"]+":"+config['database']["user"]+"@"+config['database']["host"]+"/"+config['database']["database"]+"?charset=utf8mb4"
else:
    print("volatile database")
    _DB_URI = 'sqlite://'

engine = create_engine(_DB_URI)
metadata = MetaData(bind=None)

#Session = sessionmaker(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()
