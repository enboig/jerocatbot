from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#from settings import TOKEN
database=config['database']["file"]
Base = declarative_base()


class Jerocat:

    def __init__(self):
        print(database)
        self.engine = create_engine('sqlite:///'+database+'.sqlite')
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

    def game_add(self, name, user=None):
        '''
        Insert a empty game and returns its id
        '''
        g = self.Game(name=name,user=user)
        self.repo.add(g)
        self.repo.commit()
        return g

    def game_list(self, uid=0):
        """
        Returns a list of games. If a user is send, it also list user games
        TODO filter by user
        """
        return self.repo.query(self.Game).all()

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

    class Question(Base):
        __tablename__ = 'question'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        # Use default=func.now() to set the default hiring time
        # of an Employee to be the current time when an
        # Employee record was created
        created_on = Column(DateTime, default=func.now())
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
        # questions = relationship(
        #     'Question',
        #     backref=backref('questions',
        #                     uselist=True,
        #                     cascade='delete,all'))
        # answers = relationship(
        #     'Answer',
        #     backref=backref('answers',
        #                     uselist=True,
        #                     cascade='delete,all'))
        # games = relationship(
        #     'Game',
        #     backref=backref('games',
        #                     uselist=True,
        #                     cascade='delete,all'))


if __name__ == '__main__':
    print("inici")
    j = Jerocat()

    # creem usuaris
    u1 = j.user_add(uid=1234, name="player1")
    u2 = j.user_add(uid=5678, alias="player2")

    # creem dos jocs
    g1 = j.game_add(name="Primer Joc",user=u1)
    g2 = j.game_add(name="Segon Joc", user=u2)

    print(g1.user.name)

    # Els hi posem preguntes
    q1 = j.question_add(game=g1, question="Pregunta q1 per a g1")
    q2 = j.question_add(game=g1, question="Pregunta q2 per a g1")
    q3 = j.question_add(game=g1, question="Pregunta q3 per a g1")
    q4 = j.question_add(game=g2, question="Pregunta q4 per a g2")
    q5 = j.question_add(game=g2, question="Pregunta q5 per a g2")

    # Els hi posem respostes
    a1 = j.answer_add(question=q1, answer="Resposta a1 per a q1")
    a2 = j.answer_add(question=q1, answer="Resposta a2 per a q1")
    a3 = j.answer_add(question=q2, answer="Resposta a3 per a q1")
    a4 = j.answer_add(question=q2, answer="Resposta a4 per a q2")
    a5 = j.answer_add(question=q2, answer="Resposta a5 per a q2")
    a6 = j.answer_add(question=q4, answer="Resposta a5 per a q4")
    a7 = j.answer_add(question=q5, answer="Resposta a5 per a q5")

    gs = j.game_list()
    for g in gs:
        print(str(g.name))
        for q in g.questions:
            print("q:"+str(q.name))
            for a in q.answers:
                print("a:"+str(a.name))
