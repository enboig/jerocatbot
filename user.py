from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    # questions = relationship(
    #     'Question',
    #     backref=backref('user-questions',
    #                     uselist=True,
    #                     cascade='delete,all'))
    # answers = relationship(
    #     'Answer',
    #     backref=backref('user-answers',
    #                     uselist=True,
    #                     cascade='delete,all'))
    # games = relationship(
    #     'Game',
    #     backref=backref('user-games',
    #                     uselist=True,
    #                     cascade='delete,all'))

    def __init__(self, id=0, username=""):
        self.id = id
        self.username = username
