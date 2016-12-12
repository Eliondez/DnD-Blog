# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(choices=[('no', 'None'), ('gp', 'GURPS'), ('d5e', 'DnD 5e')], default='None', max_length=5)),
                ('description', models.TextField()),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('ended', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]