# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-02-09 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0012_schools_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='year',
            field=models.IntegerField(default=2020),
        ),
    ]
