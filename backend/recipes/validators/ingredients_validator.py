from rest_framework import serializers
from recipes.constants import (
    INGREDIENT_AMOUNT_MIN_ERROR,
    INGREDIENT_AMOUNT_MIN,
)


class IngredientsValidator:
    def _validate_amount_ingridient(self, ingredient):
        if int(ingredient['amount']) < INGREDIENT_AMOUNT_MIN:
            raise serializers.ValidationError(
                f'{INGREDIENT_AMOUNT_MIN_ERROR}'
            )

    def __call__(self, ingredients):
        self._validate_amount_ingridient(ingredients)

        return ingredients
