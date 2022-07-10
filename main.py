import os
import telebot

from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN', default='YOU_TOKEN')
APP_URL = os.getenv(f'URL{TOKEN}', default=f'HEROKU_URL/{TOKEN}')


bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f'Привет {message}, а дай номер.')




@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', default=5000)))
