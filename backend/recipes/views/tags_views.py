from rest_framework import viewsets

from recipes.models.tags import Tag
from recipes.serializers import TagSerializer


class TagView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
