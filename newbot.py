# -*- coding: utf-8 -*-
#!/usr/bin/env python
# pylint: disable=C0116

from jerocat import Jerocat
import logging
import re
# import time

from telegram import Update, ForceReply,  InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# from settings import TOKEN
TOKEN = config['telegram']["TOKEN2"]
ORACULUS = config['telegram']["ORACULUS"]
ADMIN_PASSWORD = config['main']["password"]


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

j = Jerocat()

# # Define a few command handlers. These usually take the two arguments update and
# # context.
# def start(update: Update, _: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )


def games_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    p = j.play_get(chat_id)
    if (p == False):
        j.play_init(chat_id)
        p = j.play_get(chat_id)
    games_menu(update, context)


def status_command(update, context):
    play_show_status(update, context)


def login_command(update, context):
    chat_id = update.message.chat.id
    if update.message.chat.type != "private":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Només es poden editar jocs per converses privades")
        return
    p = j.play_get(chat_id)
    if p.get("editing", False) != True:
        p.status = Jerocat.STATUS_VALIDATING
        j.save()
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Entra la contrasenya d'editor")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ja estàs validat")


def logout_command(update, context):
    play = j.play_get(update.effective_chat.id)
    play.attributes = {}
    play.status = j.STATUS_NOTHING
    play.game = None
    j.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Logged out")


def help_command(update, context):

    commands = {  # command description used in the "help" command
        'games': 'Llista de jocs disponibles per activar',
        'status': 'Mostra com està la partida, i quins jeroglífics ja han sigut resoltrs',
    }

    commands_private = {  # command description used in the "help" command
        'games': 'Llista de jocs disponibles per activar',
        'login': 'Entra en mode editor',
        'logout': 'Surt del mode editor'
    }

    help_text = "Escull una comanda: \n"
    if update.message.chat.type == "private":
        for key in commands_private:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands_private[key] + "\n"
    else:
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def export_command(update, context):
    p = j.play_get(update.effective_chat.id)
    if p.get('editing', False) == False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Has d'estar validat per poder exportar jocs")
        return

    export_ods(update, context)


def button(update: Update, context: CallbackContext) -> None:
    '''
    Captures menu responses
    '''
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # query.edit_message_text(text=f"Selected option: {query.data}")
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    p = j.play_get(chat_id)
    param = (query.data).split("_")
    ok = False
    try:
        if param[0] == "aa":
            answer_accept(update=update, context=context)
        elif param[0] == "ad":
            answer_forget(update=update, context=context)
        elif p.status == j.STATUS_GAMES_MENU:
            ok = game_menu_response(p, update, context)
        elif p.status == j.STATUS_EDITING_QUESTIONS:
            ok = questions_edit_menu_response(p, update, context)
        elif p.status == j.STATUS_EDITING_ANSWERS:
            ok = answers_edit_menu_response(p, update, context)
        elif p.status == j.STATUS_EDITING_QUESTION_TEXT:
            question_delete_menu_response(
                play=p, update=update, context=context)
        else:
            print("Unknown command")
            print("p.status:"+str(p.status))
            print("call:"+str(update))
        if ok == False:
            # mostrem de nou el menú esperat
            pass

    except Exception as e:
        print("Except callback_query_handler")
        print(e)
    context.bot.deleteMessage(chat_id, message_id)


def process_text(update, context):
    '''
    Default handler for messages. It includes:
    * Text for adding/editing, dependending on play.STATUS
    * Text for answers if a game is active
    '''
    chat_id = update.effective_chat.id
    # check if we have a possible answer
    play = j.play_get(chat_id)
    if play.get("editing", False) == True:
        if (play.status == Jerocat.STATUS_VALIDATED):  # Estem editant
            # editing(m)
            pass
        elif (play.status == Jerocat.STATUS_GAMES_MENU):
            j.game_add(fix_chars(update.message.text))
            games_menu(update, context)

        elif (play.status == Jerocat.STATUS_EDITING_QUESTION_TEXT):
            j.question_update(play.get('question_id'), update.message.text)
            play.status = j.STATUS_EDITING_QUESTIONS
            play.unset("question_id")
            j.save()
            questions_edit_menu(update, context)

        elif (play.status == Jerocat.STATUS_EDITING_ANSWERS):
            # assuming new answer
            question = j.question_get(id=play.get('question_id'))
            j.answer_add(question, update.message.text)
            answer_edit_menu(question, update, context)
        elif (play.status == j.STATUS_EDITING_QUESTIONS):
            # Adding a aquestion
            j.question_add(play.game, update.message.text.strip())
            questions_edit_menu(update, context)

    if (play.status == Jerocat.STATUS_VALIDATING):
        login(update, context)
    else:
        if (play.game != None and update.message.text[:1].isdigit()):
            check_answer(update, context)


