# Generated by Django 3.2.18 on 2023-05-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextension',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euros'), ('GPB', 'GB Pound')], max_length=3),
        ),
    ]
