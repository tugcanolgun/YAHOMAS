# Generated by Django 2.1.4 on 2018-12-09 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy', '0002_auto_20181208_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='name',
            field=models.CharField(default='a', max_length=30),
            preserve_default=False,
        ),
    ]
