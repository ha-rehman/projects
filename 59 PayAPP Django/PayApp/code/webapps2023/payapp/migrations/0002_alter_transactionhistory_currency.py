# Generated by Django 3.2.18 on 2023-05-05 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euros'), ('GPB', 'GB Pound')], max_length=3),
        ),
    ]