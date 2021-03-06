# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-07 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0021_auto_20160802_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='billcommittee',
            name='chairman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chairman', to='legco.Individual'),
        ),
        migrations.AddField(
            model_name='billcommittee',
            name='individuals',
            field=models.ManyToManyField(related_name='individuals', to='legco.Individual'),
        ),
    ]
