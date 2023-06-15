from django.db import models
from django.db.models import UniqueConstraint

from .recipes import Recipe
from users.models import User


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    is_favorite = models.BooleanField(default=True, verbose_name='Избранное')

    class Meta:
        default_related_name = 'favorites'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(app_label)s_%(class)s_unique',
            )
        ]
        ordering = ['user']

    def __str__(self):
        return f'{self.user} :: {self.recipe}'
