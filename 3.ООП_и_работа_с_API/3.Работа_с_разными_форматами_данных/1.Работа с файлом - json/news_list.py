import json


def read_json(file_path, word_min_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_text = " ".join(item["description"] for item in data["rss"]["channel"]["items"])

    words = all_text.split()
    filtered_words = [word for word in words if len(word) >= 7]

    # Подсчитываем частоту слов
    word_counts = {}
    for word in filtered_words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Сортируем слова по частоте (по убыванию) и берем топ-10
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    top_words = [word for word, count in sorted_words[:10]]

    return top_words


if __name__ == '__main__':
    print(read_json('newsafr.json'))