# -*- coding: utf-8 -*-
"""
This is a detailed example using almost every command of the API
"""

import time
#from question import Question
import re
from sqlalchemy.sql.expression import null

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import is_string

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#from threading import Thread

from jerocat import Jerocat


import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# from settings import TOKEN
TOKEN = config['telegram']["TOKEN"]
ORACULUS = config['telegram']["ORACULUS"]
ADMIN_PASSWORD = config['main']["password"]
# telebot.apihelper.READ_TIMEOUT = 5
MAIL_USER = config['mail']["user"]
MAIL_PASSWORD = config['mail']["passowrd"]
MAIL_ADMIN = config['mail']["admin"]

j = Jerocat()

commands = {  # command description used in the "help" command
    'games': 'Llista de jocs disponibles per activar',
    'status': 'Mostra com està la partida, i quins jeroglífics ja han sigut resoltrs',
}

commands_private = {  # command description used in the "help" command
    'games': 'Llista de jocs disponibles per activar',
    'login': 'Entra en mode editor',
    'logout': 'Surt del mode editor'
}

# https://github.com/eternnoir/pyTelegramBotAPI/issues/880
bot = telebot.TeleBot(TOKEN)
#bot = telebot.TeleBot(TOKEN, threaded=False)

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


@bot.message_handler(commands=['login'])
def command_login(m):
    chat_id = m.chat.id
    if m.json['chat']['type'] != "private":
        reply_to(m, "Només es poden editar jocs per converses privades")
        return
    p = j.play_get(chat_id)
    if p.get("editing", False) != True:
        p.status = Jerocat.STATUS_VALIDATING
        j.save()
        send_message(chat_id, "Entra la contrasenya d'editor",
                     disable_notification=True)
    else:
        questions_edit_menu(chat_id)
# exits editing mode


@bot.message_handler(commands=['logout'])
def command_logout(m):
    chat_id = m.chat.id
    play = j.play_get(chat_id)
    play.attributes = {}
    play.status = j.STATUS_NOTHING
    play.game = None
    j.save()
    send_message(chat_id, "Logged out", disable_notification=True)


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    chat_id = m.chat.id
    help_text = "Escull una comanda: \n"
    if m.chat.type == "private":
        for key in commands_private:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands_private[key] + "\n"
    else:
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
    send_message(chat_id, help_text, disable_notification=True)

# Downloads a ODS file with all games


@bot.message_handler(commands=['export'])
def command_help(m):
    chat_id = m.chat.id
    export_ods(m)


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
    ok = False
    try:
        if p.status == j.STATUS_GAMES_MENU:
            ok = game_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_QUESTIONS:
            ok = questions_edit_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_ANSWERS:
            ok = answers_edit_menu_response(p, call)
        elif p.status == j.STATUS_EDITING_QUESTION_TEXT:
            question_delete_menu_response(play=p, call=call)
        else:
            print("Unknown command")
            print("p.status:"+str(p.status))
            print("call:"+str(call))
        if ok == False:
            # mostrem de nou el menú esperat
            pass

    except Exception as e:
        print("Except callback_query_handler")
        print(e)


