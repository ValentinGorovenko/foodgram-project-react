from rest_framework import viewsets

from recipes.models import Recipe
from recipes.permissions import AuthorPermission
from recipes.serializers import RecipeCreateSerializer, RecipeSerializer


class RecipeDetailView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorPermission,)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return self.serializer_class
