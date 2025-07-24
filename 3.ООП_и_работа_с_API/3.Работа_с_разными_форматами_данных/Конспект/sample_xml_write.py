import xml.etree.ElementTree as ET
xml_str = '<root><channel type="dict"><title type="str">Дайджест новостей о python</title><link type="str">https://pythondigest.ru/</link></channel></root>'
root = ET.fromstring(xml_str)
tree = ET.ElementTree(root)
tree.write("files/sample1.xml", encoding="utf-8")

import xmlformatter
# создаем formatter и задаем параметры форматирования
formatter = xmlformatter.Formatter(indent="2", indent_char=" ")

# форматируем. не забудьте указать кодировку!
prettyxml = formatter.format_string(ET.tostring(root)).decode("utf-8")

# записываем получившийся результат как текст
with open("files/sample2.xml", "w", encoding="utf-8") as f:
	f.write(prettyxml)
