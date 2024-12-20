import telebot
from telebot import types

bot = telebot.TeleBot('7949785190:AAEMaVEiHnfq0zJrQVjjuXrQj_NmMaos8PU')
data_dict = {}
user_state = {}
admin_user_id = 7114026647
START, ADD_NAME, ADD_PHONE  = range(3)

@bot.message_handler(commands=['start'])
def start(message):
    global user_state
    user_id = message.from_user.id  # Получение user_id пользователя
    #print(f"User ID: {user_id}") 
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Записаться на консультацию", callback_data="consult")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Добро пожаловать в агентство Егора Милюкова. Мы оценим ваши шансы на второе гражданство за 30 минут", 
        parse_mode="HTML", reply_markup=markup)
    user_state[message.chat.id] = START

@bot.callback_query_handler(func=lambda call: call.data.startswith("consult"))
def handle_name(call):
    global user_state, data_dict
    #global admin_user_id
    #admin_user_id = call.message.chat.id
    #print("admin_user_id: ", call.message.from_user.id)
    data_dict[call.message.chat.id] = {}
    bot.send_message(call.message.chat.id, "Введите, пожалуйста, ваше имя и фамилию")
    user_state[call.message.chat.id] = ADD_NAME

@bot.message_handler(content_types=['text'], func=lambda message: user_state.get(message.chat.id) == ADD_NAME)
def handle_phone(message):
    global user_state, data_dict
    data_dict[message.chat.id]['Name'] = message.text
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Telegram", callback_data="tele")
    btn2 = types.InlineKeyboardButton("WhatsApp", callback_data="whats")
    btn3 = types.InlineKeyboardButton("Сотовая связь", callback_data="mobile")
    markup.row(btn1, btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, "Выберите наиболее удобный для вас способ связи:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tele"))
def handle_tele(call):
    global user_state, data_dict
    data_dict[call.message.chat.id]['Connection'] = "Telegram"
    bot.send_message(call.message.chat.id, "Укажите номер телефона, привязанный к вашему Telegram, или имя пользователя.")
    user_state[call.message.chat.id] = ADD_PHONE

@bot.callback_query_handler(func=lambda call: call.data.startswith("whats"))
def handle_whats(call):
    global user_state, data_dict
    data_dict[call.message.chat.id]['Connection'] = "WhatsApp"
    bot.send_message(call.message.chat.id, "Укажите номер телефона, привязанный к вашему WhatsApp.")
    user_state[call.message.chat.id] = ADD_PHONE

@bot.callback_query_handler(func=lambda call: call.data.startswith("mobile"))
def handle_mob(call):
    global user_state, data_dict
    data_dict[call.message.chat.id]['Connection'] = "Сотовая связь"
    bot.send_message(call.message.chat.id, "Укажите ваш номер телефона.")
    user_state[call.message.chat.id] = ADD_PHONE

# Обработчик возврата к выбору языка или ввода кода
@bot.message_handler(content_types=['text'], func=lambda message: user_state.get(message.chat.id) == ADD_PHONE)
def handle_return_to_language_selection(message):
    global user_state, data_dict
    data_dict[message.chat.id]['Phone'] = message.text
    bot.send_message(message.chat.id, "Спасибо, ваша заявка на консультацию отправлена. В ближайшее время мы свяжемся с вами.\n\nПодписывайтесь на наш телеграм-канал - @bestpassport")
    message_text = f"Новая запись на консультацию в агентство Егора Милюкова!\nДанные клиента:\nИмя: {data_dict[message.chat.id]['Name']}\nСпособ связи: {data_dict[message.chat.id]['Connection']}\nКонтактные данные: {data_dict[message.chat.id]['Phone']}"
    bot.send_message(admin_user_id, message_text)
    user_state[message.chat.id] = START

# Обработчик возврата к выбору языка или ввода кода
@bot.message_handler(content_types=['text'], func=lambda message: user_state.get(message.chat.id) == START)
def handle_return_to_language_selection(message):
    start(message)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)