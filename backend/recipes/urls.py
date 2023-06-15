from django.urls import include, path
from rest_framework import routers

from recipes.views import (
    DownloadShoppingCartView,
    FavoriteRecipeView,
    IngredientView,
    RecipeDetailView,
    RecipeListView,
    ShoppingCartView,
    TagView,
)

app_name = 'recipes'

router = routers.DefaultRouter()
router.register(r'tags', TagView, basename='tags')
router.register(r'ingredients', IngredientView, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/',
        RecipeListView.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
    ),
    path(
        'recipes/<int:pk>/',
        RecipeDetailView.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
            }
        ),
    ),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view(
            {
                'get': 'list',
            }
        ),
    ),
    path(
        'recipes/<int:pk>/favorite/',
        FavoriteRecipeView.as_view(
            {
                'post': 'create',
                'delete': 'destroy',
            }
        ),
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShoppingCartView.as_view(
            {
                'post': 'create',
                'delete': 'destroy',
            }
        ),
    ),
]
