# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-28 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0018_auto_20170326_0024'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=300)),
                ('card_name', models.CharField(max_length=300)),
                ('thm', models.CharField(max_length=50)),
                ('info_block', models.TextField()),
                ('link', models.CharField(max_length=300)),
                ('card_image', models.ImageField(blank=True, upload_to='new')),
            ],
        ),
    ]