@bot.message_handler(func=lambda message: True, content_types=['text', 'document'])
def command_default(m):
    '''
    Default handler for messages. It includes:
    * Text for adding/editing, dependending on play.STATUS
    * Text for answers if a game is active
    '''
    chat_id = m.chat.id
    if m.content_type == "text":
        # check if we have a possible answer
        play = j.play_get(chat_id)
        if play.get("editing", False) == True:
            if (play.status == Jerocat.STATUS_VALIDATED):  # Estem editant
                # editing(m)
                pass
            elif (play.status == Jerocat.STATUS_GAMES_MENU):
                j.game_add(fix_chars(m.text))
                games_menu(chat_id)

            elif (play.status == Jerocat.STATUS_EDITING_QUESTION_TEXT):
                j.question_update(play.get('question_id'), m.text)
                play.status = j.STATUS_EDITING_QUESTIONS
                play.unset("question_id")
                j.save()
                questions_edit_menu(play.chat_id)

            elif (play.status == Jerocat.STATUS_EDITING_ANSWERS):
                # assuming new answer
                question = j.question_get(id=play.get('question_id'))
                j.answer_add(question, m.text)
                answer_edit_menu(chat_id, question)
            elif (play.status == j.STATUS_EDITING_QUESTIONS):
                # Adding a aquestion
                j.question_add(play.game, m.text.strip())
                questions_edit_menu(play.chat_id)
        if (play.status == Jerocat.STATUS_VALIDATING):
            login(m)
        else:
            if (play.game != None and m.text[:1].isdigit()):
                check_answer(m)

    elif m.content_type == "document":
        import_ods(m)
        pass
    else:
        send_message(chat_id, "Només puc importar fitxers .ODS")
        pass


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
        send_message(chat_id, "No hi ha cap joc actiu",
                     disable_notification=True)
    else:
        message = g.name+"\n"
        for q in g.questions:
            message += str(q.position) + ". "
            point = j.points_get(p, q)
            if (point != None):
                message += '"'+point.answer.text+'":  '
            message += q.text
            message += "\n"
        rank = j.play_get_ranking(p)
        if (len(rank) > 0):
            message += "\nRanking:\n"
            for uid, points in rank.items():
                u = j.user_get(uid)
                message += str(points) + " -> " + ((u.first_name+" "+u.last_name)
                                                   if len(u.first_name+u.last_name) else u.username)+"\n"
        send_message(chat_id, message, disable_notification=True)


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
        play.set('editing', True)
        j.save()
        bot.delete_message(m.chat.id, m.message_id)
        send_message(chat_id, "Contrasenya acceptada",
                     disable_notification=True)
        send_message(
            chat_id, "Activa un joc amb /games i introdueix un número per editar pregunta i resposta (0 per a inserir-ne una...)",
            disable_notification=True)
    else:
        play.status = Jerocat.STATUS_NOTHING
        j.save()
        bot.delete_message(m.chat.id, m.message_id)
        send_message(chat_id, "Contrasenya INCORRECTA",
                     disable_notification=True)
        mail_send(
            "", "Hi ha hagut un intent fallit d'entrar al gestor del JeroCatBot!\n"+str(m))


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
    markup.add(InlineKeyboardButton("Cancel·la", callback_data="0"),
               InlineKeyboardButton("Esborra el joc", callback_data="gd"))

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


# show edit dialog for answers


def answer_edit_menu(chat_id, question):
    send_message(chat_id, "Editant respostes de: "+question.text+"\n"
                 + "Escull una resposta per editar, o escriu-ne un de nova",
                 reply_markup=answers_edit_markup(question), disable_notification=True)


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
        q = None
        param = (call.data).split("_")
        if param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(play.chat_id, q)
        elif param[0] == "qad":  # deleting answer
            q = j.question_get(id=int(play.get("question_id")))
            j.answer_delete(param[1])
            send_message(play.chat_id, "S'ha esborrat la resposta",
                         disable_notification=True)

            answer_edit_menu(play.chat_id, q)

        elif param[0] == "0":  # cancel
            if play.get("editing") == True:
                play.status = Jerocat.STATUS_EDITING_QUESTIONS
                j.save()
                questions_edit_menu(play.chat_id)
        else:
            send_message(play.chat_id, "Opció incorrecta",
                         disable_notification=True)
            return False
    except Exception as e:
        print("def answers_edit_menu_response(play,call):")
        print(e)

    pass

# question delete


def question_edit_message(chat_id, question):
    send_message(chat_id, "Reescriu la pregunta, o prem per esborrar",
                 reply_markup=question_delete_markup(chat_id, question), disable_notification=True)


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
            send_message(ORACULUS, help_112)


def menu_cancel(play, call):
    if play.status == j.STATUS_EDITING_QUESTION_TEXT:
        play.unset("question_id")
        play.status
        j.save()


def questions_edit_menu(chat_id):
    p = j.play_get(chat_id)
    send_message(chat_id, "Escull pregunta per editar, o tecleja'n una de nova",
                 reply_markup=question_edit_markup(p), disable_notification=True)


