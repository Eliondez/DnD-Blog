# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 07:52
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('campaign', '0002_auto_20161220_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-ingamedate', '-posted']},
        ),
        migrations.AddField(
            model_name='story',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='rp_system',
            field=models.CharField(default='Нет', max_length=50, verbose_name='Система'),
        ),
        migrations.AlterField(
            model_name='story',
            name='content',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='story',
            name='ingamedate',
            field=models.DateField(verbose_name='Внутриигровая дата'),
        ),
        migrations.AlterField(
            model_name='story',
            name='posted',
            field=models.DateTimeField(auto_now_add=True, help_text='Формат ГГГГ-ММ-ДД', null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
