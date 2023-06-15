from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Subscription, User
from users.serializers import SubscriptionSerializer


class UserSubscribeView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        serializer = SubscriptionSerializer(
            author,
            data=request.data,
            context={'request': request, 'author_id': author.id},
        )
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        get_object_or_404(Subscription, user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
