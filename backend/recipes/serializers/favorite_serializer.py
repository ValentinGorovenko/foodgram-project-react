from recipes.models import Favorite
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.constants import FAVORITE_VALIDATION_ERROR


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message=FAVORITE_VALIDATION_ERROR,
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return {
            'id': recipe.id,
            'name': recipe.name,
            'image': recipe.image.url if recipe.image else None,
            'cooking_time': recipe.cooking_time,
        }
