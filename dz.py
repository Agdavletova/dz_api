import json
from pprint import pprint

import requests
import logging

#ЛОГИРОВАНИЕ
# Configure logging settings
logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Example of logging messages
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

#ID ПРИЛОЖЕНИЯ VK
APP_ID = '51868951'

class VK:


    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

# Получение списка фото с вк
    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,'album_id': 'profile', 'extended':1, 'photo_sizes': 1}
        response = requests.get(url, params={**self.params, **params})
        if response.status_code == 200 or response.status_code == 201:
            logging.info("Photos saved")
            return response.json()
        else:
            logging.error("Failed to save photo")

# Сохранение информации о фото в файл json
    def save_info_photos(self, photos_json):
        list_photos = photos_json.get('response').get('items')
        data = []
        for i in range(len(list_photos)):
            file_name = list_photos[i].get('likes').get('count')
            file_url = list_photos[i].get('sizes')[-1].get('url')
            file_size = {'height': list_photos[i].get('sizes')[-1].get('height'), 'width': list_photos[i].get('sizes')[-1].get('width')}
            d = {'file name':file_name, 'file url': file_url, 'file_size':file_size}
            data.append(d)
        with open('info_photos.json', 'w') as file:
            json.dump(data, file, indent=4)
        logging.info("Photos are saved to the file info_photos.json")


BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'
class YANDEX:

    def __init__(self, yandex_token):
        self.yandex_token = yandex_token
        # self.id = user_id
        # self.version = version
        self.headers = {'Accept': 'application/json', 'Authorization': yandex_token}

# создание папки
    def create_resourse(self):
        path = 'Photos_VK'
        url = f'{BASE_URL}resources'
        params = {'path': path}
        response = requests.put(url,params=params, headers=self.headers)
        if response.status_code == 200 or response.status_code == 201:
            logging.info('Folder created')
            return True
        elif response.status_code == 409:
            logging.warning("A folder with the same name already exists")
            return True
        elif response.status_code == 401:
            logging.error("User is not authorized")
            return False

# Загрузка файлов на яндекс диск
    def upload_photos(self, n=5):
        if self.create_resourse():
            url = f"{BASE_URL}resources/upload"
            with open('info_photos.json', 'r') as f:
                data_photos = json.load(f)
            for i in range(len(data_photos)):
                data = {'path': f"/Photos_VK/count_likes-    {data_photos[i].get('file name')}.jpg", 'url': data_photos[i].get('file url')}
                response = requests.post(url, params=data, headers=self.headers)
                if response.status_code == 202:
                    logging.info("Photo uploaded")
                elif response.status_code == 401:
                    logging.error("User is not authorized")
                if i >= n-1:
                    break

user_id = 'Your vk id'
access_token = "Your VK token"
vk = VK(access_token, user_id)
yandex_token = 'Your Yandex token'

photos_json = vk.get_photos() # скачиваем фото с вк
vk.save_info_photos(photos_json) # сохраняем информацию о фото в файл json

client = YANDEX(yandex_token)

pprint(client.upload_photos(4)) # загружаем фото из файла json  на яндекс диск
