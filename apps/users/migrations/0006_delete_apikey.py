# Generated by Django 5.1.3 on 2025-01-03 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_apikey_expires_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='APIKey',
        ),
    ]