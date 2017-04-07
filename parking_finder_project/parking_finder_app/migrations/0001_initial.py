# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('booked_till', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]