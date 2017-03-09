# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spectator', '0006_auto_20170307_1625'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ('sort_title',)},
        ),
        migrations.AlterModelOptions(
            name='reading',
            options={},
        ),
        migrations.AddField(
            model_name='publication',
            name='sort_title',
            field=models.CharField(blank=True, help_text="e.g. 'Clockwork Orange, A' or 'World Cities, The'. If left blank, will be created automatically on save.", max_length=255),
        ),
    ]
