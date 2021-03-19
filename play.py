from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean

from base import Base


class Play(Base):
    __tablename__ = 'play'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    editor_enabled = Column(Boolean, default=False)
    status = Column(Integer, default=0)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", back_populates="plays")
