import json
import os
from dump_npc_and_enemy import initialize_npc_and_enemy
from dump_map import initialize_map


def load_data():
    """
    Загружает данные NPC, врагов и локаций из JSON файлов.

    Returns:
        tuple: Три словаря с данными NPC, врагов и локаций.
    """

    initialize_npc_and_enemy()
    initialize_map()

    base_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории

    with open(os.path.join(base_dir, 'data/npc.json'), 'r', encoding='utf-8') as npc_file:
        data_npc = json.load(npc_file)

    with open(os.path.join(base_dir, 'data/enemy.json'), 'r', encoding='utf-8') as enemy_file:
        data_enemy = json.load(enemy_file)

    with open(os.path.join(base_dir, 'data/locations.json'), 'r', encoding='utf-8') as locations_file:
        locations_data = json.load(locations_file)

    return data_npc, data_enemy, locations_data


if __name__ == '__main__':
    load_data()