import telebot
import random
import time
from itertools import cycle
from characters import Protagonist, NPC, Enemy, Direction
from load_all import load_data  


# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен, полученный от BotFather
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

# Глобальные переменные для игры
player = None
locations_list = None
location = None
steps_counter = 0
game_started = False
base_location = None  # Базовая локация для проверки завершения круга

# Загрузка данных
data_npc, data_enemy, locations_data = load_data()

def start_game(chat_id):
    """
    Инициализирует игру, создавая игрока и выбирая начальную локацию.

    Args:
        chat_id (int): Идентификатор чата Telegram, в котором идет игра.
    """
    global player, locations_list, location, steps_counter, game_started, base_location

    steps_counter = 0
    player_name = bot.get_chat(chat_id).first_name
    index = len(player_name)
    player = Protagonist(player_name, index)

    # Создаем список локаций и выбираем начальную локацию
    locations_list = cycle([Direction(k, v) for k, v in locations_data.items()])
    location = next(locations_list)
    base_location = location  # Сохраняем базовую локацию

    if not game_started:
        bot.send_message(chat_id, f"Игра началась! Добро пожаловать, {player.name}!")
        game_started = True
    bot.send_message(chat_id, f"Вы находитесь в {location.name}: {location.description}")

    show_main_menu(chat_id)

def show_main_menu(chat_id):
    """
    Показывает основное меню с кнопками для выбора действия.

    Args:
        chat_id (int): Идентификатор чата Telegram, в котором идет игра.
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Персонажи 👤")
    btn2 = telebot.types.KeyboardButton("Враги 💀")
    btn3 = telebot.types.KeyboardButton("Где я? 📍")
    btn4 = telebot.types.KeyboardButton("Вперед ⬆️")
    btn5 = telebot.types.KeyboardButton("Инвентарь 🎒")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Обрабатывает команду /start и показывает стартовое меню.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    show_start_menu(message.chat.id)

def show_start_menu(chat_id):
    """
    Показывает стартовое меню с кнопкой "Начать играть".

    Args:
        chat_id (int): Идентификатор чата Telegram, в котором идет игра.
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = telebot.types.KeyboardButton("Начать играть")
    markup.add(btn_start)
    bot.send_message(chat_id, "Добро пожаловать в игру! Нажмите 'Начать играть', чтобы начать.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Начать играть")
def handle_start_game(message):
    """
    Обрабатывает нажатие на кнопку "Начать играть" и запускает игру.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    start_game(message.chat.id)

def handle_player_death(chat_id):
    """
    Обрабатывает смерть игрока, завершая игру и предлагая начать заново.

    Args:
        chat_id (int): Идентификатор чата Telegram, в котором идет игра.
    """
    global player, locations_list, location, steps_counter, game_started

    bot.send_message(chat_id, "Вы погибли. Игра окончена.")
    
    # Сброс глобальных переменных
    player = None
    locations_list = None
    location = None
    steps_counter = 0
    game_started = False

    # Предложение начать игру заново
    show_start_menu(chat_id)

def handle_game_completion(chat_id):
    """
    Обрабатывает успешное завершение игры, когда игрок возвращается в базовую локацию.

    Args:
        chat_id (int): Идентификатор чата Telegram, в котором идет игра.
    """
    global player, locations_list, location, steps_counter, game_started

    bot.send_message(chat_id, "Поздравляем, вы прошли игру!\nДля вас открыто тайное знание: https://clck.ru/3CjnLK", disable_web_page_preview=True)
    
    # Сброс глобальных переменных
    player = None
    locations_list = None
    location = None
    steps_counter = 0
    game_started = False

    # Предложение начать игру заново
    show_start_menu(chat_id)

@bot.message_handler(func=lambda message: message.text == "Вперед ⬆️")
def move_forward(message):
    """
    Обрабатывает нажатие на кнопку "Вперед", двигая игрока по локациям и выполняя случайные события.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    global steps_counter, location, locations_list, base_location

    steps_counter += 1

    if steps_counter >= 5:
        steps_counter = 0
        location = next(locations_list)
        bot.send_message(message.chat.id, "\n\n=====Местность меняется=====")
        bot.send_message(message.chat.id, f"Вы находитесь в {location.name}: {location.description}")

        # Проверка на возвращение в базовую локацию
        if location == base_location:
            handle_game_completion(message.chat.id)
            return

    # Случайное событие
    unit = random.choice([create_enemy(), create_npc()])
    bot.send_message(message.chat.id, "=============================")
    bot.send_message(message.chat.id, f"Ваши показатели: HP={player.hp}, СИЛА={player.strength}, БРОНЯ={player.armor}")
    bot.send_message(message.chat.id, "=============================\n")

    if isinstance(unit, NPC):
        bot.send_message(message.chat.id, f"Вам повстречался дружественный NPC {unit.name}.")
        time.sleep(1)
        action_index = unit.action()
        bot.send_message(message.chat.id, f"-- {unit.name} говорит: {unit.questions[action_index]}")

        if (action_index + 1) % 4 == 1:
            bot.send_message(message.chat.id, "Держи яблоко. Если соберешь 3 штуки, получишь +1 к силе.")
            player.take("apple")

        elif (action_index + 1) % 4 == 2:
            bot.send_message(message.chat.id, "Держи эликсир жизни. Каждые 2 штуки увеличивают HP на 1.")
            player.take("boost")

        elif (action_index + 1) % 4 == 3:
            bot.send_message(message.chat.id, "Держи металлическую руду. Соберешь 3 руды - улучшишь броню на 1.")
            player.take("metall")

        else:
            bot.send_message(message.chat.id, "Хорошей дороги, путник - ты ничего не получил, но ничего и не потерял. А это уже неплохо.")

    else:
        bot.send_message(message.chat.id, f"Вам повстречался враг {unit.name}.")
        time.sleep(1)
        action_index = unit.action()
        bot.send_message(message.chat.id, f"-- {unit.name} говорит: {unit.questions[action_index]}")

        if action_index == 3:
            bot.send_message(message.chat.id, "Вас миновали проблемы, враг решил, что вы недостойны сражаться с ним. Врагов много, а вы у мамы один. Идите дальше.")
        else:
            bot.send_message(message.chat.id, f"Завязался бой: урон врага {unit.attack + location.effect}")
            time.sleep(1)
            while unit.hp > 0 and player.hp > 0:
                try:
                    bot.send_message(message.chat.id, "x Вас атаковали")
                    player.take_hit(unit.attack + location.effect - player.armor)
                    if player.hp <= 0:
                        handle_player_death(message.chat.id)
                        return

                    bot.send_message(message.chat.id, f"Ваши показатели: HP={player.hp}, СИЛА={player.strength}")
                    time.sleep(1)
                    bot.send_message(message.chat.id, "x Удар в ответ:")
                    player.attack(unit)
                    time.sleep(1)
                    if unit.hp > 0:
                        bot.send_message(message.chat.id, f"Показатели монстра: HP={unit.hp}, АТАКА={unit.attack + location.effect}")
                    else:
                        bot.send_message(message.chat.id, '======Вы молодец, монстр повержен======')
                except Exception as e:
                    bot.send_message(message.chat.id, str(e))
                    handle_player_death(message.chat.id)
                    return

    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text in ["Персонажи 👤", "Враги 💀"])
