from rest_framework.filters import SearchFilter

from recipes.models import Ingredient


class IngredientFilter(SearchFilter):
    search_param = 'name'
    queryset = Ingredient.objects.all()
    fields = ('name',)
