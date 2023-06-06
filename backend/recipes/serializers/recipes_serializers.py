from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from recipes.serializers import IngredientRecipeSerializer
from recipes.serializers.tags_serializers import TagSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from users.serializers import CustomUserSerializer


class MiniRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source='ingredientrecipe_set'
    )
    image = Base64ImageField()
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
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            return Favorite.objects.filter(
                user=request_user, recipe=obj.id
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=request_user, recipe=obj.id
            ).exists()
        return False

    def create_recipe_ingredients(self, ingredients, recipe):
        ingredient_models = []
        for ingredient in ingredients:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            ingredient_models.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient_model,
                    amount=ingredient['amount'],
                )
            )
        IngredientRecipe.objects.bulk_create(ingredient_models)

    def create_tags(self, data, recipe):
        tags_data = data.get('tags')
        if not tags_data or len(tags_data) < 1:
            raise ValidationError('tags Обязательное поле для заполнения.')
        if len(tags_data) != len(set(tags_data)):
            raise ValidationError('tag повторяется.')
        for tag in tags_data:
            if not Tag.objects.filter(id=tag).exists():
                raise ValidationError(
                    f'Tags {tag} отсутствуют в Базе Данных.'
                )
        tags = Tag.objects.filter(id__in=tags_data)
        recipe.tags.set(tags)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.create_recipe_ingredients(ingredients_data, recipe)
        self.create_tags(self.initial_data, recipe)
        return recipe

    def validate(self, data):
        ingredients_data = self.initial_data.get('ingredients')
        if not ingredients_data:
            raise ValidationError(
                'ingredients (ингредиенты) обязательное поле для заполнения.'
            )
        ingredient_unique = []
        for ingredient in ingredients_data:
            if 'id' not in ingredient:
                raise ValidationError('id обязательное поле для заполнения.')
            if 'amount' not in ingredient:
                raise ValidationError(
                    'amount (количество) обязательное поле для заполнения.'
                )
            if ingredient['id'] in ingredient_unique:
                raise ValidationError(
                    f'{ingredient} уже добавлен. Нельзя повторять ингредиенты.'
                )
            ingredient_unique.append(ingredient['id'])
            amount = int(ingredient.get('amount'))
            if amount <= 0:
                raise ValidationError('Количество не может быть меньше 1')
        data['ingredients'] = ingredients_data
        return data

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.cooking_time = validated_data.get(
    #         'cooking_time', instance.cooking_time
    #     )
    #     instance.save()
    #     instance.tags.remove()
    #     self.create_tags(self.initial_data, instance)
    #     instance.ingredientrecipe.filter(
    #         recipe__in=[instance.id]
    #     ).delete()
    #     valid_ingredients = validated_data.get(
    #         'ingredients', instance.ingredients
    #     )
    #     self.create_recipe_ingredients(valid_ingredients, instance)
    #     return instance

    def update(self, recipe, data):
        recipe.name = data.get('name', recipe.name)
        recipe.image = data.get('image', recipe.image)
        recipe.text = data.get('text', recipe.text)
        recipe.cooking_time = data.get('cooking_time', recipe.cooking_time)
        recipe.tags.clear()
        self.create_tags(self.initial_data, recipe)
        recipe.ingredients.clear()
        ingredient = data.get(
                'ingredients', recipe.ingredients
            )
        self.create_recipe_ingredients(ingredient, recipe)
        return recipe
