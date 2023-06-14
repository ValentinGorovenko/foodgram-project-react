from django_filters.rest_framework import DjangoFilterBackend
from foodgram.paginations import LimitPagination
from recipes.filters import RecipeFilter
from recipes.models import Recipe
from recipes.permissions import AuthorPermission
from recipes.serializers import (
    RecipeCreateSerializer,
    RecipeSerializer,
)
from rest_framework import viewsets
from rest_framework.response import Response


class RecipeListView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorPermission,)
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def create(self, request):
        serializer = RecipeCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
