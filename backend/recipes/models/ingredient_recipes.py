from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .ingredients import Ingredient
from .recipes import Recipe
from recipes.constants import INGREDIENT_AMOUNT_MAX, INGREDIENT_AMOUNT_MIN


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
        related_name='ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(INGREDIENT_AMOUNT_MIN, message=None),
            MaxValueValidator(INGREDIENT_AMOUNT_MAX, message=None),
        ],
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
        ordering = ['recipe']

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'
