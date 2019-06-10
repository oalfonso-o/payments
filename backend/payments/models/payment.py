from model_utils.models import TimeStampedModel
from djmoney.models.fields import MoneyField

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models


class Payment(TimeStampedModel, models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        related_name='payments_sent',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        related_name='payments_received',
    )
    amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='EUR',
    )

    def __str__(self):
        return '{} paid {} to {}'.format(
            self.sender, self.amount, self.receiver,
        )

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError('Sender is the same as receiver')

    def save(self, *args, **kwargs):
        if not self.pk:
            self._transfer_money()
        super(Payment, self).save(*args, **kwargs)

    def _transfer_money(self):
        sender_account = self.sender.account
        receiver_account = self.receiver.account
        sender_account.balance -= self.amount
        receiver_account.balance += self.amount
        sender_account.save()
        receiver_account.save()
