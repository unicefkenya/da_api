# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-13 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0004_auto_20171113_1433'),
        ('schools', '0005_auto_20170928_1346'),
        ('promotions', '0002_auto_20171113_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='promoteschool',
            name='graduates_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stream.GraduatesStream'),
        ),
        migrations.AddField(
            model_name='promoteschool',
            name='promotions',
            field=models.ManyToManyField(to='promotions.PromoteStream'),
        ),
        migrations.AddField(
            model_name='promoteschool',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.Schools'),
        ),
        migrations.AlterUniqueTogether(
            name='promoteschool',
            unique_together=set([('school', 'year')]),
        ),
    ]