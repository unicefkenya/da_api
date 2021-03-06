# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-08 09:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_code', models.IntegerField(blank=True, default=0, null=True)),
                ('school_name', models.CharField(max_length=200)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('emis_code', models.IntegerField(blank=True, default=0, null=True)),
                ('source_of_water', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_no', models.IntegerField(default=0)),
                ('level', models.CharField(choices=[(b'PRIMARY', b'Primary'), (b'SECONDARY', b'Secondary')], default=b'PRIMARY', max_length=50)),
                ('status', models.CharField(choices=[(b'PUBLIC', b'Public'), (b'PRIVATE', b'Private')], default=b'PUBLIC', max_length=50)),
                ('headteacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headteacher', to=settings.AUTH_USER_MODEL)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zone.Zone')),
            ],
        ),
    ]
