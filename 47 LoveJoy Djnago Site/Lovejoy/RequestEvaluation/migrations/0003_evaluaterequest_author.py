# Generated by Django 3.2.16 on 2022-12-20 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RequestEvaluation', '0002_rename_employee_evaluaterequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluaterequest',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
