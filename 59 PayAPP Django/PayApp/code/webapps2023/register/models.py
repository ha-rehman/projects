from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserExtension(models.Model):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

    currency_choices = [
        (USD, 'US Dollar'),
        (EUR, 'Euros'),
        (GBP, 'GB Pound')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=15, blank=False, null=False)
    l_name = models.CharField(max_length=20, blank=False, null=False)
    currency = models.CharField(max_length=3, null=False, blank=False, choices=currency_choices)
    balance = models.FloatField(default=1000, blank=False, null=False)
