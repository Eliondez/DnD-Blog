# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название кампании')),
                ('rp_system', models.CharField(choices=[('no', 'None'), ('gp', 'GURPS'), ('d5e', 'DnD 5e')], default='no', max_length=5, verbose_name='Система')),
                ('description', models.TextField(verbose_name='Описание кампании')),
                ('started', models.DateField(blank=True, null=True, verbose_name='Дата начала')),
                ('ended', models.DateField(blank=True, null=True, verbose_name='Дата окончания')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('ingamedate', models.CharField(max_length=100)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
