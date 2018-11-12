#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import tempfile
from os.path import join
from sys import platform

import telebot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(os.environ.get('BOT_API_TOKEN'))

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
        temp_path = tempfile.mkdtemp()
        filename = 'voice'
        voice_file = join(temp_path, f'{filename}.mp3')

        if platform == 'darwin':
            cd_cmd = f'cd {temp_path}'
            say_cmd = f'say -v "Zarvox" "{say}" -o {filename}'
            conversion_cmd = f'lame -m m "{filename}.aiff" "{filename}.mp3"'
            args = f'{cd_cmd} && {say_cmd} && {conversion_cmd} &> /dev/null'
        else:
            espeak_cmd = f'espeak -s 120 -ven-us+m1 --stdout'
            ffmpeg_cmd = f'ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 {voice_file}'
            args = f'echo "{say}" | {espeak_cmd} | {ffmpeg_cmd} &> /dev/null'

        result = os.popen(args).read()
        bot.send_voice(chat_id, open(voice_file, 'rb'))


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
