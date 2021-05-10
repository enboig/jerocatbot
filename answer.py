from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean

from base import Base


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String(255))
    created_on = Column(DateTime, default=func.now())
    question_id = Column(Integer, ForeignKey('questions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    accepted = Column(Boolean, default=True)
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    question = relationship(
        "Question",
        backref=backref('questions',
                        uselist=True,
                        cascade='delete,all'))
    points = relationship(
        "Point",
        back_populates="answer",
        cascade="delete, merge, save-update"
    )
