# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0002_auto_20160629_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=512)),
                ('name_ch', models.CharField(max_length=512)),
            ],
        ),
    ]
