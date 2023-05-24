from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = ColorField(format='hex')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Только латинские буквы и символы "-" "_"',
            ),
        ],
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
