# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 19:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='quantity',
            new_name='stock',
        ),
    ]
