import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    """
    Добавляем ингредиенты из файла CSV
    """
    help = 'загрузка из csv файла'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/ingredient.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)

            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)

        return (
            f'{Ingredient.objects.count()} - ингредиентов успешно загружено')
