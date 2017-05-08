# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-08 09:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_created=True)),
                ('student_id', models.IntegerField(blank=True, default=0, null=True)),
                ('emis_code', models.IntegerField(blank=True, default=0, null=True)),
                ('fstname', models.CharField(max_length=200)),
                ('midname', models.CharField(blank=True, max_length=200, null=True)),
                ('lstname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('admission_no', models.IntegerField(blank=True, default=0, null=True)),
                ('gender', models.CharField(choices=[(b'M', b'MALE'), (b'F', b'FEMALE')], default=b'ML', max_length=2)),
                ('previous_class', models.IntegerField(blank=True, default=0, null=True)),
                ('mode_of_transport', models.CharField(blank=True, max_length=200, null=True)),
                ('time_to_school', models.CharField(blank=True, default=0, max_length=50, null=True)),
                ('stay_with', models.CharField(blank=True, max_length=200, null=True)),
                ('household', models.IntegerField(blank=True, default=0, null=True)),
                ('meals_per_day', models.IntegerField(blank=True, default=0, null=True)),
                ('not_in_school_before', models.BooleanField(default=False)),
                ('emis_code_histories', models.CharField(blank=True, max_length=200, null=True)),
                ('total_attendance', models.IntegerField(blank=True, default=0, null=True)),
                ('total_absents', models.IntegerField(blank=True, default=0, null=True)),
                ('last_attendance', models.DateField(blank=True, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=50, null=True)),
                ('guardian_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.Stream')),
            ],
            options={
                'ordering': ['-gender'],
            },
        ),
    ]
