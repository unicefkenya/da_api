# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 20:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_auto_20161025_2253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schools',
            old_name='cons_name',
            new_name='constituency',
        ),
    ]
