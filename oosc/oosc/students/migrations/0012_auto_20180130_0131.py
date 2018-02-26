# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-29 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_students_offline_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='mode_of_transport',
            field=models.CharField(choices=[(b'PERSONAL', b'Personal Vehicle'), (b'BUS', b'School Bus'), (b'FOOT', b'By Foot'), (b'NS', b'Not Set')], default=b'NS', max_length=20),
        ),
        migrations.AlterField(
            model_name='students',
            name='stay_with',
            field=models.CharField(choices=[(b'P', b'Parents'), (b'G', b'Gurdians'), (b'A', b'Alone'), (b'NS', b'Not Set')], default=b'NS', max_length=20),
        ),
        migrations.AlterField(
            model_name='students',
            name='time_to_school',
            field=models.CharField(choices=[(b'1HR', b'One Hour'), (b'-0.5HR', b'Less than 1/2 Hour'), (b'+1HR', b'More than one hour.'), (b'NS', b'Not Set')], default=b'NS', max_length=50),
        ),
    ]