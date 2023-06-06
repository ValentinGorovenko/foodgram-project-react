from recipes.models.ingredients import Ingredient
from recipes.serializers import IngredientSerializer
from rest_framework import viewsets, filters


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
