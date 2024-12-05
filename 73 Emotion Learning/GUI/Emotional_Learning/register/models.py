from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class EmotionHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    session_id = models.CharField(max_length=30, null=False, blank=False)
    dated_at = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    label = models.CharField(max_length=15)