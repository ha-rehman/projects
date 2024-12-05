from django.contrib.auth.models import User
from django.db import models
from register.models import UserExtension


# Create your models here.
class TransactionHistory(models.Model):
    transfer = "trans"
    request = "req"
    completed = 'complete'
    pending = 'pending'
    rejected = 'rejected'

    mode_choices = [
        (transfer, 'Transfer'),
        (request, 'Request'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField(blank=False, null=False)
    currency = models.CharField(max_length=3, null=False, blank=False, choices=UserExtension.currency_choices)
    mode = models.CharField(max_length=10, choices=mode_choices)
    dated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='completed')
