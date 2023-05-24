from recipes.models.ingredients import Ingredient
from rest_framework.validators import ValidationError as RFError


def validate_ingredients(data):
    if not data:
        raise RFError({'ingredients': ['Обязательное поле.']})
    if len(data) < 1:
        raise RFError({'ingredients': ['Не переданы ингредиенты.']})
    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get('id'):
            raise RFError({'ingredients': ['Отсутствует id ингредиента.']})
        id = ingredient.get('id')
        if not Ingredient.objects.filter(id=id).exists():
            raise RFError({'ingredients': ['Ингредиента нет в БД.']})
        if id in unique_ingredient:
            raise RFError(
                {'ingredients': ['Нельзя повторять имена ингредиентов.']}
            )
        unique_ingredient.append(id)
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise RFError({'amount': ['Количество не может быть менее 1.']})
    return data
