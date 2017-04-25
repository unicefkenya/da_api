# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-25 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.Schools')),
                ('teachers', models.ManyToManyField(related_name='class_teachers', to='teachers.Teachers')),
            ],
        ),
    ]