# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-11 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_auto_20170109_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='ended',
            field=models.DateField(blank=True, null=True, verbose_name='Последняя история'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='started',
            field=models.DateField(auto_now_add=True, verbose_name='Дата начала'),
        ),
    ]
