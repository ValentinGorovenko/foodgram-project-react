from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import RecipeFilter
from recipes.models import Favorite, IngredientRecipe, Recipe, ShoppingCart
from recipes.permissions import AuthorOrReadOnly
from recipes.serializers import MiniRecipeSerializer, RecipeSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_recipe_to_model(self, model, user, pk, name):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'error': f'Рецепт в {name} уже добавлен.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            model.objects.create(user=user, recipe=recipe)
            serialized_recipe = MiniRecipeSerializer(recipe)
            return Response(
                serialized_recipe.data, status=status.HTTP_201_CREATED
            )

    def delete_relation(self, model, user, pk, name):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'errors': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {'errors': f'В {name} рецепт не найден.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
    )
    def favorite(self, request, pk=None):
        return self.handle_relation_request(
            request, Favorite, pk, 'избранное'
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        return self.handle_relation_request(
            request, ShoppingCart, pk, 'список покупок'
        )

    def handle_relation_request(self, request, model, pk, name):
        user = request.user
        if request.method == 'POST':
            return self.add_recipe_to_model(model, user, pk, name)
        elif request.method == 'DELETE':
            return self.delete_relation(model, user, pk, name)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['GET'],
        url_name='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(ingredient_total_amount=Sum('amount'))
        )
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_total_amount']
            shopping_list.append(f'{name}: {amount} {measurement_unit}')
        content = '\n'.join(shopping_list)
        response = HttpResponse(
            content, content_type='text/plain,charset=utf8'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping-list.txt"'
        return response
