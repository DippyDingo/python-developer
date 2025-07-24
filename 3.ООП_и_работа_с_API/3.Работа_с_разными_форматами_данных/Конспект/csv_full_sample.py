# https://replit.com/@shorstko/netologycsvfullsample#main.py

import csv

# ======================================
# ЧТЕНИЕ CSV
# ======================================
# вариант 1 - csv.reader
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.reader(f)
	for row in reader:
		print(row[-1])

# вариант 2 - csv.reader + list. только для небольших файлов!
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.reader(f)
	news_list = list(reader)

header = news_list.pop(0)
for news in news_list:
	print(news[-1])

# вариант 3 - csv.DictReader
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.DictReader(f)
	for row in reader:
		print(row["title"])
	
# ======================================
# ЗАПИСЬ CSV - csv.writer
# ======================================
# предварительно прочитаем данные
# данные будут храниться в news_list
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.reader(f)
	news_list = list(reader)

# вариант 1 - csv.writer и "w" (перезапись файла)
with open("sample2.csv", "w", encoding="utf-8", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(news_list[0]) # запись одной строки данных
	writer.writerows(news_list) # запись нескольких строк данных

# вариант 2 - csv.writer и "a" (добавление записей в существующий файл)
# добавим в файл sample2.csv еще несколько строк данных
with open("sample2.csv", "a", encoding="utf-8", newline="") as f:
	writer = csv.writer(f)
	writer.writerows(news_list[:3])

# ======================================
# ЗАПИСЬ CSV - csv.DictWriter
# ======================================
# предварительно прочитаем данные при помощи DictReader
# данные хранятся в reader
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.DictReader(f)

	# запишем данные в новый файл sample_d.csv
	with open("sample_d.csv", "w", encoding="utf-8", newline="") as f:
		# необходимо передать ключи из DictReader: fieldnames=reader.fieldnames
		writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
		writer.writeheader() # записываем заголовок файла (ключи DictReader)
		for row in reader:
			# изменим данные: пусть все заголовки новостей будут прописными (большими) буквами
			row["title"] = row["title"].upper()
			writer.writerow(row) # записываем получившуюся строку данных в файл

# как получить ключи из DictReader:
with open("sample.csv", encoding="utf-8", newline="") as f:
	reader = csv.DictReader(f)
	# получаем ключи из reader
	keys = reader.fieldnames
	# преобразуем ключи из reader в обычный список: 
	keys_list = list(keys)
	print(keys_list)
			
# ======================================
# НАСТРОЙКИ - ДИАЛЕКТЫ
csv.register_dialect('customcsv', delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
with open("sample4.csv", "w", encoding="utf-8", newline="") as f:
	writer = csv.writer(f, dialect="customcsv")
	writer.writerows(news_list)