from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import SubscriptionSerializer

from .models.subscription import Subscription
from .models.user import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def subscriptions(self, request):
        user = request.user
        subscriptions = user.follower.all()
        paginated_subscriptions = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            paginated_subscriptions, many=True, context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
    )
    def subscribe(self, request, id=None):
        user = request.user
        try:
            author = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {'errors': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user == author:
            return Response(
                {'errors': 'Нельзя на себя подписаться / отписаться.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = Subscription.objects.filter(
            author=author, user=user
        ).first()
        if request.method == 'POST':
            if subscription:
                return Response(
                    {'errors': 'Повторно подписаться нельзя.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription = Subscription.objects.create(
                author=author, user=user
            )
            serializer = SubscriptionSerializer(
                subscription, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not subscription:
                return Response(
                    {'errors': 'Повторно отписаться нельзя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'Данный метод не поддерживается'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
