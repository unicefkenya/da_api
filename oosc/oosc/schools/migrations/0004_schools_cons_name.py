# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constituencies', '0002_auto_20161025_2239'),
        ('schools', '0003_remove_schools_cons_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='cons_name',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='constituencies.Constituencies'),
            preserve_default=False,
        ),
    ]