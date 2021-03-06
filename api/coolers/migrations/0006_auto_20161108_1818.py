# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('coolers', '0005_auto_20161020_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooler',
            name='highlighted',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='processed',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='public',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='published',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='rawfile_in_db',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='title',
        ),
        migrations.RemoveField(
            model_name='cooler',
            name='url',
        ),
        migrations.AddField(
            model_name='cooler',
            name='twod',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cooler',
            name='uuid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='cooler',
            name='processed_file',
            field=models.TextField(),
        ),
    ]
