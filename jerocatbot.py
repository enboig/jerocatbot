# -*- coding: utf-8 -*-
"""
This is a detailed example using almost every command of the API
"""

import time
import re
from sqlalchemy.sql.expression import null

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from jerocat import Jerocat


import configparser
config = configparser.ConfigParser()
config.read('config.ini')


#from settings import TOKEN
TOKEN = config['telegram']["TOKEN"]
ORACULUS = config['telegram']["ORACULUS"]

j = Jerocat()

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'games': 'Llista de jocs disponibles per activar',
    'punts': 'Mostra quants punts té cada usuari',
    'mostra': 'Mostra els jeroglífics (els solucionats amb la solució)',
    #    'getImage'    : 'A test using multi-stage messages, custom keyboard, and media sending'
}


# imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
#imageSelect.add('Mickey', 'Minnie')

# hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(" [" + str(m.chat.id) + "]: " + m.text)
            # print(str(m.from_user))


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


def games_choose_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    games = j.game_list_full()
    for g in games:
        markup.add(InlineKeyboardButton(g.name, callback_data=g.id))
    return markup

# handle the "/start" command


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    call_id = call_get_id(call)
    g = j.game_get(call.data)
    if (g == False):
        bot.answer_callback_query(call_id, "El joc no existeix!")
        return
    bot.answer_callback_query(call.id, "Has escollit "+g.name)
    p = j.play_get(call_id)
    j.play_set_game(p, g)
    play_show_status(call_id)


@bot.message_handler(commands=['games'])
def command_games(m):
    cid = m.chat.id
    p = j.play_get(cid)
    if (p == False):
        j.play_init(cid)
        p = j.play_get(cid)
    bot.send_message(cid, "Escull un joc", reply_markup=games_choose_markup())


@bot.message_handler(commands=['status'])
def command_games(m):
    chat_id = m.chat.id
    play_show_status(chat_id)


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        # save user id, so you could brodcast messages to all users of this bot later
        knownUsers.append(cid)
        # save user id and his current "command level", so he can use the "/getImage" command
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(
            cid, "I already know you, no need for me to scan you again!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your image now",
                     reply_markup=imageSelect)  # show the keyboard
    # set the user to the next step (expecting a reply in the listener now)
    userStep[cid] = 1

# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # check if we have a possible answer
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    if (m.text[:1].isdigit()):
        position, answer_text = split_answer(m.text)
        answer = j.answer_check(play.game, position, answer_text)
        question = j.question_from_position(play.game, position)
        if (answer != None):
            user = m.from_user
            j.point_add(play, user, question, answer)
            play_show_status(chat_id)
        else:
            # ask for human help....
            help_112 = "Joc: "+play.game.name+"\nPregunta: " + \
                question.text+"\nResposta: "+answer_text
            if (question.answers):
                help_112 += "\nAltres respostes:"
                for a in question.answers:
                    help_112 += "\n - "+a.text
            bot.send_message(ORACULUS, help_112)


def split_answer(input):
    position = int(re.search(r'\d+', input).group())
    answer = input[len(str(position)):].strip(" .,;-_:")
    return position, answer


def play_show_status(chat_id):
    p = j.play_get(chat_id)
    if (p == False):
        j.play_init(chat_id)
        p = j.play_get(chat_id)
    g = j.game_get(p.game_id)
    if (g == None):
        bot.send_message(chat_id, "No hi ha cap joc actiu")
    else:
        message = g.name+"\n"
        for q in g.questions:
            message += str(q.position) + ". "+q.text
            point = j.points_get(p, q)
            if (point != None):
                message += '"'+point.answer.text+'"'
            message += "\n"
        bot.send_message(chat_id, message)


def call_get_id(call):

    # id d'un missatge amb teclat rebut
    call_id = call.message.json["chat"]["id"]
    return call_id


bot.polling()
