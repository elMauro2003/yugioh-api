# Generated by Django 5.1.3 on 2024-12-31 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_rename_frame_type_card_frametype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
