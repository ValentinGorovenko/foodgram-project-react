from recipes.models.tags import Tag
from recipes.serializers import TagSerializer
from rest_framework import viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
