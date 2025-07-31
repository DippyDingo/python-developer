# Задание «Куда поедем в отпуск?»
import requests
import time      # Для функции sleep

# Список популярных городов Великобритании
POPULAR_UK_CITIES = [
    'Leeds', 'London', 'Liverpool', 'Manchester',
    'Oxford', 'Edinburgh', 'Norwich', 'York'
]

API_KEY = '' # https://geocode.maps.co/

def find_uk_city(coordinates: list) -> str:
    """
    Функция принимает список координат ([(lat, lon), ...])
    и возвращает первый город из списка POPULAR_UK_CITIES, найденный по координатам через API geocode.maps.co.
    """
    for lat, lon in coordinates:
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'api_key': API_KEY
            }
            response = requests.get('https://geocode.maps.co/reverse', params=params)
            response.raise_for_status()

            data = response.json()
            address = data.get('address', {})

            # Ищем название города в разных подходящих полях
            city = (address.get('city')
                or address.get('town')
                or address.get('village')
                or address.get('hamlet'))

            if city in POPULAR_UK_CITIES:
                return city

        except requests.RequestException as e:
            print(f"Ошибка запроса для координат ({lat}, {lon}): {e}")

        # Задержка в 1 сек
        time.sleep(1)

    return ''  # Если не найден город в списке

if __name__ == '__main__':
    _coordinates = [
        ('55.7514952', '37.618153095505875'),  # Москва
        ('52.3727598', '4.8936041'),          # Амстердам
        ('53.4071991', '-2.99168')            # Ливерпуль
    ]

    result = find_uk_city(_coordinates)
    print(result)  # Ожидается: Liverpool
    assert result == 'Liverpool'
