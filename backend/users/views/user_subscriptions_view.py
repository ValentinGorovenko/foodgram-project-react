from foodgram.paginations import LimitPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import User

from users.serializers import SubscriptionSerializer


class UserSubscriptionsView(viewsets.ModelViewSet):
    pagination_class = LimitPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        return queryset

    def list(self, request):
        limit = request.GET.get('recipes_limit')

        queryset = self.get_queryset()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request, 'limit': limit}
        )
        return self.get_paginated_response(serializer.data)
