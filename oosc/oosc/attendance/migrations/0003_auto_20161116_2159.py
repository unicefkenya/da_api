# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-16 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20161116_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.IntegerField(choices=[(1, 'Present'), (0, 'Absent')], default=0, max_length=10),
        ),
    ]
