from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = filters.CharFilter(
        field_name='author__username', lookup_expr='iexact'
    )
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='shopping_cart_filter')

    def favorited_filter(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        else:
            return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        else:
            return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
