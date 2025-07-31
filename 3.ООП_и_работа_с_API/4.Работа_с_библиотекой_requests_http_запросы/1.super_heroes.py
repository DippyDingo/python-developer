import requests
from pprint import pprint
# мое решение
def get_the_smartest_superhero() -> str:
    the_smartest_superhero = ''
    url = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
    response = requests.get(url).json()

    target_heroes = ["Hulk", "Captain America", "Thanos"]
    hero_intelligence = {}
    for hero in response:
        if hero['name'] in target_heroes:
            intelligence = hero['powerstats'].get('intelligence', 0)
            hero_intelligence[hero['name']] = intelligence

    if hero_intelligence:
        the_smartest_superhero = max(hero_intelligence, key=hero_intelligence.get)
        return the_smartest_superhero
    else:
        return "Ни один из героев не найден"

# Решение эксперта
def get_the_smartest_superhero_2() -> str:
    # URL API для получения данных о всех супергероях
    url = "https://akabab.github.io/superhero-api/api/all.json"
    # Отправляем GET-запрос к API
    response = requests.get(url)
    # Преобразуем ответ в формат JSON
    heroes = response.json()

    # Список супергероев, среди которых нужно найти самого умного
    target_heroes = ['Hulk', 'Captain America', 'Thanos']
    # Словарь для хранения пар "имя супергероя: уровень интеллекта"
    hero_intelligence = {}

    # Проходим по всем супергероям из API
    for hero in heroes:
        # Если текущий супергерой есть в нашем списке
        if hero['name'] in target_heroes:
            # Добавляем в словарь пару "имя: уровень интеллекта"
            hero_intelligence[hero['name']] = hero['powerstats']['intelligence']

    # Находим супергероя с максимальным значением интеллекта
    # max() возвращает пару (имя, интеллект), [0] берет только имя
    the_smartest_superhero = max(hero_intelligence.items(), key=lambda x: x[1])[0]
    return the_smartest_superhero

# мое решение
def get_the_smartest_superhero_3(superheros):
    max_intelligence = -1
    smartest_name = ''  # имя героя
    base_url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/id/{}.json"

    for hero_id in superheros:
        try:
            url = base_url.format(hero_id)
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            powerstats = data.get("powerstats", {})

            intelligence = powerstats.get("intelligence", 0)
            try:
                int_value = int(intelligence) if intelligence is not None else 0
            except (TypeError, ValueError):
                int_value = 0

            # Обновляем максимум только если нашли большее значение
            if int_value > max_intelligence:
                max_intelligence = int_value
                smartest_name = data.get("name", "")  # Сохраняем имя героя

        except requests.exceptions.RequestException:
            continue  # Пропускаем проблемных героев

    return smartest_name

# Решение эксперта
def get_the_smartest_superhero(superheros):
    # Создаем словарь для хранения пар "имя супергероя: уровень интеллекта"
    hero_intelligence = {}

    # Проходим по каждому ID супергероя в списке
    for hero_id in superheros:
        # Формируем URL для получения информации о конкретном супергерое
        url = f"https://akabab.github.io/superhero-api/api/id/{hero_id}.json"

        # Отправляем GET-запрос к API
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Преобразуем ответ в формат JSON
            hero_data = response.json()

            # Получаем имя и уровень интеллекта супергероя
            hero_name = hero_data['name']
            intelligence = hero_data['powerstats']['intelligence']

            # Добавляем в словарь пару "имя: уровень интеллекта"
            hero_intelligence[hero_name] = intelligence

    # Находим супергероя с максимальным значением интеллекта
    # max() возвращает пару (имя, интеллект), [0] берет только имя
    the_smartest_superhero = max(hero_intelligence.items(), key=lambda x: x[1])[0]

    return the_smartest_superhero
if __name__ == '__main__':
    print(get_the_smartest_superhero())
    print(get_the_smartest_superhero_2())
