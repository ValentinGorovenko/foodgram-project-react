from django.core.validators import MinValueValidator
from django.db import models

from .ingredients import Ingredient
from .recipes import Recipe


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Не может быть меньше 1')]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]
