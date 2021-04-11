# -*- coding: utf-8 -*-
"""
This is a detailed example using almost every command of the API
"""

import json
import time
import re
from sqlalchemy.sql.expression import null

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import is_string

from jerocat import Jerocat


import configparser
config = configparser.ConfigParser()
config.read('config.ini')


#from settings import TOKEN
TOKEN = config['telegram']["TOKEN"]
ORACULUS = config['telegram']["ORACULUS"]
ADMIN_PASSWORD = config['main']["password"]

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
    print("funció "+str(call))
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
    chat_id = m.chat.id
    p = j.play_get(chat_id)
    if (p == False):
        j.play_init(chat_id)
        p = j.play_get(chat_id)
    bot.send_message(chat_id, "Escull un joc",
                     reply_markup=games_choose_markup())


@bot.message_handler(commands=['status'])
def command_games(m):
    chat_id = m.chat.id
    play_show_status(chat_id)


@bot.message_handler(commands=['edit'])
def command_edit(m):
    chat_id = m.chat.id
    if m.json['chat']['type'] != "private":
        bot.reply_to(m, "Només es poden editar jocs per converses privades")
        return
    p = j.play_get(chat_id)
    p.status = Jerocat.STATUS_VALIDATING
    j.save()
    bot.send_message(chat_id, "Entra la contrasenya d'editor")

# exits editing mode


@bot.message_handler(commands=['logout'])
def command_help(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    j.logout(play)
    bot.send_message(chat_id, "Logged out")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    chat_id = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text)  # send the generated help page


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # check if we have a possible answer
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    if (play.status == Jerocat.STATUS_VALIDATING):
        login(m)

    else:
        if (play.status == Jerocat.STATUS_VALIDATED):  # Estem editant
            editing(m)

        else:
            if (m.text[:1].isdigit()):
                check_answer(m)


def split_answer(input):
    position = int(re.search(r'\d+', input).group())
    answer = input[len(str(position)):].strip(" .,;-_:")
    return position, answer

# show game status


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


def login(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)

    print("validant contrasenya...")
    if (m.text == ADMIN_PASSWORD):
        play.status = Jerocat.STATUS_VALIDATED
        j.save()
        bot.send_message(chat_id, "Contrasenya acceptada")
        bot.send_message(
            chat_id, "Activa un joc amb /games i introdueix un número per editar pregunta i resposta (0 per a inserir-ne una...)")
    else:
        play.status = Jerocat.STATUS_NOTHING
        j.save()
        bot.send_message(chat_id, "Contrasenya INCORRECTA")


def editing(m):
    print("editing...")
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    print(play.attributes)
    if (play.game.id > 0):  # editant i tenim joc acttivat
        print(type(play.attributes))
        if ("question" in play.attributes):  # tenim pregunta
            print("tenim pregunta marcada")
            question_edit(play)
            pass
        else:  # no tenim res, ho assumim com a pregunta
            print("no tenim pregunta activada")
            if (m.text.isdigit()):
                print("guardant quina pregunta volem editar")
                print("tenia: "+str(play.attributes))
                play = j.play_set_attribute(chat_id, "question", int(m.text))
                print("tinc: "+str(play.attributes))

    else:
        print("no tenim cap joc per editar")

# show edit dialog


def question_edit(play):
    chat_id = play.chat_id
    bot.send_message(chat_id, "Escull una resposta per esborrar, o tecleja'n una de nova",
                     reply_markup=answer_edit_markup(play))


def answer_edit_markup(play):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    question_order = play.attributes["question"]
    question = j.question_get(play.game, question_order)
    print("Pregunta: "+question.text)

    answers = question.answers
    for a in answers:
        buton_data = {
            "button_type": "answer_edit",
            "game_id": play.game.id,
            "answer_id": a.id, "confirmed": False}
        markup.add(InlineKeyboardButton(
            a.text, callback_data=json.dumps(buton_data)))
    buton_data = {"game_id": play.game.id, "answer_id": 0}
    markup.add(InlineKeyboardButton(
        "Cancel·la", callback_data=json.dumps(buton_data)))
    return markup


def check_answer(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    position, answer_text = split_answer(m.text)
    if (is_string(answer_text)):
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


bot.polling()
