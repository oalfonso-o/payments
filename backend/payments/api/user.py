from rest_framework import mixins
from rest_framework import viewsets

from django.contrib.auth.models import User

from payments.serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.exclude(pk=user.pk)
