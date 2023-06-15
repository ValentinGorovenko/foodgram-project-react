from rest_framework import status
from rest_framework.response import Response


def create_favorite_or_shopping_list(request, recipe_id, serializer_class):
    data = {
        'user': request.user.id,
        'recipe': recipe_id,
    }

    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
