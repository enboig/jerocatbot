from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    created_on = Column(DateTime, default=func.now())
    position = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    game = relationship(
        'Game',
        backref=backref('games',
                        uselist=True,
                        cascade='delete,all'))
    answers = relationship(
        'Answer',
        backref=backref('answer',
                        uselist=True,
                        cascade='delete,all'))
