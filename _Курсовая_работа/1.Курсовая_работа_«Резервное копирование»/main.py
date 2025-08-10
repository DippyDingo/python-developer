import requests
import json
from tqdm import tqdm


class YDConnector:
    """Класс для работы с REST API Яндекс.Диска через OAuth-токен."""

    def __init__(self, token: str):
        self.headers = {"Authorization": f"OAuth {token}"}
        self.base_url = "https://cloud-api.yandex.net/v1/disk/"

    def create_folder(self, path: str):
        """Создает папку на Яндекс.Диске, если её еще нет."""
        url = f"{self.base_url}resources"
        response = requests.put(url, headers=self.headers, params={"path": path})
        if response.status_code == 409:
            print(f"Папка '{path}' уже существует на Яндекс.Диске.")
        else:
            response.raise_for_status()

    def get_upload_link(self, path: str) -> str:
        """Получает ссылку для загрузки файла на Яндекс.Диск."""
        url = f"{self.base_url}resources/upload"
        params = {"path": path, "overwrite": "true"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["href"]

    def upload_file(self, upload_url: str, file_data: bytes):
        """Загружает файл по временной ссылке upload_url."""
        response = requests.put(upload_url, data=file_data)
        response.raise_for_status()


def get_cat_image(text: str) -> bytes:
    """Запрашивает у cataas.com картинку кота с заданным текстом."""
    url = f"https://cataas.com/cat/says/{text}"
    response = requests.get(url)
    response.raise_for_status()
    return response.content


class CatUploader:
    """Класс для получения и загрузки на Яндекс.Диск картинок с котами с текстом."""

    def __init__(self, yd_token: str, group_folder: str):
        self.yd_connector = YDConnector(yd_token)
        self.group_folder = group_folder
        self.uploaded_files_info = []

    def run(self, texts: list):
        """Создает папку и поочередно загружает картинки с текстами из списка с прогресс-баром."""
        print(f"Создаем папку '{self.group_folder}' на Яндекс.Диске...")
        self.yd_connector.create_folder(self.group_folder)

        print("Начинаем загрузку картинок...")
        for text in tqdm(texts, desc="Загрузка картинок", unit="шт"):
            image_data = get_cat_image(text)
            size_bytes = len(image_data)
            filename = f"{text}.jpg"
            yd_path = f"{self.group_folder}/{filename}"

            upload_url = self.yd_connector.get_upload_link(yd_path)
            self.yd_connector.upload_file(upload_url, image_data)

            self.uploaded_files_info.append({
                "file_name": yd_path,
                "text": text,
                "size_bytes": size_bytes
            })

    def save_info(self, json_filename='uploaded_files_info.json'):
        """Сохраняет информацию о загруженных файлах в локальный JSON-файл."""
        with open(json_filename, 'w', encoding='utf-8') as f_json:
            json.dump(self.uploaded_files_info, f_json, ensure_ascii=False, indent=4)
        print(f"Информация о загруженных файлах сохранена в {json_filename}")

def main():
    import configparser

    config = configparser.ConfigParser()
    config.read('settings.ini')

    group_name = config['settings']['group_name']
    yd_token = config['tokens']['yd_token']

    texts = []
    print("Введите тексты для картинок (каждый с новой строки). Для окончания ввода оставьте пустую строку.")
    while True:
        line = input("Текст для картинки: ").strip()
        if not line:
            break
        texts.append(line)

    if not texts:
        print("Ошибка: не введен ни один текст. Завершаем.")
        return
    if not yd_token:
        print("Ошибка: токен в config отсутствует. Завершаем.")
        return

    uploader = CatUploader(yd_token, group_name)
    uploader.run(texts)
    uploader.save_info()

if __name__ == "__main__":
    main()