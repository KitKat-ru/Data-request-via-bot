

# @bot.message_handler(commands=['start1'])
# def start(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     buttonA = telebot.types.InlineKeyboardButton('request_contact', callback_data=message.from_user)
#     markup.row(buttonA)
#     bot.send_contact(message.chat.id, f'Привет {message.from_user.first_name}, а дай номер.', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def handle(call):
#     bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
#     bot.answer_callback_query(call.id)


# @bot.message_handler(commands=['start'])
# def start(message):
#     # markup = telebot.types.InlineKeyboardMarkup()
#     # buttonA = telebot.types.InlineKeyboardButton('request_contact', callback_data=message)
#     # markup.row(buttonA)
#     bot.send_message(message.chat.id, f'Привет {message}, а дай номер.') #, reply_markup=markup
