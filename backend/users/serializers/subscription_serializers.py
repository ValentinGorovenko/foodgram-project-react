from rest_framework.exceptions import ValidationError

from rest_framework.fields import SerializerMethodField
from rest_framework import status

from .users_serializers import UserSerializer
from recipes.serializers import RecipeMiniFieldsSerializer
from users.constants import (
    YOU_ARE_ALREADY_SUBSCRIBED,
    YOU_CAN_NOT_SUBSCRIBE_TO_YOURSELF,
)


class SubscriptionSerializer(UserSerializer):

    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        limit = self.context.get('limit')

        recipes = obj.recipes.all()

        if limit:
            recipes = recipes[: int(limit)]

        return RecipeMiniFieldsSerializer(
            recipes, many=True, read_only=True
        ).data

    def validate(self, data):
        user = self.context.get('request').user
        author_id = self.context.get('author_id')
        if user.follower.filter(author=author_id).exists():
            raise ValidationError(
                {YOU_ARE_ALREADY_SUBSCRIBED}, status.HTTP_400_BAD_REQUEST
            )

        if user.id == author_id:
            raise ValidationError(
                {YOU_CAN_NOT_SUBSCRIBE_TO_YOURSELF},
                status.HTTP_400_BAD_REQUEST,
            )

        return data