def games_menu(chat_id):
    p = j.play_get(chat_id)
    p.status = j.STATUS_GAMES_MENU
    p.unset("question_id")
    j.save()
    send_message(chat_id, "Escull un joc",
                 reply_markup=games_menu_markup(), disable_notification=True)
    if p.get("editing", False) == True:
        send_message(chat_id, "O escriu el nom d'un joc per afegir-lo")


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
            answer_callback_query(play.chat_id, "El joc no existeix!")
            return

        send_message(play.chat_id, "Has escollit " +
                     g.name, disable_notification=True)

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
        send_message(play.chat_id, "Opció incorrecta",
                     disable_notification=True)
        return False


def questions_edit_menu_response(play, call):
    '''
    Response to questions+answers edit menu
    '''
    try:
        param = (call.data).split("_")
        if param[0] == "qe":  # estem passant una pregunta a editar
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_QUESTION_TEXT
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            question_edit_message(play.chat_id, q)
        elif param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(play.chat_id, q)
        elif param[0] == "0":  # Cancel
            play.status = Jerocat.STATUS_VALIDATED
            j.save()
            # TODO estem cancel·lant l'edició d'una resposta
            games_menu(play.chat_id)
        elif param[0] == "gd":  # Esborrant un joc!!!!
            print("Esborraré un joc!!!!")
            if j.game_delete(play.game.id):
                send_message(play.chat_id, "Joc esborrat")
                games_menu(play.chat_id)
            else:
                send_message(play.chat_id, "Només esborraré jocs buits")
                questions_edit_menu(play.chat_id)
            pass
        else:
            answer_callback_query(play.chat_id, "Opció incorrecta")
            return False
    except Exception as e:
        print("Except questions_edit_menu_response")
        print(e)


def question_delete_menu_response(play, call):
    '''
    Response to delete question menu and "cancel editing question text"
    '''
    try:
        param = (call.data).split("_")
        if param[0] == "qd":  # estem passant una pregunta a esborrar
            if int(param[1]) > 0:
                j.question_delete(id=int(param[1]))

            play.status = j.STATUS_EDITING_QUESTIONS
            play.unset("question_id")
            send_message(
                play.chat_id, "Pregunta esborrada, amb les seves respostes i puntucacions.")
            j.save()
            questions_edit_menu(play.chat_id)

        else:
            answer_callback_query(play.chat_id, "Opció incorrecta")
            return False

    except Exception as e:
        print("except: def question_delete_menu_response(play, call):")
        print(e)


def mail_send(to, mail_content):
    # The mail addresses and password
    sender_address = MAIL_USER
    sender_pass = MAIL_PASSWORD
    receiver_address = 'enboig@gmail.com'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = to
    # The subject line
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def send_message(chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None, timeout=None):
    '''
    Wrapper to fix timeout problems:
    https://github.com/eternnoir/pyTelegramBotAPI/issues/880
    '''
    retries = 5
    while retries > 0:
        try:
            bot.send_message(chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup,
                             parse_mode, disable_notification, timeout)
            retries = 0
        except:
            print("except: send_message "+str(retries))
            time.sleep(1)
        retries -= 1


def reply_to(message, text, **kwargs):
    '''
    Wrapper to fix timeout problems:
    https://github.com/eternnoir/pyTelegramBotAPI/issues/880
    '''
    retries = 5
    while retries > 0:
        try:

            bot.reply_to(message, text, **kwargs)
            retries = 0
        except:
            print("except: reply_to "+str(retries))
            time.sleep(1)
        retries -= 1