def split_answer(input):
    '''
    Splits a message in question_order and answer_text
    '''
    question_order = int(re.search(r'\d+', input).group())
    answer_text = input[len(str(question_order)):].strip(" .,;-_:")
    return question_order, answer_text


def play_show_status(update, context):
    '''
    Print game status:
    * All the questions and typed answers
    * Stats of player answers (TODO)
    '''
    chat_id = update.effective_chat.id
    p = j.play_get(chat_id)
    if (p == False):
        j.play_init(chat_id)
        p = j.play_get(chat_id)
    g = j.game_get(p.game_id)
    if (g == None):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="No hi ha cap joc actiu")
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
                if (u != None):
                    message += str(points) + " -> " + ((str(u.first_name)+" "+str(u.last_name)).strip()
                                                       if len(str(u.first_name)+str(u.last_name)) else str(u.username))+"\n"
                else:
                    message += str(points) + " -> " + "unknown..." + "\n"
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)


def login(update, context):
    chat_id = update.effective_chat.id
    play = j.play_get(chat_id)
    if (update.message.text == ADMIN_PASSWORD):
        play.set('editing', True)
        j.save()
        context.bot.deleteMessage(chat_id, update.message.message_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Contrasenya acceptada")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Activa un joc amb /games i introdueix un número per editar pregunta i resposta (0 per a inserir-ne una...)")
    else:
        play.status = Jerocat.STATUS_NOTHING
        j.save()
        context.bot.deleteMessage(chat_id, update.message.message_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Contrasenya INCORRECTA")
        context.bot.send_message(
            chat_id=ORACULUS, text="Login fallit: "+str(update))


def question_edit_markup(play):

    keyboard = []
    game = j.game_get(id=play.game.id)
    pag = int(play.get("pag", 0))
    i = 0
    for q in game.questions:
        i += 1
        if (int(i/10) == pag):
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
            keyboard.append([InlineKeyboardButton(q.text, callback_data=buton_q),
                             InlineKeyboardButton(answers_txt, callback_data=buton_a)])
    if (pag > 0) and (pag < int(len(game.questions)/10)):
        keyboard.append([InlineKeyboardButton("<--Pàg", callback_data="pag_pre"),
                         InlineKeyboardButton("Pàg-->", callback_data="pag_post")])
    elif (pag > 0):
        keyboard.append([InlineKeyboardButton(
            "<--Pàg", callback_data="pag_pre")])
    elif (pag < int(len(game.questions)/10)):
        keyboard.append([InlineKeyboardButton(
            "Pàg-->", callback_data="pag_post")])
    keyboard.append([InlineKeyboardButton("Cancel·la", callback_data="0"),
                     InlineKeyboardButton("Esborra el joc", callback_data="gd")])

    return InlineKeyboardMarkup(keyboard)


def answer_edit_menu(question, update=None, context=None):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Editant respostes de: "+question.text+"\n"
                             + "Escull una resposta per editar, o escriu-ne un de nova",
                             reply_markup=answers_edit_markup(question))


def answers_edit_markup(question):
    keyboard = []
    answers = question.answers
    for a in answers:
        keyboard.append([InlineKeyboardButton(
            a.text, callback_data="qad_"+str(a.id))])
    keyboard.append([InlineKeyboardButton(
        "Cancel·la", callback_data="0")])
    return InlineKeyboardMarkup(keyboard)


def answers_edit_menu_response(play, update, context):
    '''
    Response to questions+answers edit menu
    '''
    try:
        q = None
        query = update.callback_query
        param = (query.data).split("_")
        if param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(q, update, context)
        elif param[0] == "qad":  # deleting answer
            q = j.question_get(id=int(play.get("question_id")))
            j.answer_delete(param[1])
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="S'ha esborrat la resposta")
            answer_edit_menu(q, update, context)

        elif param[0] == "0":  # cancel
            if play.get("editing") == True:
                play.status = Jerocat.STATUS_EDITING_QUESTIONS
                j.save()
                questions_edit_menu(update, context)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Opció incorrecta")
            return False
    except Exception as e:
        print("def answers_edit_menu_response(play,update,context):")
        print(e)


