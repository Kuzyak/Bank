# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-28 11:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0024_remove_iconame_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iconame',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
