import xml.etree.ElementTree as ET
from collections import Counter
from pprint import pprint

def read_xml(file_path, word_min_len=7, top_words_amt=10):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(file_path, parser)
    root = tree.getroot()

    desc_texts = root.findall("channel/item/description")
    all_text = " ".join(desc.text for desc in desc_texts if desc.text)

    words = all_text.split()
    filtered = [word for word in words if len(word) >= word_min_len]

    counter = Counter(filtered)
    most_common_words = [word for word, count in counter.most_common(top_words_amt)]

    return most_common_words


if __name__ == '__main__':
    print(read_xml('newsafr.xml'))
