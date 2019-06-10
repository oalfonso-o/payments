from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from payments.serializers import AccountSerializer
from payments.models import Account


class AccountViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
        ):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        try:
            account = Account.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Account not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(self.get_serializer(account).data)
