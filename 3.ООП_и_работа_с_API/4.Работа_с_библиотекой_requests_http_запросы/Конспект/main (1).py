# pip install requests

import requests

import json
from pprint import pprint

from tokens import yd_token

url = ''
response = ''

# Получить страницу сайта и сохранить

# url = 'https://ru.wikipedia.org/wiki/HTTP'
# response = requests.get(url)
# # print(response)
# # if 200 <= response.status_code < 300:
# #     pass
# # print(response.status_code)
# # pprint(response.headers)
# # print(response.text)
# with open('index.html', 'w') as f:
#     f.write(response.text)


# заполнить анкету

# url = 'https://functions.yandexcloud.net/d4e8qsrmeednndemfsus'
# payload = {
#     "name": "тимур",
#     "surname": "тимур",
#     "patronymic": "Отсутствует",
#     "telephone": "+7(124)124-12-42",
#     "birthdate": "2000-05-23",
#     "passport": "2352 35235236"
# }
# # headers = {
# #     'Content-type': 'application/json'
# # }
#
# # response = requests.post(url,
# #                          headers=headers,
# #                          data=json.dumps(payload))
#
# response = requests.post(url, json=payload)
# print(response.json())


# 1) сходить на сервер НАСА и получить инфу о картинке дня
# 2) скачать картинку на компьютер
# 3) сходить на яндекс-диск и создать папку для хранения картинок
# 4) загрузить картинку в эту папку

# # 1) сходить на сервер НАСА и получить инфу о картинке дня
#
# url_nasa = 'https://api.nasa.gov/planetary/apod'
# params = {
#     'api_key': 'ZDRRhoU8Fl4uD2qzA1aN0hXrq5buYG3zZclnbmw9',
#     'date': '2025-06-19'
# }
# response = requests.get(url_nasa, params=params)
# image_url = response.json()['url']
# filename = image_url.split('/')[-1]
#
# # 2) скачать картинку на компьютер
#
# response = requests.get(image_url)
# with open(f'images/{filename}', 'wb') as f:
#     f.write(response.content)
#
#
# # 3) сходить на яндекс-диск и создать папку для хранения картинок
#
# url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
# params = {
#     'path': 'Nasa'
# }
# headers = {
#     'Authorization': f'OAuth {yd_token}'
# }
# response = requests.put(url_create_folder,
#                         params=params,
#                         headers=headers)
#
# # 4) загрузить картинку в эту папку
#
# url_upload_link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
# params = {
#     'path': f'Nasa/{filename}'
# }
# response = requests.get(url_upload_link,
#                         params=params,
#                         headers=headers)
# url_upload = response.json()['href']
#
# with open(f'images/{filename}', 'rb') as f:
#     requests.put(url_upload, files={'file': f})




# Домашка

# url = 'https://cdn.jsdelivr.net/gh/akabab/superh ero-api@0.3.0/api/all.json'
# heroes = requests.get(url).json()
# for hero in heroes:
#     if hero['powerstats']['durability'] == 100:
#         print(hero['name'], hero['powerstats']['durability'])


# url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
# params = {
#     'key': 'dict.1.1.20250623T191904Z.4c7a9ba57fd24d52.250a3b87afb13bdcb23c2e31b8dcde7286316daa',
#     'lang': 'ru-en',
#     'text': 'машина'
# }
# response = requests.get(url, params=params)
# print(response.json()['def'][0]['tr'][0]['text'])


# url = 'https://geocode.maps.co/reverse'
# params = {
#     'lat': '52.3727598',
#     'lon': '4.8936041',
#     'api_key': '67bc88d09e323493187631sjhf1323a',
# }
# response = requests.get(url, params=params)
# pprint(response.json()['address']['city'])


Википедия про интерфейсы: https://ru.wikipedia.org/wiki/%D0%98%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81 https://ru.wikipedia.org/wiki/%D0%98%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F https://ru.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F https://ru.wikipedia.org/wiki/API

HTTP-протокол и не только: https://habr.com/ru/articles/820419/ - модель OSI. На лекции это не стали разбирать, но хороший IT-специалист должен об этом знать. https://ru.wikipedia.org/wiki/HTTP - статья в вики https://ru.wikipedia.org/wiki/Cookie - про куки https://www.cloud4y.ru/upload/medialibrary/4c2/yt8bj40q1rh22nzkdhuc1kh1seqth33g/2.jpg - как выглядит запрос https://zametkinapolyah.ru/wp-content/uploads/2016/06/HTTP_ResponseMessageExample.png - как выглядит ответ

URL: https://ru.wikipedia.org/wiki/URL - википедия про URL https://habrastorage.org/files/373/2b3/3fd/3732b33fd43043049c18e3c108bc9d1a.jpg - схема URL посложнее https://sitechecker.pro/wp-content/uploads/2017/12/url-structure.jpg - схема URL попроще

Методы: https://avatars.mds.yandex.net/get-lpc/1527204/19bdfe55-7f57-41aa-8a15-7322b5f68475/orig

Статусы ответов: https://lh6.googleusercontent.com/5GaKAPxjAwtYK69xGChJpyuwMzzoBLTEp2oTQn_o861QK_8AlTRsDcNcXypWMXd953k_VTfP5-DcSpZpf66TfhoPRaEVRfMoD6JgBpRvTSC1pdyaz10A37xi_7-ATg6skKm4JzAFGPzpJaCrPTCSLH1z2nu68X-kuClemdHWiVL5BXd1XR9KrGhfaG2cmA

Форма из лекции: https://sinsl.github.io/testing-form/

API Яндекс-диска: https://yandex.ru/dev/disk/poligon/ - Здесь получаете токен и смотрите Swagger яндекса https://yandex.ru/dev/disk/api/concepts/about.html - документация по работе с API яндекс диска.

Пример Swagger'а: https://petstore.swagger.io/#/

Интересные/веселые открытые API, которые можно самостоятельно поизучать: https://open-meteo.com/en/docs https://api.nasa.gov/ https://spoonacular.com/food-api

Блог на хабре (всем бежать читать): https://habr.com/ru/users/Molechka/posts/ https://habr.com/ru/articles/524288/ - что такое XML https://habr.com/ru/articles/554274/ - что такое JSON https://habr.com/ru/post/464261/ - cтатья про API https://habr.com/ru/post/704090/ - как тестировать API https://habr.com/ru/articles/770226/ - спорные вопросы про REST API

Различия между SOAP и REST: https://habr.com/ru/post/483204/ https://appmaster.io/ru/blog/mylo-protiv-otdykha https://medium.com/@kamolanuritdinova/rest-vs-soap-d1d9335b5f81

Про идемпотентность методов: https://developer.mozilla.org/ru/docs/Glossary/Idempotent









