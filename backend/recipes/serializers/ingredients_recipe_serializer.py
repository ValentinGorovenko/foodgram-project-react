from rest_framework import serializers

from recipes.models import Ingredient
from recipes.validators import IngredientsValidator


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source="ingredient.name")
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount', 'name')
        validators = [IngredientsValidator()]
