# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-09 19:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseevent',
            options={'ordering': ['datetime']},
        ),
    ]
