from datetime import date
from base import Session, engine, Base

import configparser

from answer import Answer
from game import Game
from play import Play
from point import Point
from question import Question
from user import User

config = configparser.ConfigParser()
config.read('config.ini')

Base.metadata.create_all(engine)
session = Session()


class Jerocat:
    # Game status
    STATUS_PUBLIC = 1
    STATUS_PRIVATE = 2
    STATUS_PENDING = 3

    def __init__(self):
        # if (config['database']["engine"] == "sqlite"):
        #     self.engine = create_engine(
        #         'sqlite:///'+config['database']["database"]+'.sqlite')
        #     self.session = sessionmaker()
        #     self.session.configure(bind=self.engine)
        #     #Base = declarative_base()
        #     print("create all!")
        #     Base.metadata.create_all(self.engine)
        # session = self.session()
        pass

    def answer_check(self, game, position, answer):
        """
        Checks if an answer is correct
        """
        q = session.query(Question).filter(
            Question.game == game, Question.position == position).first()
        ans = session.query(Answer).filter(
            Answer.question == q, Answer.text.ilike(answer)).first()
        return ans != None

    def user_add(self, uid, name=None, alias=None):
        '''
        Insert a user
        '''
        u = User(uid=uid, name=name, alias=alias)
        session.add(u)
        session.commit()
        return u

    def game_add(self, name, user=None, status=0):
        '''
        Insert a empty game and returns its id
        '''
        g = Game(name=name, user=user)
        session.add(g)
        session.commit()
        return g

    def game_get(self, id, user=None):
        '''
        Insert a empty game and returns its id
        '''
        g = session.query(Game).get(id)
        return g

    def play_init(self, chat_id):
        p = Play(chat_id=chat_id)
        session.add(p)
        session.commit()
        return p

    def play_get(self, chat_id):
        '''
        Returns the play
        '''
#        s = session.query(Play).get(chat_id=chat_id)
        print("buscant la sessió "+str(chat_id))
        try:
            p = session.query(Play).filter(Play.chat_id == chat_id).first()
        except:
            p = Play(chat_id=chat_id)
            session.add(p)
            session.commit()
        return p

    def play_set_game(self, play, game):
        play.game = game
        session.commit()

    def game_list_full(self, uid=0):
        """
        Returns a list of games. If a user is send, it also list user games
        TODO filter by user
        """
        games = session.query(Game).all()
        return games

    def game_list(self, uid=0):
        """
        Returns a list of games. If a user is send, it also list user games
        TODO filter by user
        """
        list = {}
        for g in session.query(Game).all():
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
        q = Question(game=game, text=question)
        session.add(q)
        session.commit()
        position = session.query(Question).filter(
            Question.game == q.game).filter(Question.id <= q.id).count()
        setattr(q, 'position', position)
        session.commit()
        return q

    def question_get(self, game, position):
        return session.query(Question).filter(Question.game == game, Question.position == position).first()

    def answer_add(self, question, answer):
        a = Answer(question=question, text=answer)
        session.add(a)
        session.commit()
        return a

    def numerize():
        """
        Set the questions numbers
        """
        pass

    def points_get(self, play, question):
        return session.query(Point).filter(Point.question_id == question.id, Point.play_id == play.id).first()
