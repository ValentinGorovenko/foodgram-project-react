from django.db.models import Sum
from django.http.response import HttpResponse
from rest_framework import viewsets

from recipes.models import IngredientRecipe
from recipes.permissions import AuthorPermission


class DownloadShoppingCartView(viewsets.ModelViewSet):
    permission_classes = (AuthorPermission,)

    def download_shopping_cart_helper(self, user):
        return (
            IngredientRecipe.objects.filter(recipe__shopping_list__user=user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
        )

    def shopping_list(self, ingredients):
        header = 'Foodgram. Список покупок:'
        formatted_ingredients = [
            f"{ingredient['ingredient__name']} - "
            f"{ingredient['total_amount']}"
            f"{ingredient['ingredient__measurement_unit']}"
            for ingredient in ingredients
        ]
        shopping_list = [header] + formatted_ingredients
        response = HttpResponse(
            '\n'.join(shopping_list), content_type='text/plain'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_list.txt"'
        return response

    def list(self, request):
        ingredients = self.download_shopping_cart_helper(request.user)
        return self.shopping_list(ingredients)
