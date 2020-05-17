import telebot

from f import Accent
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

print('bot run')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 'Привет, я покажу куда ставить ударение!')


@bot.message_handler(content_types=['text'])
def lalala(message):

    if len(message.text) < 250:
        get_result(message)
    else:
        bot.send_message(message.chat.id, 'Слишком большой текст')

    # logs
    print('Querry: {} chat_id: {}'.format(message.from_user.username, message.chat.id))

    log = '*\|LOG*' + '\n'
    log += '*\|username*: ' + message.from_user.username + '\n'
    log += '*\|name*: ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n'
    log += '*\|_Message:_*\n' + message.text
    bot.send_message(93260961, log, parse_mode='MarkdownV2')


def get_result(message):
    obj = Accent(message.text)
    if obj.is_solo_word:
        bot.send_message(message.chat.id, obj.one_word())
    else:
        bot.send_message(message.chat.id, obj.many_words())


bot.polling(none_stop=True)
