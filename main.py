"""Тестовой задание."""
import logging
import os
import sys
from http import HTTPStatus
from logging import StreamHandler
from urllib.error import HTTPError

import requests
import telebot
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

TOKEN = os.getenv('TOKEN', default='YOU_TOKEN')
APP_URL = f'https://testcasebotartem.herokuapp.com/{TOKEN}'
TEST_URL = 'https://s1-nova.ru/app/private_test_python/'


bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    filename='test_bot.log',
    encoding='utf-8',
    format='%(asctime)s, %(levelname)s, %(funcName)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s - %(lineno)s '
)
handler.setFormatter(formatter)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция для начала работы бота."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    button_phone = telebot.types.KeyboardButton(
        text='Передать номер телефона',
        request_contact=True,
    )
    keyboard.add(button_phone)
    try:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Привет {message.from_user.first_name}, а дай номер.',
            reply_markup=keyboard,
        )
        logger.info('Сообщение отправлено.')
    except Exception as err:
        logger.error(
            f'Сообщение {bot.send_message.text} не отправлено. Ошибка - {err}.'
        )
        raise Exception(f'Сообщение не отправлено. Ошибка - {err}.')


@bot.message_handler(content_types=['contact'])
def capture_contacts(message):
    """Перехватывает контакт.

    Функция для проверки подлинности контакта пользователя.
    Функция для передачи контакта пользователя на тестовый URL.
    """
    if message.from_user.id == message.contact.user_id:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Контакт {message.contact.phone_number} сохранен. Спасибо!',
        )
        data = {
            "phone": message.contact.phone_number,
            "login": f'@{message.from_user.username}'
        }
        try:
            requests.post(TEST_URL, json=data)
            logger.info(f'Сообщение отправлено на {TEST_URL}.')
        except HTTPError as err:
            logger.critical(f'Ошбика сети - {err}')
            raise HTTPError(f'Ошбика сети - {err}')
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Контакт не сохранен! Прошу прислать корректные данные',
        )


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    """Заглушка.

    Заглушка на все действия пользователя
    не предусмотренные функционалом бота.
    """
    bot.reply_to(
        message=message,
        text=f'{message.from_user.first_name}, извините,'
        'но я создан что бы получать Ваш номер телефона',
    )
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите команду /start что бы взаимодействовать со мной',
    )


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    """Получение и декодирование json."""
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', HTTPStatus.OK
    except Exception as err:
        logger.critical(f'Ошбика - {err}')
        raise Exception(f'Ошбика - {err}')


@server.route('/')
def webhook():
    """Перезагрузка и установка нового webhook."""
    try:
        bot.remove_webhook()
        bot.set_webhook(url=APP_URL)
        return 'OK', HTTPStatus.OK
    except HTTPError as err:
        logger.critical(f'Ошбика сети - {err}')
        raise HTTPError(f'Ошбика сети - {err}')


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', default=5000)))
