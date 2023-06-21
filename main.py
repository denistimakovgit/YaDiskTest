import requests
import configparser

class YaUploader:

    def get_headers(self):
        settings_path = 'Settings.ini'
        # Получаем токен для Яндекс.Диск из файла
        config = configparser.ConfigParser()  # создаём объект парсера
        config.read(settings_path)
        self.ya_token = config['DEFAULT']['ya_token']

        return {
            "Content-Type": "application/json",
            "Authorization": "OAuth {}".format(self.ya_token)
        }

    def create_folder(self):
        """
        Метод создания папки на Яндекс.Диск
        """
        headers = self.get_headers()
        params = {"path": "Python_Timakov", "overwrite": "true"}

        #Удалаяем папку с именем Python_Timakov если она существует
        del_url = "https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2FPython_Timakov&permanently=true"
        del_dir = requests.delete(del_url, headers=headers)

        #создаем папку с именем Python_Timakov
        create_url = "https://cloud-api.yandex.net/v1/disk/resources"
        response = requests.put(create_url, headers=headers, params=params)
        result = response.json()

        return result

if __name__ == '__main__':

    uploader = YaUploader()
    result = uploader.create_folder()