# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-13 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]