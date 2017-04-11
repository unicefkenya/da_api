# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-10 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0005_auto_20170122_1625'),
        ('classes', '0003_auto_20170118_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='teacher',
        ),
        migrations.AddField(
            model_name='classes',
            name='teacher',
            field=models.ManyToManyField(related_name='class_teacher', to='teachers.Teachers'),
        ),
    ]
