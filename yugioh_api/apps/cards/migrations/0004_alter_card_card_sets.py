# Generated by Django 5.1.3 on 2024-12-31 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_card_card_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_sets',
            field=models.ManyToManyField(to='cards.cardset'),
        ),
    ]
