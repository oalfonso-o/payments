from djmoney.money import Money
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets

from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from payments.serializers import PaymentSerializer
from payments.serializers import PaymentSerializerFlatUsers
from payments.models import Payment


class PaymentViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
        ):

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentSerializer
        if self.action == 'create':
            return PaymentSerializerFlatUsers

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(Q(sender=user) | Q(receiver=user))

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            receiver_user = User.objects.get(pk=request.data['receiver'])
            if receiver_user == request.user:
                return self._same_sender_and_receiver_response()
        except ObjectDoesNotExist:
            return self._receiver_not_found_response()

        sender_account = request.user.account
        if self._enough_money(request.data['amount'], sender_account):
            self._set_request_user_as_sender(request)
            # Don't catch exceptions here, let atomic know it and rollback
            payment_response = super(
                PaymentViewSet, self).create(request, *args, **kwargs)
        else:
            payment_response = self._not_enough_money_response()

        return payment_response

    def _same_sender_and_receiver_response(self):
        return Response(
            {'error': 'Receiver user is the same as sender'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _receiver_not_found_response(self):
        return Response(
            {'error': 'Receiver user not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    def _enough_money(self, amount, sender_account):
        return sender_account.balance >= Money(amount, 'EUR')

    def _set_request_user_as_sender(self, request):
        request.data['sender'] = request.user.pk

    def _not_enough_money_response(self):
        return Response(
            {'error': 'You don\'t have enough money'},
            status=status.HTTP_400_BAD_REQUEST,
        )
