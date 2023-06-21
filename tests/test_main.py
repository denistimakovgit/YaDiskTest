from unittest import TestCase
import requests
from main import YaUploader
import configparser

class CreateFolderTestcase(TestCase):

    def get_headers(self):
        settings_path = 'Settings.ini'  #указываем путь к файлу, хранящему токен к Я.диску

        # Получаем токен для Яндекс.Диск из файла
        config = configparser.ConfigParser()  # создаём объект парсера
        config.read(settings_path)
        self.ya_token = config['DEFAULT']['ya_token']

        return {
            "Content-Type": "application/json",
            "Authorization": "OAuth {}".format(self.ya_token)
        }

    def test_correct_status_code(self):
        """
        Проверка успешности создания директории (200 статус)
        """
        expected_status = 200
        headers = self.get_headers()

        uploader = YaUploader()
        result = uploader.create_folder()

        test_url = "https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2FPython_Timakov"
        request_status = requests.get(test_url, headers=headers)

        self.assertEqual(request_status.status_code, expected_status)

    def test_exist_foder(self):
        """
        Проверка на создание директории с указанным именем Python_Timakov
        """
        expected_folder_name = 'Python_Timakov'
        check_url = "https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F"
        headers = self.get_headers()
        test = requests.get(check_url, headers=headers).json()
        folder_names = []
        for elem in test["_embedded"]["items"]:
            folder_names.append(elem['name'])

        self.assertIn(expected_folder_name, folder_names)

    def test_negative_auth(self):
        """
        Проверка авторизации на Яндекс.Диск при создании папки (ошибка токена)
        """
        expected_description = "Unauthorized"
        params_list = []
        uploader = YaUploader()
        result = uploader.create_folder()

        for key, value in result.items():
            params_list.append(value)
        self.assertNotIn(expected_description, params_list)