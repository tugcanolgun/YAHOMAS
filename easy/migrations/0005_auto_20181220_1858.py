# Generated by Django 2.1.4 on 2018-12-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy', '0004_roomcleaning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='room_number',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
