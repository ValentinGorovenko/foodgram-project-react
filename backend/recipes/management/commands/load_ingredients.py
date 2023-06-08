import csv
import os

from django.core.management.base import BaseCommand
from foodgram import settings
from recipes.models import Ingredient


def ingredient_create(row):
    Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Ingredient(name=row[0], measurement_unit=row[1])
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены.'))
