# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 12:49
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20160409_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(help_text='Pick up a image file from your computer. Image should be big enough so that it wont get scaled up by the system.', upload_to='courses/', verbose_name='General image of the course'),
        ),
    ]
