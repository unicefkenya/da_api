# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-11 09:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0004_auto_20170410_2048'),
        ('students', '0016_auto_20170411_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('joined', models.DateField()),
                ('joined_description', models.CharField(max_length=400)),
                ('left', models.DateField()),
                ('left_description', models.CharField(max_length=400)),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Classes')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Students')),
            ],
        ),
    ]