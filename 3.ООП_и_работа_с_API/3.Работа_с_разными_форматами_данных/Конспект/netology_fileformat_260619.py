#!/usr/bin/env python
# coding: utf-8

# In[23]:


import csv

# чтение csv построчно
with open(r"d:\temp\files\newsafr.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count > 0:
            print(type(row), row[-1])
        count += 1

print(f"В этом файле {count-1} новостей")


# In[45]:


import csv

# чтение csv целиком
with open(r"d:\temp\files\newsafr.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    news_list = list(reader)

# [ [title], [Израильский турист], []], ...]

# print(type(news_list))
# print(news_list[0])
# print(news_list[1])

header = news_list.pop(0)
print(header)
print(news_list[0])

print(f"В этом файле {len(news_list)} новостей")

for row in news_list:
    print(row[-1])


def read_csv(file):
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        news_list = list(reader)
    return news_list

result = read_csv(r"d:\temp\files\newsafr.csv")
print(len(result))


# In[51]:


import csv

# чтение csv в словарь
with open(r"d:\temp\files\newsafr.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(type(row), row)
        print(row["title"])


# In[103]:


import csv

# чтение csv целиком
with open(r"d:\temp\files\newsafr.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    news_list = list(reader)

header = news_list.pop(0)
# print(header)

csv.register_dialect("csv_comma_no_quoting", delimiter=",", quoting=csv.QUOTE_NONE, escapechar="\\")
csv.register_dialect("csv_semicolon_quote_all", delimiter=";", quoting=csv.QUOTE_ALL)

# запись csv в файл
with open(r"d:\temp\files\result.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, dialect="csv_semicolon_quote_all")
    # print(type(header), header)
    writer.writerow(header)
    writer.writerows(news_list[:2])


# with open(r"d:\temp\files\result.csv", encoding="utf-8", newline="") as f:
#     reader = csv.reader(f, escapechar="\\")
#     for row in reader:
#         print(row)


# In[135]:


import json
from pprint import pprint

with open(r"d:\temp\files\newsafr.json", encoding="utf-8") as f:
    json_data = json.load(f)

print(type(json_data))
# pprint(json_data)
news_list = json_data["rss"]["channel"]["items"]
# print(f"В этом файле {len(news_list)} новостей")

# for row in news_list:
#     print(row["title"])

with open(r"d:\temp\files\result.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

news = json_data["rss"]["channel"]["items"][0]
# print(type(news), news)

json_str = json.dumps(news, ensure_ascii=False)
print(type(json_str), json_str)

json_data2 = json.loads(json_str)
print(type(json_data2), json_data2)


# In[163]:


import xml.etree.ElementTree as ET

# создаем парсер XML. парсеру обязательно задаем кодировку
parser = ET.XMLParser(encoding="utf-8")
# parser = xml.etree.ElementTree.XMLParser(encoding="utf-8")
# превращаем исходный текстовый файл sample.xml в дерево XML
tree = ET.parse(r"d:\temp\files\newsafr.xml", parser)
print(tree)

root = tree.getroot()
print(root)
print(root.tag, root.text, root.attrib)

news_list = root.findall("channel/item")
print(f"В этом файле {len(news_list)} новостей")

# for row in news_list:
#     title = row.find("title")
#     print(title.text)

# XPath

titles_list = root.findall("channel/item/title")
for title in titles_list:
    print(title.text)


tree.write(r"d:\temp\files\result.xml", encoding="utf-8")


# In[ ]:




