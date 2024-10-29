import telebot
import json
import random


# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен, полученный от BotFather
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

# Загрузка данных из JSON файлов
with open('data/npc.json', 'r', encoding='utf-8') as npc_file:
    data_npc = json.load(npc_file)

with open('data/enemy.json', 'r', encoding='utf-8') as enemy_file:
    data_enemy = json.load(enemy_file)

# Стартовое меню
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Characters")
    btn2 = telebot.types.KeyboardButton("Enemies")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Choose a category:", reply_markup=markup)

# Обработка выбора категорий
@bot.message_handler(func=lambda message: message.text in ["Characters", "Enemies"])
def choose_subcategory(message):
    category = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    if category == "Characters":
        for subcategory in data_npc.keys():
            markup.add(telebot.types.KeyboardButton(subcategory))
    elif category == "Enemies":
        for subcategory in data_enemy.keys():
            markup.add(telebot.types.KeyboardButton(subcategory))
    
    markup.add(telebot.types.KeyboardButton("Back to main menu"))
    bot.send_message(message.chat.id, f"Choose a subcategory of {category}:", reply_markup=markup)

# Обработка выбора подкатегорий для Characters
@bot.message_handler(func=lambda message: message.text in data_npc.keys())
def generate_npc_phrase(message):
    subcategory = message.text
    phrase = random.choice(data_npc[subcategory])
    bot.send_message(message.chat.id, f"{subcategory} says: {phrase}")
    start_message(message)

# Обработка выбора подкатегорий для Enemies
@bot.message_handler(func=lambda message: message.text in data_enemy.keys())
def generate_enemy_phrase(message):
    subcategory = message.text
    phrase = random.choice(data_enemy[subcategory]['phrases'])
    damage = data_enemy[subcategory]['damage']
    bot.send_message(message.chat.id, f"{subcategory} says: {phrase}\nDamage: {damage}")
    start_message(message)

# Возврат к главному меню
@bot.message_handler(func=lambda message: message.text == "Back to main menu")
def back_to_main_menu(message):
    start_message(message)

# Запуск бота
bot.polling(none_stop=True)
