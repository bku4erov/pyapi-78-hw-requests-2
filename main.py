import os
from pprint import pprint

import requests


class YaUploader:
    
    base_url = 'https://cloud-api.yandex.net/v1/disk/'
    
    def __init__(self, token: str):
        self.token = token
    
    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        return headers

    def upload(self, file_path: str):
        """Метод загружает файл, путь к которому указан в file_path, на яндекс диск"""
        url_get_upload_url = YaUploader.base_url + 'resources/upload'
        file_name = os.path.basename(file_path)
        upload_url = requests.get(url_get_upload_url, params={'path': file_name, 'overwrite': True}, headers=self.get_headers())
        # pprint(upload_url.json())
        if upload_url.status_code != 200:
            return f'Something went wrong during getting upload url:\n {upload_url}!\n{upload_url.json()}'
        upload_href = upload_url.json()['href']
        res = requests.put(upload_href, data=open(file_path, 'rb'))
        # print(type(res), res)
        if res.status_code == 201:
            return 'File was successfully uploadad'
        else:
            return f'Something went wrong during uploading file:\n {res}!'


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input('Введите путь к файлу для загрузки на Яндекс.Диск: ')
    token = input('Введите токен для обращения к Яндекс.Диску: ')
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
    print(result)