# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_remove_teachers_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='non_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='gender',
            field=models.CharField(choices=[(b'M', b'MALE'), (b'F', b'FEMALE')], default=b'M', max_length=2),
        ),
    ]