def choose_subcategory(message):
    """
    Обрабатывает выбор категории Персонажи или Враги и предлагает выбрать подкатегорию.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    category = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if category == "Персонажи 👤":
        for subcategory in data_npc.keys():
            markup.add(telebot.types.KeyboardButton(subcategory))
    elif category == "Враги 💀":
        for subcategory in data_enemy.keys():
            markup.add(telebot.types.KeyboardButton(subcategory))

    markup.add(telebot.types.KeyboardButton("Вернуться в главное меню"))
    bot.send_message(message.chat.id, f"Выберите подкатегорию для {category}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Вернуться в главное меню")
def back_to_main_menu(message):
    """
    Обрабатывает нажатие на кнопку "Вернуться в главное меню" и показывает основное меню.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text in data_npc.keys())
def generate_npc_phrase(message):
    """
    Обрабатывает выбор подкатегории Персонажей и показывает случайную фразу NPC.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    subcategory = message.text
    npc = NPC(subcategory)
    npc.load_questions(data_npc[subcategory])  # Загружаем вопросы NPC

    if not npc.questions:
        bot.send_message(message.chat.id, f"Ошибка: у NPC {subcategory} нет вопросов.")
        show_main_menu(message.chat.id)
        return

    phrase_index = npc.action()
    phrase = data_npc[subcategory][phrase_index]
    bot.send_message(message.chat.id, f"{subcategory} говорит: {phrase}")
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text in data_enemy.keys())
def generate_enemy_phrase(message):
    """
    Обрабатывает выбор подкатегории Врагов и показывает случайную фразу врага, а также его урон.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    subcategory = message.text
    enemy = Enemy(subcategory)
    enemy.load_questions(data_enemy[subcategory]['phrases'])  # Загружаем фразы врага
    phrase_index = enemy.action()
    phrase = data_enemy[subcategory]['phrases'][phrase_index]
    damage = data_enemy[subcategory]['damage']
    bot.send_message(message.chat.id, f"{subcategory} говорит: {phrase}\nУрон: {damage}")
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Где я? 📍")
def show_location(message):
    """
    Обрабатывает нажатие на кнопку "Где я?" и показывает текущую локацию игрока.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    global location
    if location is None:
        location = next(locations_list)  # Инициализируем локацию, если она пуста
    bot.send_message(message.chat.id, f"Вы находитесь в {location.name}: {location.description}")
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Инвентарь 🎒")
def show_inventory(message):
    """
    Обрабатывает нажатие на кнопку "Инвентарь" и показывает текущее содержимое инвентаря игрока.

    Args:
        message (telebot.types.Message): Сообщение Telegram.
    """
    bot.send_message(message.chat.id, format_inventory(player.inventory))
    show_main_menu(message.chat.id)

def create_npc():
    """
    Создает и возвращает случайного NPC.

    Returns:
        NPC: Случайный NPC из списка доступных.
    """
    names = list(data_npc.keys())
    unit = NPC(random.choice(names))
    unit.load_questions(data_npc[unit.name])
    return unit

def create_enemy():
    """
    Создает и возвращает случайного врага.

    Returns:
        Enemy: Случайный враг из списка доступных.
    """
    names = list(data_enemy.keys())
    unit = Enemy(random.choice(names))
    unit.load_questions(data_enemy[unit.name]['phrases'])
    unit.load_attack(data_enemy[unit.name]['damage'])
    return unit

def format_inventory(inventory):
    """
    Форматирует и возвращает строку с содержимым инвентаря игрока.

    Args:
        inventory (dict): Словарь с предметами инвентаря.

    Returns:
        str: Отформатированная строка с содержимым инвентаря.
    """
    result = "== В вашем инвентаре:\n"
    if len(inventory) == 0:
        result += "Пусто\n"
    else:
        result += f"Яблоки: {inventory.get('apple', 0)} шт.\n"
        result += f"Эликсир: {inventory.get('boost', 0)} шт.\n"
        result += f"Железо: {inventory.get('metall', 0)} шт.\n"
    return result

# Запуск бота
bot.polling(none_stop=True)
