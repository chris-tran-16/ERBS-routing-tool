import requests
from typing import List
import json
from time import sleep
from src.util.util import check_dir


class DataFetcher:
    BASE_URL = 'https://open-api.bser.io'

    def __init__(self, api_key: str = None, version: str = 'v1'):
        self.api_key = api_key
        self.version = version

    @property
    def api_url(self) -> str:
        return f'{self.BASE_URL}/{self.version}'

    @property
    def header_data(self) -> dict:
        return {
            'Accept': 'application/json',
            'X-Api-Key': self.api_key,
        }

    def fetch_meta_data(self, meta_type: str = 'hash') -> List[dict]:
        url = f'{self.api_url}/data/{meta_type}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get('data', [])

    def read_api_key(self, file):
        f = open(file, "r")
        self.api_key = f.read()
        f.close()

    def set_api_key(self, key):
        self.api_key = key

    def dump_items_to_folder(self, folder="data"):
        items = {
            "ItemArmor": "armor",
            "ItemWeapon": "weapons",
            "ItemSpawn": "spawn",
            "ItemConsumable": "consumable",
            "ItemMisc": "misc",
            "ItemSpecial": "special",
        }
        check_dir(folder)
        for item in items:
            data = self.fetch_meta_data(item)
            with open(f"{folder}/{items[item]}.json", "w") as fout:
                json.dump(data, fout)
            sleep(2)

    def fetch_english_data(self):
        request_url = "http://api.playeternalreturn.com/aesop/item/all"
        response = requests.get(request_url)

        return response.json()

    def dump_english_items(self, folder="data"):
        response = self.fetch_english_data()
        with open(f"{folder}/english_items.json", "w") as fout:
            json.dump(response, fout)
