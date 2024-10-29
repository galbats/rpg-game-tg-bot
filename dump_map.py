import json


def initialize_map():
    # Для локаций
    locations_data = {
    "Средиземье": "Это базовая локация достаточно дружелюбна и неприхотлива",
    "Лето": "Летняя локация - благоприятно влияет на вас и отрицательно на врагов. Показатель атаки врагов снижен на 1.",
    "Зима": "Зимняя локация - суровая местность. Показатель атаки врагов увеличен на 1."
    }


    with open('data/locations.json', 'w', encoding='utf-8') as map_locations:
        json.dump(locations_data, map_locations, ensure_ascii=False, indent=4)

