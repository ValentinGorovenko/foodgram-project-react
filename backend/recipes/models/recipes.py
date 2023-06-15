from django.core.validators import MinValueValidator
from django.db import models

from .ingredients import Ingredient
from .tags import Tag
from users.models import User


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список id тегов',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка, закодированная в Base64',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления (в минутах)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
