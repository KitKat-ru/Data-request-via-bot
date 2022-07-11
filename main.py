
import os
import telebot
import requests
import json
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN', default='YOU_TOKEN')
# APP_URL = os.getenv(f'URL{TOKEN}', default=f'HEROKU_URL{TOKEN}')
APP_URL = f'https://testcasebotartem.herokuapp.com/{TOKEN}'
TEST_URL = 'https://s1-nova.ru/app/private_test_python/'


bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text='Передать боту номер телефона',request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, а дай номер.', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def capture_contacts(message):
    if message.from_user.id == message.contact.user_id:
        bot.send_message(message.chat.id, f'Контакт {message.contact.phone_number} сохранен. Спасибо!')
    else:
        bot.send_message(message.chat.id, 'Контакт не сохранен! Прошу прислать корректные данные')
    # print(message.contact)
    # print()
    # print(message)
    data = {
        "phone": message.contact.phone_number,
        "login": f'@{message.from_user.username}'
    }
    requests.post(TEST_URL, json=data)






@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, f'{message.from_user.first_name}, извините, но я создан что бы получать Ваш номер телефона')
    bot.send_message(message.chat.id, 'Введите команду /start что бы взаимодействовать со мной')


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