def answer_accept(update, context):
    print("def answer_accept(...):")
    query = update.callback_query
    print("el missatge és: "+query.data)
    param = (query.data).split("_")
    print("l'id de la resposta és: "+str(param[1]))
    a = j.answer_get(id=int(param[1]), only_accepted=False)
    print("acceptant: "+str(a.text))
    a.accepted = True
    j.save()


def answer_forget(update, context):
    query = update.callback_query
    param = (query.data).split("_")
    j.answer_delete(id=param[1])
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Resposta esborrada")


def question_edit_message(chat_id, question, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Reescriu la pregunta, o prem per esborrar",
                             reply_markup=question_delete_markup(question))


def question_delete_markup(question):
    keyboard = []
    keyboard.append([InlineKeyboardButton(
        "Esborra: "+str(question.text), callback_data="qd_"+str(question.id))])
    keyboard.append([InlineKeyboardButton(
        "Cancel·la", callback_data="qd_0")])
    return InlineKeyboardMarkup(keyboard)


def check_answer(update, context):
    chat_id = update.effective_chat.id
    play = j.play_get(chat_id)
    position, answer_text = split_answer(update.message.text)
    question = j.question_from_position(play.game, position)
    if question == None:
        return
    answer = j.answer_check(play.game, position, answer_text)
    user = j.user_upsert(user=update.effective_user)

    if (answer != None):
        j.point_add(play, user, question, answer)
        play_show_status(update, context)
    else:
        # ask for human help....
        answer = j.answer_get(
            question=question, text=answer_text, only_accepted=False)
        if answer == None:
            answer = j.answer_add(question=question, answer=fix_chars(
                str(answer_text).strip()), accepted=False)
        j.point_add(play, user, question, answer)

        help_112 = "Joc: "+play.game.name+"\nPregunta: " + \
            question.text+"\nResposta: "+answer_text
        altres_respostes = ""
        if (question.answers):
            for a in question.answers:
                if a.accepted == True:
                    altres_respostes += "\n - " + a.text
            if (altres_respostes != ""):
                altres_respostes = "\nAltres respostes:"+altres_respostes
        help_112 += altres_respostes
        keyboard = []
        keyboard.append([InlineKeyboardButton("Accepta", callback_data="aa_"+str(answer.id)),
                         InlineKeyboardButton("Esborra", callback_data="ad_"+str(answer.id))])
        context.bot.send_message(chat_id=ORACULUS, text=help_112,
                                 reply_markup=InlineKeyboardMarkup(keyboard))
        # update.message.reply_text("Resposta incorrecta")


def questions_edit_menu(update, context):
    p = j.play_get(update.effective_chat.id)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Escull pregunta per editar, o tecleja'n una de nova",
        reply_markup=question_edit_markup(p))


def games_menu(update, context):
    chat_id = update.effective_chat.id
    p = j.play_get(chat_id)
    p.status = j.STATUS_GAMES_MENU
    p.unset("question_id")
    p.unset('pag')
    j.save()

    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Escull un joc",
        reply_markup=games_menu_markup())
    if p.get("editing", False) == True:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="O escriu el nom d'un joc per afegir-lo")


def games_menu_markup():
    keyboard = []
    games = j.game_list_full()
    for g in games:
        keyboard.append([InlineKeyboardButton(
            g.name, callback_data="g_"+str(g.id))])
    return InlineKeyboardMarkup(keyboard)


def game_menu_response(play, update, context):
    '''
    Response to game menu. It will delete the game, check if game ok and show status or game menu again
    '''
    query = update.callback_query
    param = (query.data).split("_")
    if param[0] == "g":
        g = j.game_get(param[1])
        if (g == False):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="El joc no existeix!")
            return

        context.bot.send_message(chat_id=update.effective_chat.id, text="Has escollit " +
                                 g.name)
        j.play_set_game(play, g)
        if play.get("editing") == True:
            play.status = Jerocat.STATUS_EDITING_QUESTIONS
            j.save()
            questions_edit_menu(update, context)
        else:
            play.status = Jerocat.STATUS_GAME_PLAY
            j.save()
            play_show_status(update, context)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Opció incorrecta")
        return False


