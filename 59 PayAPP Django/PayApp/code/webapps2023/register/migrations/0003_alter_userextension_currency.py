# Generated by Django 3.2.18 on 2023-05-11 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_alter_userextension_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextension',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euros'), ('GBP', 'GB Pound')], max_length=3),
        ),
    ]