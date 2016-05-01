from os import path

from django.conf import settings
from django.core.management.base import BaseCommand

import requests


USDA_API_TOKEN = "0VGQXHrIcK7cO8MTZYg3HlKoDfizFdHNw5qQNtOM"
USDA_API_URL = "http://api.nal.usda.gov/ndb/list"
DATA_FILE = path.join(settings.BASE_DIR, 'pg_trgm',
                      'migrations', 'data', 'food_names.txt')


def get_foodlist_page(offset=0, count=50):
    params = {
        "format": "json",
        "api_key": USDA_API_TOKEN,
        "sort": "id",
        "lt": "f",
        "offset": offset,
        "max": count,
    }
    return requests.get(USDA_API_URL, params).json()


def get_food_names(num=10000):
    per_page = 50
    offset = 0
    for _ in range(num / per_page + 1):
        page = get_foodlist_page(offset, per_page)
        offset += per_page
        for item in page['list']['item']:
            yield item['name']


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(DATA_FILE, 'w') as data_file:
            for name in get_food_names():
                data_file.write(name + '\n')
