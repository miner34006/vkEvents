# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-09 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20170808_0231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['event_id']},
        ),
    ]