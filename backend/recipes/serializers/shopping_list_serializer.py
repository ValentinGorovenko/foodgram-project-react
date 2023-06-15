from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.constants import SHOPPING_CART_VALIDATION_ERROR
from recipes.models import ShoppingList


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=['user', 'recipe'],
                message=SHOPPING_CART_VALIDATION_ERROR,
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
