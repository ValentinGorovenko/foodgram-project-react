from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response
from recipes.constants import RECIPE_WITH_GIVEN_IDENTIFIER_DOES_NOT_EXIST


def get_recipe_by_pk_or_404(
    pk,
):
    try:
        data = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        return Response(
            {'error': RECIPE_WITH_GIVEN_IDENTIFIER_DOES_NOT_EXIST},
            status=status.HTTP_404_NOT_FOUND,
        )

    return data
