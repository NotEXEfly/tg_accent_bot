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
    print('Querry: ', message.chat.id)

    log = '***log*** user: {}|| Message: {}'.format(
        message.chat.id, message.text)
    bot.send_message(93260961, log)


def get_result(message):
    obj = Accent(message.text)
    if obj.is_solo_word:
        bot.send_message(message.chat.id, obj.one_word())
    else:
        bot.send_message(message.chat.id, obj.many_words())


bot.polling(none_stop=True)
