from sqlalchemy.sql.expression import null
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
    attributes = Column(MutableType)
#    menus = Column(MutableType)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", back_populates="plays")

    def __init__(self, chat_id):
        # set mutable column to `Mutable` object
        self.chat_id = chat_id
        self.attributes = Mutable()
        self.attributes = {}
#        self.menus = Mutable()
#        self.menus = []

    def get(self, attribute):
        return self.attributes.get(attribute, None)

    def set(self, attribute, value):
        self.attributes[attribute] = value

    def unset(self, attribute):
        self.attributes.pop(attribute, None)
        pass

    # def menu_pop(self):
    #     if len(self.menus)>0:
    #         return self.menus.pop()
    #     else:
    #         return None

    # def menu_push(self, value):
    #     self.menus.append(value)
