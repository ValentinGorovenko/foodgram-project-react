from recipes.serializers import MiniRecipeSerializer
from rest_framework import serializers
from users.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and Subscription.objects.filter(
                author=obj.author, user=user
            ).exists()
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        author_recipes = obj.author.recipes.all()
        if limit:
            author_recipes = author_recipes[: int(limit)]
        return MiniRecipeSerializer(author_recipes, many=True).data
