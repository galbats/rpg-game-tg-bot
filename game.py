import dump_npc_and_enemy
import dump_map
import characters 
import random
import json
import time
import sys
from itertools import cycle


def create_npc():
    with open('data/npc.json', 'r', encoding='utf-8') as npc_file:
        npc_data = json.load(npc_file)
    names = list(npc_data.keys())

    unit = characters.NPC(random.choice(names))
    unit.load_questions(npc_data[unit.name])

    return unit

def create_enemy():
    with open('data/enemy.json', 'r', encoding='utf-8') as enemy_file:
        enemy_data = json.load(enemy_file)
    names = list(enemy_data.keys())
   
    unit = characters.Enemy(random.choice(names))
    unit.load_questions(enemy_data[unit.name]['phrases'])
    unit.load_attack(enemy_data[unit.name]['damage'])
   
    return unit

def create_protagonist(name: str):
    # Сначала читаем данные из файла
    try:
        with open('data/protagonists.json', 'r', encoding='utf-8') as proto_file:
            proto_data = json.load(proto_file)
    except FileNotFoundError:
        # Если файл не существует, создаем пустой словарь
        proto_data = {}

    # Определяем новый индекс
    index = len(proto_data)
    # Добавляем нового протагониста в словарь
    proto_data[index + 1] = name

    # Теперь записываем обновленные данные обратно в файл
    with open('data/protagonists.json', 'w', encoding='utf-8') as proto_file:
        json.dump(proto_data, proto_file, ensure_ascii=False, indent=4)
    
    return index

def create_location():
    with open('data/locations.json', 'r', encoding='utf-8') as locations_file:
        locations_data = json.load(locations_file)
    # names = list(locations_data.keys())
    loc_list = []
    for k, v in locations_data.items():
        loc_list.append(characters.Direction(k, v))
   
    return loc_list


def game():
    # Инициируем NPC, Enemy и их вопросы
    dump_npc_and_enemy.initialize_npc_and_enemy()
    dump_map.initialize_map()
    # Создаем игрока
    player_name = input("Введите имя: ")
    index = create_protagonist(player_name)
    player = characters.Protagonist(player_name, index)
    locations_list = cycle(create_location())
    location = next(locations_list)
    player.whereami(location)
    print()
    steps_counter = 0
    # NPC_list = create_npc()
    # Enemy_list = create_enemy()
    # all_list = NPC_list + Enemy_list
    while(True):
        unit = random.choice([create_enemy(), create_npc()])
        time.sleep(1)
        print("============================================================================")
        print(f"Ваши показатели: HP={player.hp}, STRENGHT={player.strength}, ARMOR={player.armor}")
        print("============================================================================\n")
        if isinstance(unit, characters.NPC):
            print(f"Вам повстречался дружественный NPC - {unit.name}")
            time.sleep(1)
            print(f"-- {unit.name} говорит: ", end ='')
            action = unit.action()
            # Смотрим по индексу действия (вопроса) и исходя из этого даем плюшки игроку
            if (action+1) % 4 == 1:
                time.sleep(1)
                print("Держи яблоко. Если соберешь 3 штуки, получишь + 1 к силе")
                player.take("apple")
                
            elif (action+1) % 4 == 2:
                time.sleep(1)
                print("Держи эликсир жизни. Каждые 2 штуки увеличивают HP на 1")
                player.take("boost")

            elif (action+1) % 4 == 3:
                time.sleep(1)
                print("Держи металлическую руду. Соберешь 3 руды - улучшишь броню на 1")
                player.take("metall")
            else:
                time.sleep(1)
                print("Хорошей дороги, путник - ты ничего не получил, но ничего и не потерял. А это уже неплохо.")
        else:
            print(f"Вам повстречался враг {unit.name}")
            time.sleep(1)
            print(f"-- {unit.name} говорит: ", end ='')
            action = unit.action()
            if action == 3:
                time.sleep(1)
                print("Вас миновали проблемы, враг решил, что вы недостойны сражаться с ним. Врагов много, а вы у мамы один. Идите дальше.")
            else:
                print(f"Завязался бой: урон врага {unit.attack+location.effect}")
                time.sleep(1)
                while unit.hp > 0 and player.hp > 0:
                    try:
                        print(f"x Вас атаковали")
                        player.take_hit(unit.attack + location.effect - player.armor)
                        print(f"Ваши показатели: HP={player.hp}, STRENGHT={player.strength}")
                        time.sleep(1)
                        print("x Удар в ответ:")
                        player.attack(unit)
                        time.sleep(1)
                        if unit.hp > 0:
                            print(f"Показатели монстра: HP={unit.hp}, ATTACK={unit.attack+location.effect}")
                        else:
                            print('======Вы молодец, монстр повержен======')
                    except Exception as e:
                        print(e)
                        sys.exit(1)
        is_game_contionue = input("\n-> Путь дальше может быть опасен... Идем дальше? (y/n)")
        steps_counter = player.go(steps_counter)
        if steps_counter >= 5:
            steps_counter = 0
            location = next(locations_list)
            print("\n\n=====Местность меняется=====")
            player.whereami(location)
            print()

        if is_game_contionue.lower() == 'y':
            time.sleep(1)
            continue
        else:
            time.sleep(1)
            print("\n======Этот мир слишком жесток для тебя, слабак. Прощай======\n")
            break


if __name__ == "__main__":
    game()

