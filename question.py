from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import collate

from base import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String(255,collation="utf8mb4_bin"))
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    created_on = Column(DateTime, default=func.now())
    position = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    game = relationship(
        'Game',
        backref=backref('games',
                        uselist=True,
                        # cascade='delete,all'
                        ))
    answers = relationship(
        'Answer',
        backref=backref('answer',
                        uselist=True,
                        cascade='delete,all'))
