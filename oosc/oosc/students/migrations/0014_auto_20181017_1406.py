# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-17 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_students_dropout_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='admission_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
