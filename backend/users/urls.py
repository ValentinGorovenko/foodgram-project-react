from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserSubscribeView, UserSubscriptionsView, UserView

app_name = 'users'

router = DefaultRouter()
router.register('users', UserView, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/', UserSubscriptionsView.as_view({'get': 'list'})
    ),
    path(
        'users/<int:id>/subscribe/',
        UserSubscribeView.as_view({'post': 'create', 'delete': 'destroy'}),
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
