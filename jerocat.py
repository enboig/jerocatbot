from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#from settings import TOKEN
Base = declarative_base()


class Jerocat:
    # Game status
    STATUS_PUBLIC = 1
    STATUS_PRIVATE = 2
    STATUS_PENDING = 3

    def __init__(self):
        if (config['database']["engine"] == "sqlite"):
            self.engine = create_engine(
                'sqlite:///'+config['database']["database"]+'.sqlite')
            self.session = sessionmaker()
            self.session.configure(bind=self.engine)
            #Base = declarative_base()
            Base.metadata.create_all(self.engine)
        self.repo = self.session()

    def answer_check(self, question, answer):
        """
        Checks if an answer is correct
        """
        return True

    def user_add(self, uid, name=None, alias=None):
        '''
        Insert a user
        '''
        u = self.User(uid=uid, name=name, alias=alias)
        self.repo.add(u)
        self.repo.commit()
        return u

    def game_add(self, name, user=None, status=0):
        '''
        Insert a empty game and returns its id
        '''
        g = self.Game(name=name, user=user)
        self.repo.add(g)
        self.repo.commit()
        return g

    def game_get(self, id, user=None):
        '''
        Insert a empty game and returns its id
        '''
        g = self.repo.query(self.Game).get(id)
        return g

    def game_list_full(self, uid=0):
        """
        Returns a list of games. If a user is send, it also list user games
        TODO filter by user
        """
        return self.repo.query(self.Game).all()

    def game_list(self, uid=0):
        """
        Returns a list of games. If a user is send, it also list user games
        TODO filter by user
        """
        list = {}
        for g in self.repo.query(self.Game).all():
            list[g.id] = g.name
        return list

    def game_allowed(self, uid=0):
        """
        Check if a game is valid
        """
        return True

    def question_add(self, game, question):
        '''
        Insert a question to the game
        '''
        q = self.Question(game=game, name=question)
        self.repo.add(q)
        self.repo.commit()
        position = self.repo.query(self.Question).filter(
            self.Question.game==q.game).filter(self.Question.id <= q.id).count()
        setattr(q, 'position', position)
        self.repo.commit()
        return q

    def answer_add(self, question, answer):
        a = self.Answer(question=question, name=answer)
        self.repo.add(a)
        self.repo.commit()
        return a

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

        def numerize():
            """
            Set the questions numbers
            """
            pass

    class Question(Base):
        __tablename__ = 'question'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        # Use default=func.now() to set the default hiring time
        # of an Employee to be the current time when an
        # Employee record was created
        created_on = Column(DateTime, default=func.now())
        position = Column(Integer, default=0)
        user_id = Column(Integer, ForeignKey('user.id'))
        game_id = Column(Integer, ForeignKey('game.id'))
        # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
        game = relationship(
            'Game',
            backref=backref('games',
                            uselist=True,
                            cascade='delete,all'))
        answers = relationship(
            'Answer',
            backref=backref('answer',
                            uselist=True,
                            cascade='delete,all'))

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
            'Question',
            backref=backref('questions',
                            uselist=True,
                            cascade='delete,all'))

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        uid = Column(Integer, unique=True)
        name = Column(String, nullable=True)
        alias = Column(String, nullable=True)
        created_on = Column(DateTime, default=func.now())
        questions = relationship(
            'Question',
            backref=backref('user-questions',
                            uselist=True,
                            cascade='delete,all'))
        answers = relationship(
            'Answer',
            backref=backref('user-answers',
                            uselist=True,
                            cascade='delete,all'))
        games = relationship(
            'Game',
            backref=backref('user-games',
                            uselist=True,
                            cascade='delete,all'))
