from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingList,
    Tag,
)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('name', 'author')
    inlines = (IngredientInline,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author', 'tags')


class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug')
    list_filter = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')


class FavoriteShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteShoppingListAdmin)
admin.site.register(ShoppingList, FavoriteShoppingListAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
