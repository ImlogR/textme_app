# Generated by Django 4.0.3 on 2022-04-11 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goji', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 11, 21, 54, 2, 216052)),
        ),
    ]
