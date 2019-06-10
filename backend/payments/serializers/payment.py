from rest_framework import serializers

from payments.models import Payment
from .user import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):

    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Payment
        fields = ('sender', 'receiver', 'amount', 'created')


class PaymentSerializerFlatUsers(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('sender', 'receiver', 'amount', 'created')
