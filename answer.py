from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref

from base import Base


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    created_on = Column(DateTime, default=func.now())
    question_id = Column(Integer, ForeignKey('question.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    question = relationship(
        "Question",
        backref=backref('questions',
                        uselist=True,
                        cascade='delete,all'))




