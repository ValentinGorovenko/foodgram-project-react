from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    TAGS_DATA = [
        {'name': 'Завтрак', 'color': '#70A3E2', 'slug': 'breakfast'},
        {'name': 'Обед', 'color': '#E2350A', 'slug': 'lunch'},
        {'name': 'Ужин', 'color': '#162BE2', 'slug': 'dinner'},
    ]

    def handle(self, *args, **kwargs):
        self.load_tags()

    def load_tags(self):
        bulk_tags = [Tag(**tag) for tag in self.TAGS_DATA]
        Tag.objects.bulk_create(bulk_tags)
        self.stdout.write(self.style.SUCCESS('Тэги загружены.'))
