from django.shortcuts import get_object_or_404
from recipes.models import ShoppingList
from recipes.serializers import ShoppingListSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.handlers import get_recipe_by_pk_or_404
from recipes.handlers import create_favorite_or_shopping_list


class ShoppingCartView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, pk=None):
        recipe = get_recipe_by_pk_or_404(pk)
        return create_favorite_or_shopping_list(
            request, recipe.id, ShoppingListSerializer
        )

    def destroy(self, request, pk=None):
        model_instance = get_object_or_404(
            ShoppingList,
            user=request.user,
            recipe=pk,
        )
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
