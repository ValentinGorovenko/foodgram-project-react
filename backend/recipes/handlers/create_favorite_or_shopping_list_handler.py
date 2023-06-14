from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def create_favorite_or_shopping_list(request, recipe_id, serializer_class):
    data = {
        'user': request.user.id,
        'recipe': recipe_id,
    }

    serializer = serializer_class(data=data)

    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
