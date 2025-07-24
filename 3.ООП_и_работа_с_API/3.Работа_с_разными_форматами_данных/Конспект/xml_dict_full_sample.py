# ================================
# ПРЕОБРАЗОВАНИЕ dict в xml
# ================================
# 1) при помощи dicttoxml преобразуем dict в текст в формате binary string
# 2) преобразуем binary string в string при помощи str.decode()
# 3) преобразуем строку в XML дерево при помощи функции ET.fromstring()
# https://pypi.org/project/dicttoxml/ pip install dicttoxml
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml

json_data = {"channel": {"title": "Дайджест новостей о python", 
							"link": "https://pythondigest.ru/"}}

xml = dicttoxml(json_data) # dict в binary string
root = ET.fromstring(xml.decode("utf-8")) # binary string в string
# проверяем, что все хорошо с нашим xml (выводим заголовки новостей так же, как делали раньше)
# у нас будет только один title - "Дайджест новостей о python"
titles_list = root.findall("channel/title")
for title in titles_list:
	print(title.text)

# внимание! в этом случае мы сразу получаем root, не получая дерево XML
# чтобы получить дерево XML (например, для сохранения XML в файл):
tree = ET.ElementTree(root)
tree.write("sample2.xml", encoding="utf-8")

# https://replit.com/@shorstko/netologyxmldictfullsample#main.py

# ================================
# ПРЕОБРАЗОВАНИЕ XML в dict
# ================================
# самый удобный способ - подключить defaultdict из модуля collections
# и написать собственную функцию конверсии https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary
from collections import defaultdict
import json

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

# читаем XML в дерево, получаем root дерева
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse("sample.xml", parser)
root = tree.getroot()
# преобразуем root в dict
json_data = etree_to_dict(root)
with open("sample3.json", "w", encoding="utf-8") as f:
	json.dump(json_data, f, ensure_ascii=False, indent=2)
