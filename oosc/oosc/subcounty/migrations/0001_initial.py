# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-08 09:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('counties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='county_na', to='counties.Counties')),
            ],
        ),
    ]
