# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-15 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20170822_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='class_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='stream.Stream'),
        ),
    ]