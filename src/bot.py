#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from os.path import join, realpath, dirname

import telebot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
token = open(join(dirname(realpath(__file__)), 'secret.key'), 'r+').read()
bot = telebot.TeleBot(token)

COMMANDS = {
    'help': 'Show this text',
    'say': 'Ask the bot to say something in a bot voice',
    'zhaw': 'Show current ZHAW stats',
}


@bot.message_handler(commands=['help'])
def help_info(message):
    chat_id = message.chat.id
    logger.info(f'Sending help to {chat_id}')
    help_text = '\n'.join([f'/{command} - {text}' for command, text in COMMANDS.items()])
    bot.send_message(chat_id, help_text)


@bot.message_handler(commands=['superhelp'])
def superhelp(message):
    chat_id = message.chat.id
    logger.info(f'Sending superhelp to {chat_id}')
    superhelp_text = 'README:\n\n'
    superhelp_text += '|Command|Action|\n'
    superhelp_text += '|---|---|\n'
    superhelp_text += '\n'.join([f'|/{command}|{text}|' for command, text in COMMANDS.items()])
    superhelp_text += '\n\n'
    superhelp_text += 'Bot Father:\n'
    superhelp_text += '\n'.join([f'{command} - {text}' for command, text in COMMANDS.items()])
    bot.send_message(chat_id, superhelp_text)


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


@bot.message_handler(commands=['zhaw'])
def zhaw(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'You asked me to show you zhaw')


@bot.message_handler(func=lambda message: is_invalid_command(message))
def unknown_command(message):
    chat_id = message.chat.id
    logger.info(f'Unknown command {message.text} in {chat_id}')
    bot.send_message(chat_id, text='That ain\'t no command!')


def is_invalid_command(message):
    if not message.text:
        return False
    if not message.text.startswith('/'):
        return False
    return not any(message.text.startswith(f'/{valid}') for valid in COMMANDS.keys())


if __name__ == '__main__':
    logger.info('Starting bot...')
    bot.polling()
