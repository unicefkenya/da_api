# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0012_auto_20170421_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]