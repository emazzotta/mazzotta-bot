#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import random
import re
import string
import time

import telebot
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(os.environ.get('BOT_API_TOKEN'))

COMMANDS = {
    'help': 'Show this text',
    'say': 'Say something in a bot voice (/say [lang=de] <text>)',
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


def extract_language_and_text(voice_text):
    results = re.match('(((lang=)([A-Za-z]{2}))?(.*))', voice_text).groups()
    text = results[4]
    language = results[3]
    return 'en' if language is None else language.strip(), text.strip()


@bot.message_handler(commands=['say'])
def bot_voice(message):
    chat_id = message.chat.id
    voice_text = remove_command(message.text)
    voice_text = remove_dangerous_characters(voice_text)
    logger.info(f'Bot voice invoked in {chat_id}, text: "{voice_text}"')

    if len(voice_text) == 0:
        bot.send_message(chat_id, f'Okay, but what? E.g. /say hello')
        return

    language, text = extract_language_and_text(voice_text)

    bot.send_message(chat_id, "Hold on! I'm recording myself...")
    file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    text_file = f'/app/in/{file_name}.txt'
    open(text_file, 'w+').write(f'{language}\n{text}')

    voice_file = f'/app/out/{file_name}.mp3'
    sleep_times = 0.0
    while not os.path.exists(voice_file):
        if sleep_times > 10:
            bot.send_message(chat_id, f'Sorry, recording failed')
            return
        sleep_duration = 0.2
        sleep_times += sleep_duration
        time.sleep(sleep_duration)

    bot.send_voice(chat_id, open(voice_file, 'rb'))


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


def remove_dangerous_characters(text):
    return re.sub(r'[^\w!@%&*()_+=.,<>;: ]', '', text)


def remove_command(text):
    return re.sub(r'^/[a-z]+(@[\S]*)?', '', text).strip()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_zhaw_statistics_to_optimizers, 'cron', day_of_week='mon', hour=8, minute=0)
    scheduler.start()

    try:
        bot.polling()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
