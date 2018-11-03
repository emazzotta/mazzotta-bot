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

VALID_COMMANDS = ['say']


@bot.message_handler(commands=['say'])
def say(message):
    chat_id = message.chat.id
    voter = message.from_user.username
    votee = message.text.split(' ')
    bot.send_message(chat_id, 'hello! you asked me to say!')


@bot.message_handler(func=lambda message: is_invalid_command(message))
def unknown_command(message):
    chat_id = message.chat.id
    logger.info(f'Unknown command {message.text} in {chat_id}')
    bot.send_message(chat_id, text='That ain\'t no command!')


def is_invalid_command(message):
    return message.document.mime_type == 'text/plain' and \
           all(message.text.startswith('/') and not message.text.startswith(f'/{valid}') for valid in VALID_COMMANDS)


if __name__ == '__main__':
    logger.info('Starting bot...')
    bot.polling()
