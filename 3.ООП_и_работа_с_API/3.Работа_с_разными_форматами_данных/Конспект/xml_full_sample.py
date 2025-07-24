# https://replit.com/@shorstko/netologyxmlfullsample#main.py

# чтение и запись XML
# подключаем библиотеку xml и из нее импортируем ElementTree
# чтобы каждый раз не писать etree.ElementTree - назначаем алиас (короткое имя) ET
import xml.etree.ElementTree as ET

# ======================================
# ЧТЕНИЕ XML ИЗ ФАЙЛА
# ======================================
# создаем парсер XML. парсеру обязательно задаем кодировку
parser = ET.XMLParser(encoding="utf-8")
# превращаем исходный текстовый файл sample.xml в дерево XML
tree = ET.parse("sample.xml", parser)

# посмотрим на наше дерево и увидим примерно такой объект:
# <xml.etree.ElementTree.ElementTree object at 0x7f3602e9ffd0>
print(tree)

# для работы с деревом XML нужно получить его корень - root
root = tree.getroot()
print(root.tag) # имя тега для root
print(root.text) # текст root (если ничего нет, выводится пустая строка)
print(root.attrib) # атрибуты root. если они есть, выводится dict

# ======================================
# ЧТЕНИЕ XML ИЗ СТРОКИ
# ======================================
# строка, содержащая XML:
xml_str = '<root><channel type="dict"><title type="str">Дайджест новостей о python</title><link type="str">https://pythondigest.ru/</link></channel></root>'

# превращаем строку в XML. внимание! в этом случае мы получаем не дерево, а сразу корень!
root = ET.fromstring(xml_str)
# при необходимости строим дерево XML - просто преобразовываем root к типу ElementTree
tree = ET.ElementTree(root)

# ======================================
# РАБОТА С ДАННЫМИ В XML
# findall - найти все теги с указанным именем, find - найти первый по счету тег с указанным именем
# можно задавать целый "путь" к тегу, любой длины: "channel/item"
# ======================================
# прочитаем XML и получим root
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse("sample.xml", parser)
root = tree.getroot()

# ищем все теги item (внутри которых находятся новости)
news_list = root.findall("channel/item")
print(f"В этом файле {len(news_list)} новостей")

# читаем заголовки новостей - стандартный подход (прочитать весь блок новости, найти и вывести title)
for news in news_list:
	title = news.find("title")
	print(title.text)

# читаем заголовки новостей - упрощенный подход (прочитать сразу все title)
# доступен только в XML. в CSV и JSON такого нет
titles_list = root.findall("channel/item/title")
for title in titles_list:
	print(title.text)

# ======================================
# ЗАПИСЬ XML В ФАЙЛ - БЕЗ ФОРМАТИРОВАНИЯ
# ======================================
# вариант 1 - запись через write
# обязательно задать кодировку! иначе кириллица превратится в цифры!
tree.write("sample2.xml", encoding="utf-8")

# ВНИМАНИЕ! write() пишет текст без отступов (на примере из лекции этого не видно, потому что исходный XML уже форматированный
# зато хорошо видно в этом коде:
xml_str = '<root><channel type="dict"><title type="str">Дайджест новостей о python</title><link type="str">https://pythondigest.ru/</link></channel></root>'
root = ET.fromstring(xml_str)
tree = ET.ElementTree(root)
tree.write("sample3.xml", encoding="utf-8")

# ======================================
# ЗАПИСЬ XML В ФАЙЛ - С ФОРМАТИРОВАНИЕМ
# ======================================
# вариант 2 - запись через xmlformatter
# для XML с отступами используйте модуль xmlformatter. предварительно нужно установить: pip install xmlformatter
# в параметрах Formatter'а указывается тип отступа (пробел, табулятор) и количество отступов, в качестве входного значения даем XML, сериализованный в строку
import xmlformatter

# предварительно создаем XML (например, из строки)
xml_str = '<root><channel type="dict"><title type="str">Дайджест новостей о python</title><link type="str">https://pythondigest.ru/</link></channel></root>'
root = ET.fromstring(xml_str)

# создаем formatter и задаем параметры форматирования
formatter = xmlformatter.Formatter(indent="2", indent_char=" ")

# форматируем. не забудьте указать кодировку!
prettyxml = formatter.format_string(ET.tostring(root)).decode("utf-8")

# записываем получившийся результат как текст
with open("sample4.xml", "w", encoding="utf-8") as f:
	f.write(prettyxml)


