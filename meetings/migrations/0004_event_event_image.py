# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-05 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20170804_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
