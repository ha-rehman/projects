# Generated by Django 4.2.4 on 2023-09-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emotionhistory",
            name="dated_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]