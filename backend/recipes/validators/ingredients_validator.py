from rest_framework import serializers

from recipes.constants import (
    INGREDIENT_AMOUNT_MAX,
    INGREDIENT_AMOUNT_MAX_ERROR,
    INGREDIENT_AMOUNT_MIN,
    INGREDIENT_AMOUNT_MIN_ERROR,
)


class IngredientsValidator:
    def _validate_amount_ingridient(self, ingredient):
        if int(ingredient['amount']) < INGREDIENT_AMOUNT_MIN:
            raise serializers.ValidationError(
                f'{INGREDIENT_AMOUNT_MIN_ERROR}'
            )
        if int(ingredient['amount']) > INGREDIENT_AMOUNT_MAX:
            raise serializers.ValidationError(
                f'{INGREDIENT_AMOUNT_MAX_ERROR}'
            )

    def __call__(self, ingredients):
        self._validate_amount_ingridient(ingredients)

        return ingredients
