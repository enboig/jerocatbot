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
from telebot.util import is_string

from jerocat import Jerocat


import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# from settings import TOKEN
TOKEN = config['telegram']["TOKEN"]
ORACULUS = config['telegram']["ORACULUS"]
ADMIN_PASSWORD = config['main']["password"]
# telebot.apihelper.READ_TIMEOUT = 5

j = Jerocat()

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'games': 'Llista de jocs disponibles per activar',
    'punts': 'Mostra quants punts té cada usuari',
    'mostra': 'Mostra els jeroglífics (els solucionats amb la solució)',
    #    'getImage'    : 'A test using multi-stage messages, custom keyboard, and media sending'
}

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

'''
COMMANDS
'''


@bot.message_handler(commands=['games'])
def command_games(m):
    chat_id = m.chat.id
    p = j.play_get(chat_id)
    if (p == False):
        j.play_init(chat_id)
        p = j.play_get(chat_id)
    games_menu(chat_id)


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
    if p.attributes.get("editing", False) != True:
        p.status = Jerocat.STATUS_VALIDATING
        j.save()
        bot.send_message(chat_id, "Entra la contrasenya d'editor")
    else:
        questions_edit_menu(chat_id)
# exits editing mode


@bot.message_handler(commands=['logout'])
def command_help(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
#    j.logout(play)
    play.attributes = {}
    play.status = j.STATUS_NOTHING
    play.game = None

    j.save()  # TODO check if disabling this works

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


'''
MESSAGES HANDLERS
'''


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    '''
    Captures menu responses
    '''
    chat_id = call_get_id(call)
    p = j.play_get(chat_id)
    param = (call.data).split("_")

    try:
        if p.status == j.STATUS_GAMES_MENU:
            game_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_QUESTIONS:
            questions_edit_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_ANSWERS:
            answers_edit_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_QUESTION_TEXT:
            question_delete_menu_response(play=p, call=call)

        ########################################
        ##### OLD DEPRECATED ###################
        ########################################
        # bot.delete_message(
        #     call.message.json["chat"]["id"], call.message.message_id)
        # if param[0] == "g":
        #     g = j.game_get(param[1])
        #     if (g == False):
        #         bot.answer_callback_query(chat_id, "El joc no existeix!")
        #         return
        #     bot.answer_callback_query(call.id, "Has escollit "+g.name)

        #     j.play_set_game(p, g)
        #     if p.status == Jerocat.STATUS_VALIDATED:
        #         questions_edit_menu(chat_id)
        #     else:
        #         play_show_status(chat_id)
        # if param[0] == "qe":  # estem passant una pregunta a editar
        #     q = j.question_get(id=int(param[1]))
        #     p.status = Jerocat.STATUS_EDITING_QUESTIONS
        #     p.attributes["question_id"] = q.id
        #     j.save()
        #     # mostrem el menú per editar o esborrar la pregunta
        #     question_edit_message(chat_id, q)
        # if param[0] == "qd":  # estem esborrant una pregunta
        #     p.status = Jerocat.STATUS_VALIDATED
        #     p.attributes.pop("question_id")
        #     j.save()
        #     q = j.question_get(id=param[1])

        #     j.question_delete(id=param[1])
        #     j.save()
        #     # mostrem el menú informant de la pregunta esborrada
        #     bot.send_message(
        #         chat_id, "S'ha esborrat la pregunta "+str(q.position)+" "+str(q.text))
        # if param[0] == "qae":  # estem editant respostes....
        #     q = j.question_get(id=int(param[1]))
        #     p.status = Jerocat.STATUS_EDITING_ANSWERS
        #     p.attributes["question_id"] = q.id
        #     j.save()
        #     # mostrem el menú per editar o esborrar la pregunta
        #     answer_edit_menu(chat_id, q)
        # if param[0] == "0":
        #     menu_cancel(call)
        else:
            print("No sé quina comanda de menú he rebut?!?!?!?!?")
            print("p.status:"+(p.status))

    except:
        print("Except 98")
        pass  # message deleted while processing


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    '''
    Default handler for messages. It includes:
    * Text for adding/editing, dependending on play.STATUS
    * Text for answers if a game is active
    '''
    # check if we have a possible answer
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    if (play.status == Jerocat.STATUS_VALIDATING):
        login(m)
    elif (play.status == Jerocat.STATUS_VALIDATED):  # Estem editant
        # editing(m)
        pass

    elif (play.status == Jerocat.STATUS_EDITING_QUESTION_TEXT):
        j.question_update(play.attributes['question_id'], m.text)
        play.status = j.STATUS_EDITING_QUESTIONS
        play.unset("question_id")
        j.save()
        questions_edit_menu(play.chat_id)

    elif (play.status == Jerocat.STATUS_EDITING_ANSWERS):
        # assuming new answer
        question = j.question_get(id=play.attributes['question_id'])
        j.answer_add(question, m.text)
        answer_edit_menu(chat_id, question)
    elif (play.status == j.STATUS_EDITING_QUESTIONS):
        # Adding a aquestion
        j.question_add(play.game, m.text.strip())
        questions_edit_menu(play.chat_id)

    else:
        if (m.text[:1].isdigit()):
            check_answer(m)


def split_answer(input):
    '''
    Splits a message in question_order and answer_text
    '''
    question_order = int(re.search(r'\d+', input).group())
    answer_text = input[len(str(question_order)):].strip(" .,;-_:")
    return question_order, answer_text

# show game status


def play_show_status(chat_id):
    '''
    Print game status:
    * All the questions and typed answers
    * Stats of player answers (TODO)
    '''
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
    '''
    Helper to get chat_id from a message
    '''
    chat_id = call.message.json["chat"]["id"]
    return chat_id


def login(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    if (m.text == ADMIN_PASSWORD):
        play.attributes['editing'] = True
        j.save()
        bot.delete_message(m.chat.id, m.message_id)
        bot.send_message(chat_id, "Contrasenya acceptada")
        bot.send_message(
            chat_id, "Activa un joc amb /games i introdueix un número per editar pregunta i resposta (0 per a inserir-ne una...)")
    else:
        play.status = Jerocat.STATUS_NOTHING
        j.save()
        bot.delete_message(m.chat.id, m.message_id)
        bot.send_message(chat_id, "Contrasenya INCORRECTA")


# generates questions markup for edit
def question_edit_markup(play):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    game = j.game_get(id=play.game.id)
    for q in game.questions:
        # question button
        buton_q = "qe_" + str(q.id)
        # answer button
        buton_a = "qae_" + str(q.id)
        answers_txt = "+++ add answer +++"
        if len(q.answers):
            answers_txt = ""
            for a in q.answers:
                answers_txt += a.text+", "

            answers_txt = answers_txt[:-2]
        markup.add(InlineKeyboardButton(q.text, callback_data=buton_q),
                   InlineKeyboardButton(answers_txt, callback_data=buton_a))

    # buton_data = {"game_id": play.game.id, "question_id": 0}
    # markup.add(InlineKeyboardButton(
    #     "Add", callback_data=json.dumps(buton_data)))
    return markup


def editing(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    if (play.game.id > 0):  # editant i tenim joc acttivat
        if ("question" in play.attributes):  # tenim pregunta
            answer_edit_menu(play)
            pass
        else:  # no tenim res, ho assumim com a pregunta nova
            bot.delete_message(m.chat.id, m.message_id)
            j.question_add(play.game, m.text)
            questions_edit_menu(chat_id)

    else:
        print("no tenim cap joc per editar")

# show edit dialog for answers


def answer_edit_menu(chat_id, question):
    bot.send_message(chat_id, "Editant respostes de "+question.text,
                     reply_markup=answers_edit_markup(question))
    bot.send_message(
        chat_id, "Escull una resposta per editar, o escriu-ne un de nova")


def answers_edit_markup(question):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    answers = question.answers
    for a in answers:
        markup.add(InlineKeyboardButton(
            a.text, callback_data="qad_"+str(a.id)))
    markup.add(InlineKeyboardButton(
        "Cancel·la", callback_data="0"))
    return markup


def answers_edit_menu_response(play, call):
    '''
    Response to questions+answers edit menu
    '''
    try:
        param = (call.data).split("_")
        if param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.attributes.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(play.chat_id, q)
        elif param[0] == "qad":  # deleting answer
            q = j.question_get(id=int(play.get("question_id")))
            j.answer_delete(param[1])
            answer_edit_menu(play.chat_id, q)

        elif param[0] == "0":  # cancel
            if play.get("editing") == True:
                play.status = Jerocat.STATUS_EDITING_QUESTIONS
                j.save()
                questions_edit_menu(play.chat_id)
            else:
                # never shouls happen
                play.status = Jerocat.STATUS_GAME_PLAY
                j.save()
                play_show_status(play.chat_id)
            pass
    except:
        print("def answers_edit_menu_response(play,call):")

    pass

# question delete


def question_edit_message(chat_id, question):
    bot.send_message(chat_id, "Reescriu la pregunta, o prem per esborrar",
                     reply_markup=question_delete_markup(chat_id, question))


def question_delete_markup(chat_id, question):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "Esborra: "+str(question.text), callback_data="qd_"+str(question.id)))
    markup.add(InlineKeyboardButton(
        "Cancel·la", callback_data="qd_0"))
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


def menu_cancel(play, call):
    if play.status == j.STATUS_EDITING_QUESTION_TEXT:
        play.unset("question_id")
        play.status
        j.save()
    # chat_id = call_get_id(m)
    # play = j.play_get(chat_id)
    # print("cancel·lant:")
    # print(" play.status:"+str(play.status)+" attributes:"+str(play.attributes))
    # if play.status == Jerocat.STATUS_EDITING_ANSWERS:
    #     question = j.question_get(play.attributes['question_id'])
    #     play.status = Jerocat.STATUS_EDITING_QUESTIONS
    #     j.save()
    #     question_edit_message(chat_id, question)
    # elif play.status == Jerocat.STATUS_EDITING_QUESTIONS:
    #     # TODO
    #     pass


def questions_edit_menu(chat_id):
    p = j.play_get(chat_id)
    bot.send_message(chat_id, "Escull pregunta per editar, o tecleja'n una de nova",
                     reply_markup=question_edit_markup(p))


def games_menu(chat_id):
    p = j.play_get(chat_id)
    p.status = j.STATUS_GAMES_MENU
    p.unset("question_id")
    j.save()
    m = bot.send_message(chat_id, "Escull un joc",
                         reply_markup=games_menu_markup(), disable_notification=True)
    time.sleep(10)
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except:
        pass  # message already deleted on selection


def games_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    games = j.game_list_full()
    for g in games:
        markup.add(InlineKeyboardButton(g.name, callback_data="g_"+str(g.id)))
    return markup


def game_menu_response(play, call):
    '''
    Response to game menu. It will delete the game, check if game ok and show status or game menu again
    '''

    param = (call.data).split("_")
    if param[0] == "g":
        g = j.game_get(param[1])
        if (g == False):
            bot.answer_callback_query(play.chat_id, "El joc no existeix!")
            return

        bot.send_message(play.chat_id, "Has escollit " + g.name)

        try:
            bot.delete_message(
                call.message.json["chat"]["id"], call.message.message_id)
        except:
            print("Borrant missatge que no existeix")

        j.play_set_game(play, g)
        if play.get("editing") == True:
            play.status = Jerocat.STATUS_EDITING_QUESTIONS
            j.save()
            questions_edit_menu(play.chat_id)
        else:
            play.status = Jerocat.STATUS_GAME_PLAY
            j.save()
            play_show_status(play.chat_id)
    else:
        bot.send_message(play.chat_id, "Opció incorrecta")


def questions_edit_menu_response(play, call):
    '''
    Response to questions+answers edit menu
    '''
    try:
        param = (call.data).split("_")
        if param[0] == "qe":  # estem passant una pregunta a editar
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_QUESTION_TEXT
            play.attributes["question_id"] = q.id
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            question_edit_message(play.chat_id, q)
        elif param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.attributes["question_id"] = q.id
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(play.chat_id, q)
        elif param[0] == "0":  # Cancel
            # TODO estem cancel·lant l'edició d'una resposta
            pass
        else:
            bot.answer_callback_query(play.chat_id, "Opció incorrecta")
    except:
        print("Except 964364")
        pass


def question_delete_menu_response(play, call):
    '''
    Response to delete question menu and "cancel editing question text"
    '''
    try:
        param = (call.data).split("_")
        if param[0] == "qd":  # estem passant una pregunta a esborrar
            clear_menus(play)

            if param[1] > 0:
                j.question_delete(param[1])

            play.status = j.STATUS_EDITING_QUESTIONS
            play.unset("question_id")
            j.save()

    except:
        print("except: def question_delete_menu_response(play, call):")


def clear_menus(play):
    '''
    Deletes previous menus stored
    '''
    while True:
        m_id = play.menu_pop()
        if m_id != None:
            try:
                bot.delete_message(play.chat_id, m_id)
            except:
                pass
        else:
            break
    j.save()


bot.polling()
