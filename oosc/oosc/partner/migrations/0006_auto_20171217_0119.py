# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-16 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_partneradmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partneradmin',
            name='partners',
            field=models.ManyToManyField(blank=True, null=True, related_name='partner_admins', to='partner.Partner'),
        ),
    ]