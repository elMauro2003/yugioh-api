# Generated by Django 5.1.3 on 2024-12-31 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_card_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
