# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-22 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0006_auto_20170122_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schools',
            name='school_code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]