# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-31 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_schools_subcounty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schools',
            name='emis_code',
            field=models.BigIntegerField(default=199, unique=True),
            preserve_default=False,
        ),
    ]