from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase, Query
#
#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.orm import sessionmaker, scoped_session
#from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean

import json
from sqlalchemy.types import TypeDecorator


from base import Base
#from base import TextPickleType


class Play(Base):
    __tablename__ = 'play'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    editor_enabled = Column(Boolean, default=False)
    status = Column(Integer, default=0)
#    saved_Data = Column(TextPickleType(),default={})
    attributes = Column(MutableType)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", back_populates="plays")

    def __init__(self, chat_id):
        # set mutable column to `Mutable` object
        self.chat_id = chat_id
        self.attributes = Mutable()
        self.attributes = {}
