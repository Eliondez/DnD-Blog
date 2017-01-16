# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_auto_20170111_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('img_width', models.IntegerField()),
                ('img_height', models.IntegerField()),
                ('file', models.ImageField(blank=True, height_field=models.IntegerField(), upload_to='maps/', width_field=models.IntegerField())),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
            ],
        ),
    ]