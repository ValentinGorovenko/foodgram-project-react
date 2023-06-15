from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.handlers import create_favorite_or_shopping_list
from recipes.models import Favorite, Recipe
from recipes.serializers import FavoriteSerializer


class FavoriteRecipeView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        return create_favorite_or_shopping_list(
            request, recipe.id, FavoriteSerializer
        )

    def destroy(self, request, pk=None):
        model_instance = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=pk,
        )
        model_instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
