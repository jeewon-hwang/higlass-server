# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coolers', '0004_auto_20161019_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='cooler',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cooler',
            name='processed_file',
            field=models.TextField(default=''),
        ),
    ]
