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
    STATUS_NOTHING = 0
    STATUS_PUBLIC = 1
    STATUS_PRIVATE = 2
    STATUS_PENDING = 3
    STATUS_VALIDATING = 4

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
        return ans

    def user_add(self, id, username=None):
        '''
        Insert a user
        '''
        u = User(id=id, username=username)
        session.add(u)
        session.commit()
        return u

    def user_upsert(self, user):
        new_user = session.query(User).filter(
            User.id == user.id).first()
        if (new_user == None):
            new_user = User(id=user.id, username=user.username)
            session.add(new_user)
        else:
            new_user.username = user.username

        session.commit()
        return new_user

    def user_get(self, id=False, username=False):
        user = None
        if (id != False):
            user = session.query(User).filter(User.id == id).first()
        elif (username != False):
            user = session.query(User).filter(
                User.username == username).first()
        return user

    def game_add(self, name, user=None, status=0):
        '''
        Insert a empty game and returns its id
        '''
        g = Game(name=name, user=user)
        session.add(g)
        session.commit()
        return g

    def game_get(self, id=None, user=None, name=None):
        '''
        Insert a empty game and returns its id
        '''
        print("id: " + str(id))
        g = None
        if (id != None):
            g = session.query(Game).get(id)
        elif (name != None):
            g = session.query(Game).filter(Game.name == name).first()
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
        try:
            p = session.query(Play).filter(Play.chat_id == chat_id).first()
        finally:
            if (p == None):
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

    def question_get(self, game, position=None, text=None):
        if position != None:
            return session.query(Question).filter(Question.game == game, Question.position == position).first()
        elif text != None:
            return session.query(Question).filter(Question.game == game, Question.text == text).first()

    def answer_add(self, question, answer):
        a = Answer(question=question, text=answer)
        session.add(a)
        session.commit()
        return a

    def answer_get(self, question, text):
        return session.query(Answer).filter(Answer.question == question, Answer.text == text).first()

    def numerize():
        """
        Set the questions numbers
        """
        pass

    def points_get(self, play, question):
        return session.query(Point).filter(Point.question_id == question.id, Point.play_id == play.id).first()

    def question_from_position(self, game, position):
        return session.query(Question).filter(Question.game_id == game.id, Question.position == position).first()

    def point_add(self, play, user, question, answer):
        user = self.user_upsert(user)
        p = Point(play, user, question, answer)
        session.commit()
