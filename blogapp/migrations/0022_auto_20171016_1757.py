# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-16 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0021_aboutus_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='Title_EN',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='Title_HU',
            field=models.TextField(),
        ),
    ]