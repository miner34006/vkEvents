# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-27 11:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20170827_1051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choiceList_whoChoosen',
            new_name='choiceList_whoChosen',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='choiceList_whomChoosen',
            new_name='choiceList_whomChosen',
        ),
    ]
