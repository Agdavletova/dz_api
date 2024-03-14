import json
from pprint import pprint

import requests

APP_ID = '51868951'
access_token = ""
class VK:


    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,'album_id': 'profile', 'extended':1, 'photo_sizes': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'
class YANDEX:

    def __init__(self, yandex_token):
        self.yandex_token = yandex_token
        # self.id = user_id
        # self.version = version
        self.headers = {'Accept': 'application/json', 'Authorization': yandex_token}

# получение ифнормации о диске
    def get_info_disk(self):
        response = requests.get(BASE_URL, headers=self.headers)
        return response.json()

# создание папки
    def create_resourse(self):
        path = 'Photos_VK'
        url = f'{BASE_URL}resources'
        params = {'path': path}
        response = requests.put(url,params=params, headers=self.headers)
        return response

    def upload_photos(self):
        file = vk.get_photos().get('response').get('items')[0].get('sizes')[-1].get('url')
        # file = "https://sun9-27.userapi.com/impf/5SUc_DEu4LauiTPoHB7SzPw56getZHzMU9iUtg/a3k8Xzy-9UA.jpg?size=562x562&quality=96&sign=428c164dbdc0485595a51d108b1064d7&c_uniq_tag=JxJqPYy6XQ4wuUvyFOLr1V9cXlipBBjwafGHm7yqa1o&type=album"
        url = f"{BASE_URL}/resources/upload"
        data = {'path':'/Photos_VK/11111.jpg', 'url': file}
        response = requests.post(url, data=data, headers=self.headers)
        return response

user_id = '329645286'
vk = VK(access_token, user_id)
yandex_token = ""
# pprint(vk.get_photos())
client = YANDEX(yandex_token)
client.create_resourse()
pprint(client.upload_photos())