"""
This is a detailed example using almost every command of the API
"""

import time
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


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
            # print(str(m.from_user))


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


def games_choose_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    games = j.game_list_full()
    for g in games:
        markup.add(InlineKeyboardButton(g.name, callback_data=g.id))
    return markup

# handle the "/start" command


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    g=j.game_get(call.data)
    if (g==False):
        print("el joc no existeix")
        bot.answer_callback_query(call.id, "El joc no existeix!")
        return
    bot.answer_callback_query(call.id, "Has escollit "+g.name)
    print("carreguem la sessió")
    p = j.play_get(call.id)
    p.set_game = g
    


@bot.message_handler(commands=['games'])
def command_games(m):
    cid = m.chat.id
    p = j.play_get(cid)
    if (p == False):
        print("creem sessió...")
        j.play_init(cid)
        p = j.play_get(cid)
    bot.send_message(cid, "Escull un joc", reply_markup=games_choose_markup())


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


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == 'Mickey':  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
    elif text == 'Minnie':
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" +
                     m.text + "\"\nMaybe try the help page at /help")


bot.polling()
