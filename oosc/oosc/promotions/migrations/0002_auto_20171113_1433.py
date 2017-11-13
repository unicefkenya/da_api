# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-13 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0003_auto_20170928_1346'),
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoteSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('year', models.PositiveSmallIntegerField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PromoteStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('next_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_class', to='stream.Stream')),
                ('prev_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prev_class', to='stream.Stream')),
            ],
        ),
        migrations.AlterField(
            model_name='promotions',
            name='next_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nexti_class', to='stream.Stream'),
        ),
    ]
