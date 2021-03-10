from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base





class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Integer, default=1)  # STATUS_PRIVATE
    created_on = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        'User',
        backref=backref('users',
                        # uselist=True,
                        cascade='delete,all'))
    questions = relationship(
        'Question',
        backref=backref('question',
                        uselist=True,
                        cascade='delete,all'))
    plays = relationship("Play", back_populates="game")
