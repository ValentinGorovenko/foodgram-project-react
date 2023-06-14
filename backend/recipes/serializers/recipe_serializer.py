from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from recipes.serializers.ingredients_recipe_serializer import (
    IngredientRecipeSerializer,
)
from recipes.serializers.tags_serializers import TagSerializer
from rest_framework import serializers
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=False, many=True)
    author = UserSerializer(read_only=True, many=False)
    image = Base64ImageField(max_length=None)
    ingredients = IngredientRecipeSerializer(many=True, source='recipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        is_anonymous = not request or request.user.is_anonymous
        return (
            not is_anonymous
            and obj.favorites.filter(user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        is_anonymous = not request or request.user.is_anonymous
        return (
            not is_anonymous
            and obj.shopping_list.filter(user=request.user).exists()
        )
