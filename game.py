from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    status = Column(Integer, default=1)  # STATUS_PRIVATE
    created_on = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        'User',
        backref=backref('user',
                        # uselist=True,
                        cascade='delete,all'))
    questions = relationship(
        'Question',
        backref=backref('question',
                        uselist=True,
                        # cascade='delete,all'
                        ))
    plays = relationship("Play", back_populates="game")
