# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 13:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0009_teachers_headteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='school',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='schools.Schools'),
            preserve_default=False,
        ),
    ]