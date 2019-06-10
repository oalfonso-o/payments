from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from .account import Account


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
