import csv
import os
import logging

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to csv file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.isfile(file_path):
            logger.error(f"Файл '{file_path}' не найден.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)

            Ingredient.objects.bulk_create(
                [
                    Ingredient(
                        name=row[0].strip(), measurement_unit=row[1].strip()
                    )
                    for row in reader
                ]
            )

        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены.'))
