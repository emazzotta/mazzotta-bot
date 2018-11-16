#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import shutil
import tempfile
from os.path import join
from sys import platform
from apscheduler.schedulers.background import BackgroundScheduler

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
    superhelp_text += '@BotFather\n'
    superhelp_text += '\n'.join([f'{command} - {text}' for command, text in COMMANDS.items()])
    bot.send_message(chat_id, superhelp_text)


@bot.message_handler(commands=['say', 'sing'])
def bot_voice(message):
    chat_id = message.chat.id
    voice_type = 'Zarvox' if message.text.startswith('/say') else 'Cellos'
    voice_text = remove_command(message)
    voice_text = remove_dangerous_characters(voice_text)
    logger.info(f'Bot voice invoked in {chat_id}')

    if len(voice_text) == 0:
        bot.send_message(chat_id, f'Okay, but what? E.g. /say hello or /sing hello')
    else:
        temp_path = tempfile.mkdtemp()
        filename = 'voice'
        voice_file = join(temp_path, f'{filename}.mp3')

        if platform == 'darwin':
            cd_cmd = f'cd {temp_path}'
            say_cmd = f'say -v "{voice_type}" "{voice_text}" -o {filename}'
            conversion_cmd = f'lame -m m "{filename}.aiff" "{filename}.mp3"'
            args = f'{cd_cmd} && {say_cmd} && {conversion_cmd} &> /dev/null'
        else:
            espeak_cmd = f'echo "{voice_text}" | espeak -s 120 -ven-us+m1 --stdout'
            ffmpeg_cmd = f'ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 {voice_file}'
            args = f'{espeak_cmd} | {ffmpeg_cmd} &> /dev/null'

        result = os.popen(args).read()
        logger.info(f'Sending voice to {chat_id}')
        bot.send_voice(chat_id, open(voice_file, 'rb'))
        shutil.rmtree(temp_path)


@bot.message_handler(commands=['zhaw'])
def zhaw(message):
    chat_id = message.chat.id
    logger.info(f'Sending zhaw statistics to {chat_id}')
    bot.send_message(chat_id, show_zhaw_statistics())


def show_zhaw_statistics():
    return os.popen(f'kw 10 telegram-formatting').read()


def send_zhaw_statistics_to_optimizers():
    bot.send_message(os.environ.get('OPTIMIZER_CHAT_ID'), show_zhaw_statistics())


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


def remove_dangerous_characters(voice_text):
    return re.sub(r'[^a-zA-Z0-9!@%&*()_-+=.,<>;: ]', '', voice_text)


def remove_command(message):
    return re.sub(r'^\/[a-z]+(@[a-z]+)?', '', message.text).strip()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_zhaw_statistics_to_optimizers, 'cron', day_of_week='mon', hour=8, minute=0)
    scheduler.start()

    try:
        bot.polling()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
