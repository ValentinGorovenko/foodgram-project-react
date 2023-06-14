from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import IngredientRecipe, Recipe, Tag
from recipes.serializers.ingredients_recipe_serializer import (
    IngredientRecipeSerializer,
)
from recipes.serializers.recipe_serializer import RecipeSerializer
from rest_framework import serializers
from recipes.constants import (
    REQUIRES_AT_LEAST_ONE_INGREDIENT,
    INGREDIENTS_SHOULD_NOT_BE_REPEATED,
    REQUIRES_AT_LEAST_ONE_TAG,
    TAGS_SHOULD_NOT_BE_REPEATED,
)


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(max_length=None)
    author = UserSerializer(read_only=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_at_least_one_ingridient(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                REQUIRES_AT_LEAST_ONE_INGREDIENT
            )

    def validate_at_least_one_tag(self, tags):
        if not tags:
            raise serializers.ValidationError(REQUIRES_AT_LEAST_ONE_TAG)

    def validate_unique_ingridient(self, ingredients):
        ingredient = [item['id'] for item in ingredients]
        if len(ingredient) != len(set(ingredient)):
            raise serializers.ValidationError(
                INGREDIENTS_SHOULD_NOT_BE_REPEATED
            )

    def validate_unique_tag(self, tags):
        print(tags)
        tags = [item for item in tags]
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                TAGS_SHOULD_NOT_BE_REPEATED
            )

    def validate_ingredients(self, ingredients):
        self.validate_at_least_one_ingridient(ingredients)
        self.validate_unique_ingridient(ingredients)
        return ingredients

    def validate_tags(self, tags):
        self.validate_at_least_one_tag(tags)
        self.validate_unique_tag(tags)
        return tags

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = self._create_recipe(validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def _create_recipe(self, validated_data):
        return Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance = super().update(instance, validated_data)

        if ingredients_data:
            instance.ingredients.clear()
            self.create_ingredients(ingredients_data, instance)

        if tags_data:
            instance.tags.set(tags_data)

        return instance

    def create_ingredients(self, ingredients_data, recipe):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    recipe=recipe,
                    ingredient_id=item['id'],
                    amount=item['amount'],
                )
                for item in reversed(ingredients_data)
            ]
        )

    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        ).data
