# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-23 16:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_auto_20170223_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='CNY',
            new_name='UAH',
        ),
    ]