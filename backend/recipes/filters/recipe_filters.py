from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter_by_user_relation(self, relation_name):
        def filter_fn(self, queryset, name, value):
            if value and self.request.user.is_authenticated:
                return queryset.filter(**{relation_name: self.request.user})
            return queryset

        return filter_fn

    def filter_is_favorited(self):
        return self.filter_by_user_relation('favorites__user')

    def filter_is_in_shopping_cart(self):
        return self.filter_by_user_relation(
            'shopping_list__user'
        )
