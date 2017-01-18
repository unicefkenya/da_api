# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-16 06:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_class', to='classes.Classes')),
                ('prev_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_class', to='classes.Classes')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Students')),
            ],
        ),
    ]