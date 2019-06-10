from djmoney.models.fields import MoneyField

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    class Meta:
        verbose_name = 'Account'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='account')
    balance = MoneyField(
        max_digits=18,
        decimal_places=2,
        default_currency='EUR',
        default=100,  # Free initial money for test purposes
    )

    def __str__(self):
        return 'Account of {}'.format(self.user)
