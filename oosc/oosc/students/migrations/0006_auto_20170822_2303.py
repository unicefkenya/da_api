# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-22 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20170822_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='stream.Stream'),
        ),
    ]