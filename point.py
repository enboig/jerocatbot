from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    chatid = Column(Integer, unique=True)
    uid = Column(String, nullable=True)
    alias = Column(String, nullable=True)
    created_on = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship(
        'Game',
        backref=backref('game_points',
                            uselist=True,
                            cascade='delete,all'))
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(
        'Question',
        backref=backref('question_points',
                            uselist=True,
                            cascade='delete,all'))
    answer_id = Column(Integer, ForeignKey('answer.id'))
    answer = relationship(
        'Answer',
        backref=backref('answer_points',
                            uselist=True,
                            cascade='delete,all'))
    play_id = Column(Integer, ForeignKey('play.id'))
    play = relationship(
        'Play',
        backref=backref('play_points',
                            uselist=True,
                            cascade='delete,all'))
