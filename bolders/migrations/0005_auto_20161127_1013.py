# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolders', '0004_auto_20161124_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='level',
        ),
        migrations.AddField(
            model_name='character',
            name='photo_full',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
