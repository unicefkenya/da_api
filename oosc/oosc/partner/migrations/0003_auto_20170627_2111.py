# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-27 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_partner_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=90, unique=True),
        ),
    ]
