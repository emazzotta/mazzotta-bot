#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from os.path import join, realpath, dirname

import telebot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

token = open(join(dirname(realpath(__file__)), 'secret.key'), 'r+').read()
bot = telebot.TeleBot(token)

VALID_COMMANDS = ['help', 'say']


@bot.message_handler(commands=['help'])
def help_info(message):
    chat_id = message.chat.id
    logger.info(f'Sending help to {chat_id}')
    bot.send_message(chat_id, '/help - Show this text' +
                     '\n/say - Ask the bot to say something in a bot voice')


@bot.message_handler(commands=['say'])
def say(message):
    chat_id = message.chat.id
    say = message.text.replace('/say', '').strip()
    if len(say) == 0:
        bot.send_message(chat_id, f'I need you to tell me what to say. E.g. /say hello')
    else:
        bot.send_message(chat_id, f'hello! you asked me to say: {say}')
        # TODO:
        # apt-get update && apt-get install -y espeak ffmpeg
        # echo "hello" | espeak -s 120 -ven-us+m1 --stdout | \
        # ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 final.mp3 &> /dev/null


@bot.message_handler(func=lambda message: is_invalid_command(message))
def unknown_command(message):
    chat_id = message.chat.id
    logger.info(f'Unknown command {message.text} in {chat_id}')
    bot.send_message(chat_id, text='That ain\'t no command!')


def is_invalid_command(message):
    return not message.text or \
           all(message.text.startswith('/') and not message.text.startswith(f'/{valid}') for valid in VALID_COMMANDS)


if __name__ == '__main__':
    logger.info('Starting bot...')
    bot.polling()
