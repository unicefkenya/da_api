# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-29 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_auto_20170928_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schools',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zone.Zone'),
        ),
    ]
