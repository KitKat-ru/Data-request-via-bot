import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

# TOKEN = os.getenv('TOKEN', default='YOU_TOKEN')
# APP_URL = os.getenv('URL', default='HEROKU_URL')
TOKEN = '5304389044:AAFz8QjdylhnXrPhXnpC_hJnkoJMh4mynAc'
APP_URL = 'https://git.heroku.com/testcasebotartem.git'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, а дай номер' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POSTS'])
def get_message():
    json_string = request.get.data().decode('UTF-8')
    update = telebot.tupes.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove.webhook()
    bot.set.webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', default=5000)))