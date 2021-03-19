from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    # chatid = Column(Integer, unique=True, nullable=True)
    # uid = Column(String, nullable=True)
    # alias = Column(String, nullable=True)
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

    def __init__(self, play, user, question, answer):
        self.user_id = user.id
        self.game_id = play.game.id
        self.game = play.game
        self.question_id = question.id
        self.question = question
        self.answer_id = answer.id
        self.answer = answer
        self.play_id = play.id
        self.play = play
