from datetime import date
from time import sleep, time
from base import Session, engine, Base, metadata
from sqlalchemy import create_engine, select, MetaData, Table, and_

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
    STATUS_VALIDATED = 5
    STATUS_EDITING_QUESTIONS = 6
    STATUS_EDITING_ANSWERS = 7
    STATUS_EDITING_QUESTION_TEXT = 8
    STATUS_EDITING_ANSWER_TEXT = 9

    STATUS_GAMES_MENU = 10
    STATUS_GAME_EDIT = 11
    STATUS_GAME_PLAY = 12

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
        u = session.query(User).filter(
            User.id == user.id).first()
        if (u == None):
            u = User(id=user.id,
                     username=user.username,
                     first_name=user.first_name,
                     last_name=user.last_name)
            session.add(u)
        else:
            u.username = user.username
            u.first_name = user.first_name
            u.last_name = user.last_name

        session.commit()
        return u

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
        g = None
        if (id != None):
            g = session.query(Game).get(id)
        elif (name != None):
            g = session.query(Game).filter(Game.name == name).first()
        return g

    def game_delete(self, id=None):
        '''
        Delete a game if it has no questions
        '''
        g = session.query(Game).get(id)
        if (len(g.questions)) > 0:  # Game is not empty
            return False
        session.query(Game).filter(Game.id == int(id)).delete()
        session.commit()
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
        play.unset('pag')
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

    def question_get(self, game=None, position=None, text=None, id=None):
        if id != None:
            return session.query(Question).filter(Question.id == int(id)).first()
        elif position != None:
            return session.query(Question).filter(Question.game == game, Question.position == position).first()
        elif text != None:
            return session.query(Question).filter(Question.game == game, Question.text == text).first()

    def question_delete(self, game=None, position=None, text=None, id=None):
        if id != None:
            session.query(Question).filter(Question.id == int(id)).delete()
            session.query(Answer).filter(
                Answer.question_id == int(id)).delete()
            session.query(Point).filter(Point.question_id == int(id)).delete()
            session.commit()
            # q=session.query(Question).filter(Question.id == int(id)).first()
            # session.delete(q)
        elif position != None:
            pass
        elif text != None:
            pass
        # TODO: refer els índexs

    def question_update(self, id=None, text=None):
        q = self.question_get(id=id)
        q.text = text
        session.commit()

    def answer_add(self, question, answer):
        a = Answer(question=question, text=answer)
        session.add(a)
        session.commit()
        return a

    def answer_get(self, question, text):
        return session.query(Answer).filter(Answer.question == question, Answer.text == text).first()

    def answer_delete(self, id):
        if id != None:
            session.query(Answer).filter(Answer.id == int(id)).delete()
            session.query(Point).filter(Point.answer_id == int(id)).delete()
            session.commit()

    def numerize():
        """
        Set the questions numbers
        """
        pass

    def points_get(self, play, question):
        return session.query(Point).filter(Point.question_id == question.id, Point.play_id == play.id).order_by(Point.created_on).first()

    def question_from_position(self, game, position):
        return session.query(Question).filter(Question.game_id == game.id, Question.position == position).first()

    def point_add(self, play, user, question, answer):
        user = self.user_upsert(user)
        p = Point(play, user, question, answer)
        session.commit()

    def play_set_attribute(self, chat_id, attribute, value):
        p = session.query(Play).filter(Play.chat_id == chat_id).first()
        p.attributes[attribute] = value
        session.add(p)
        session.commit()
        return p

    def save(self):
        session.commit()

    # get answers from game_id and question_position
    def answers_list(self, game_id, question_position):
        question = session.query(Question).filter(
            Question.game_id == game_id, Question.position == question_position).first()
        list = {}
        for a in session.query(Answer).filter(Play.question_id == question.position).all():
            list[a.id] = a.text
        return list

    def play_get_ranking(self, play):
        '''
        Retuns a dictionari with player names/users and correct (first) answers
        '''
        checked = {}
        result = {}
#        for p, u in session.query(Point, User).filter(Point.user_id == User.id, Play.game == play.game, Point.play == play).order_by(Point.created_on):
        for p in session.query(Point).join(Game).join(User, Point.user).filter(Point.play == play, Point.game == play.game).order_by(Point.created_on):
            if checked.get(p.question_id) is None:
                result[p.user_id] = result.get(p.user_id, 0)+1
                checked[p.question_id] = True
        return result
