from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

from .payment import PaymentViewSet
from .user import UserViewSet
from .account import AccountViewSet

api_router = DefaultRouter()

api_router.register(
    'payments', PaymentViewSet, base_name='payments',
)
api_router.register(
    'users', UserViewSet, base_name='users',
)
api_router.register(
    'account', AccountViewSet, base_name='account',
)

api_urls = [
    url(r'^api/login\/?$', obtain_auth_token),
    url(
        r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^api/', include(api_router.urls)),
]
