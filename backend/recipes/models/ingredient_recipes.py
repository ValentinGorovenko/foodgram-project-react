from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from foodgram.settings import MAX_INGREDIENT_RECIPE, MIN_VALUE

from .ingredients import Ingredient
from .recipes import Recipe


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE, 'Не может быть меньше 1'),
            MaxValueValidator(
                MAX_INGREDIENT_RECIPE, 'Не может быть больше 32000'
            ),
        ],
        verbose_name='Количество ингредиента',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'
