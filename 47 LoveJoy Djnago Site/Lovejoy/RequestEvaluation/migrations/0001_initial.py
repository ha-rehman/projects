# Generated by Django 3.2.16 on 2022-12-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('contact_via', models.CharField(max_length=80)),
                ('image', models.ImageField(upload_to='images/Evaluation_Pics')),
            ],
        ),
    ]