def answer_callback_query(callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    '''
    Wrapper to fix timeout problems:
    https://github.com/eternnoir/pyTelegramBotAPI/issues/880
    '''
    retries = 5
    while retries > 0:
        try:
            bot.answer_callback_query(
                callback_query_id, text, show_alert, url, cache_time)
            retries = 0
        except Exception as e:
            print("except: answer_callback_query "+str(retries))
            time.sleep(1)
        retries -= 1


def delete_message(self, chat_id, message_id, timeout=None):
    '''
    Wrapper to fix timeout problems:
    https://github.com/eternnoir/pyTelegramBotAPI/issues/880
    '''
    retries = 5
    while retries > 0:
        try:
            bot.delete_message(self, chat_id, message_id, timeout)
            retries = 0
        except:
            print("except: delete_message "+str(retries))
            time.sleep(1)
        retries -= 1


def export_ods(m):
    # help page
    chat_id = m.chat.id
    from pyexcel_ods import save_data
    from collections import OrderedDict
    import tempfile
    import os
    data = OrderedDict()  # from collections import OrderedDict

    gs = j.game_list_full()
    for g in gs:
        rows = []
        for q in g.questions:
            row = [q.text]
            for a in q.answers:
                row.append(a.text)
            rows.append(row)
        data.update({g.name: rows})
    file = tempfile.NamedTemporaryFile(suffix='.ods', delete=False)

    save_data(file.name, data)
    doc = open(file.name, 'rb')

    retries = 3
    while retries > 0:
        try:
            bot.send_document(chat_id, doc, caption="export.ods")
            doc.close()
            try:
                os.remove(file.name)
            except:
                pass
            retires = 0
        except:
            time.sleep(1)
            retires -= 1


def import_ods(m):
    from pyexcel_ods import get_data
    import pyexcel as pe
    import requests
    import tempfile
    import os

    chat_id = m.chat.id
    if m.json['chat']['type'] != "private":
        reply_to(m, "Només es poden importar jocs per converses privades")
        return
    # p = j.play_get(chat_id)
    # if p.status not in (j.STATUS_GAME_EDIT):
    #     reply_to(m, "Has d'estar validat per poder importar jocs")
    #     return

    if m.document.mime_type != "application/vnd.oasis.opendocument.spreadsheet":
        reply_to(m, "Només puc importar fitxers .ods")
        return

    file_info = bot.get_file(m.document.file_id)
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.ods', mode='w+b', delete=False)
    file = requests.get(
        'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
    temp_file.write(file.content)
    temp_file.write(b' ')
    temp_file.close()

    u1 = j.user_get(m.from_user.id)

    book = pe.get_book(file_name=temp_file.name)
    for sheet in book:
        if (sheet.name != "Helper"):
            q_counter = 0
            a_counter = 0
            q_new = 0
            a_new = 0
            g = j.game_get(name=fix_chars(sheet.name))
            if g == None:
                g = j.game_add(name=fix_chars(sheet.name), user=u1,
                               status=j.STATUS_PUBLIC)
                pass
            send_message(chat_id, "Processant: "+str(g.name),
                         disable_notification=True)
            for row in sheet:
                q = None
                first = True
                for cell in row:
                    if first:
                        q = j.question_get(
                            g, text=fix_chars(str(cell).strip()))
                        if q == None:
                            q = j.question_add(
                                game=g, question=fix_chars(str(cell).strip()))
                            q_new += 1
                        q_counter += 1
                        first = False
                    else:
                        if str(cell).strip() != "":
                            a = j.answer_get(
                                q, text=fix_chars(str(cell).strip()))
                            if a == None:
                                a = j.answer_add(
                                    question=q, answer=fix_chars(str(cell).strip()))
                                a_new += 1
                            a_counter += 1
            send_message(chat_id, "S'han processat "+str(q_counter) +
                         " preguntes i "+str(a_counter)+" respostes", disable_notification=True)
            send_message(chat_id, "S'han afegit "+str(q_new) +
                         " preguntes i "+str(a_new)+" respostes", disable_notification=True)
    try:
        os.remove(temp_file.name)
    except:
        pass


def fix_chars(string):
    '''
    Fixes some chars ODS files might replace
    '''
    print("original: "+str(string))
    old = ["’"]
    new = ["'"]

    for i in range(len(old)):
        string = string.replace(old[i], new[i])
    print("resultat: "+str(string))
    return string


# class Expirer(Thread):
#     '''
#     This class create a thread to delete expiring messages. It cas a method to add messages to the queue.
#     '''
#     queue = None
#     index = None
#     max_time = None
#     def __init__(self, max_time=10):
#         ''' Constructor. '''
#         Thread.__init__(self)
#         self.index = 0
#         self.queue = []
#         self.max_time = max_time
#         for i in range(max_time):
#             self.queue.append([])
#     def run(self):
#         while True:
#             time.sleep(1)
#             for m in self.queue[(self.index+1) % self.max_time]:
#                 try:
#                     bot.delete_message(m[0], m[1])
#                 except:
#                     pass  # message already deleted on selection
#             self.index = (self.index+1) % self.max_time
#     def add(self, chat_id, message_id):
#         self.queue[self.index].append((chat_id, message_id))


# expirer = Expirer()
# expirer.start()


bot.polling()
