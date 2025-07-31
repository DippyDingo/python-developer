# Задание - "Переводчик"

import requests

url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
token = ''

def translate_word(word):
    """
    Функция для перевода русского слова на английский язык
    используя Yandex Dictionary API

    Args:
        word (str): Русское слово для перевода

    Returns:
        str: Переведенное английское слово
    """
    params =  {
        'key':token,
        'lang':'ru-en',
        'text': word
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get('def') and len(data['def']) > 0:
            first_definition = data['def'][0]

            if first_definition.get('tr') and len(first_definition['tr']) > 0:
                first_definition = first_definition['tr'][0]
                return first_definition['text']
        else:
            return f"Перевод для слова '{word}' не найден"

    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    except KeyError as e:
        return f"Ошибка в структуре ответа: {e}"
    except Exception as e:
        return f"Неожиданная ошибка: {e}"

if __name__ == '__main__':
    word = 'машина'
    result = translate_word(word)
    print(f"Перевод слова '{word}': {result}")
    assert translate_word(word) == 'car'