# Generated by Django 5.1.3 on 2025-01-02 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 1, 11, 31, 11, 50173)),
        ),
    ]