def questions_edit_menu_response(play, update, context):
    '''
    Response to questions+answers edit menu
    '''
    try:
        query = update.callback_query
        param = (query.data).split("_")
        if param[0] == "qe":  # estem passant una pregunta a editar
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_QUESTION_TEXT
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            question_edit_message(
                play.chat_id, q, update=update, context=context)
        elif param[0] == "qae":  # estem editant respostes....
            q = j.question_get(id=int(param[1]))
            play.status = Jerocat.STATUS_EDITING_ANSWERS
            play.set("question_id", q.id)
            j.save()
            # mostrem el menú per editar o esborrar la pregunta
            answer_edit_menu(q, update, context)
        elif param[0] == "pag":  # Cancel
            pag = int(play.get("pag", 0))
            if param[1] == "pre":
                pag = max(pag-1, 0)
            else:
                pag = min(pag+1, int(len(play.game.questions)/10))

            play.set("pag", int(pag))
            j.save()
            questions_edit_menu(update, context)
        elif param[0] == "0":  # Cancel
            play.status = Jerocat.STATUS_VALIDATED
            j.save()
            # TODO estem cancel·lant l'edició d'una resposta
            games_menu(update, context)
        elif param[0] == "gd":  # Esborrant un joc!!!!
            if j.game_delete(play.game.id):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Joc esborrat")
                games_menu(update, context)
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Només esborraré jocs buits")
                questions_edit_menu(update, context)
        #     pass
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Opció incorrecta")
            return False
    except Exception as e:
        print("Except questions_edit_menu_response")
        print(e)


def question_delete_menu_response(play, update, context):
    '''
    Response to delete question menu and "cancel editing question text"
    '''
    try:
        query = update.callback_query
        param = (query.data).split("_")
        if param[0] == "qd":  # estem passant una pregunta a esborrar
            if int(param[1]) > 0:
                j.question_delete(id=int(param[1]))

            play.status = j.STATUS_EDITING_QUESTIONS
            play.unset("question_id")
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Pregunta esborrada, amb les seves respostes i puntucacions.")
            j.save()
            questions_edit_menu(update, context)

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Opció incorrecta")
            return False

    except Exception as e:
        print("except: def question_delete_menu_response(play, call):")
        print(e)


def export_ods(update, context):
    # help page
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
    context.bot.send_document(
        chat_id=update.effective_chat.id, document=open(file.name, 'rb'))
    os.remove(file.name)


def import_ods(update, context):
    from pyexcel_ods import get_data
    import pyexcel as pe
    import requests
    import tempfile
    import os

    chat_id = update.effective_chat.id

    if update.message.chat.type != "private":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Només es poden importar jocs per converses privades")
        return
    p = j.play_get(chat_id)

    if p.get('editing', False) == False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Has d'estar validat per poder importar jocs")
        return

    if update.message.document.mime_type != "application/vnd.oasis.opendocument.spreadsheet":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Només puc importar fitxers .ods")
        return

    temp_file, temp_path = tempfile.mkstemp(suffix=".ods")
    file_id = update.message.document.file_id
    newFile = context.bot.get_file(file_id)
#    filePath= newFile.download(custom_path=tempfile.gettempdir())
    newFile.download(temp_path)

    u1 = j.user_get(update.effective_user.id)

    book = pe.get_book(file_name=temp_path)
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
            context.bot.send_message(chat_id=update.effective_chat.id, text="Processant: "+str(g.name),
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
                                q, text=fix_chars(str(cell).strip()), only_accepted=False)
                            if a == None:
                                a = j.answer_add(
                                    question=q, answer=fix_chars(str(cell).strip()))
                                a_new += 1
                            a_counter += 1
            context.bot.send_message(chat_id=update.effective_chat.id, text="S'han processat "+str(q_counter) +
                                     " preguntes i "+str(a_counter)+" respostes", disable_notification=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text="S'han afegit "+str(q_new) +
                                     " preguntes i "+str(a_new)+" respostes", disable_notification=True)

    try:
        os.remove(temp_path)
    except:
        pass
    return


def fix_chars(string):
    '''
    Fixes some chars ODS files might replace
    '''
    old = ["’"]
    new = ["'"]

    for i in range(len(old)):
        string = string.replace(old[i], new[i])
    return string


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("games", games_command))
    dispatcher.add_handler(CommandHandler("login", login_command))
    dispatcher.add_handler(CommandHandler("logout", logout_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("export", export_command))

    dispatcher.add_handler(MessageHandler(Filters.document, import_ods))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, process_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
