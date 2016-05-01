# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import path

from django.db import migrations
from django.conf import settings


DATA_FILE_PATH = path.join(
    settings.BASE_DIR, 'pg_trgm', 'migrations', 'data',
    'food_names.txt',
)


def get_food_names():
    with open(DATA_FILE_PATH) as data_file:
        for line in data_file:
            yield line.strip()


def load_foods(apps, schema_editor):
    Food = apps.get_model('pg_trgm', 'Food')
    Food.objects.bulk_create((
        Food(name=name) for name in get_food_names()
    ), batch_size=2000)


def delete_foods(apps, schema_editor):
    Food = apps.get_model('pg_trgm', 'Food')
    Food.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pg_trgm', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_foods, delete_foods)
    ]
