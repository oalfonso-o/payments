from django.contrib import admin

from payments.admin import payment
from payments.admin import account
from payments import models

admin.site.register(models.Payment, payment.PaymentAdmin)
admin.site.register(models.Account, account.AccountAdmin)
