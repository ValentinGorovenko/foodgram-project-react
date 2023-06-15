from djoser.views import UserViewSet
from foodgram.paginations import LimitPagination

from users.models import User
from users.serializers import UserSerializer


class UserView(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPagination
