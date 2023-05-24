from recipes.models.tags import Tag
from rest_framework.validators import ValidationError as RFError


def validate_tags(data):
    if not data:
        raise RFError({'tags': ['Обязательное поле.']})
    if len(data) < 1:
        raise RFError({'tags': ['Хотя бы один тэг должен быть указан.']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise RFError({'tags': ['Тэг отсутствует в БД.']})
    return data
