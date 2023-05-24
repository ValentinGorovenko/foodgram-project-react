from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

from .ingredients import Ingredient
from .tags import Tag


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
