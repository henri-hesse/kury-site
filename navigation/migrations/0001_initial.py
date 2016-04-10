# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Title will be shown on the navigation menu.', max_length=200)),
                ('link_type', models.CharField(blank=True, max_length=200, null=True, help_text=b'Where should the user be taken when this item is clicked?', choices=[(b'page', b'Page'), (b'tailored_page', b'Tailored page'), (b'url', b'External URL')])),
                ('tailored_page', models.CharField(blank=True, max_length=200, null=True, help_text=b'Select the page that this item links to.', choices=[(b'http://example.com/', b'Example page')])),
                ('url', models.URLField(help_text=b'URL address that this item links to, like "http://example.com/".', null=True, verbose_name=b'URL', blank=True)),
                ('order_number', models.IntegerField()),
                ('deepness', models.IntegerField()),
                ('page', models.ForeignKey(blank=True, to='pages.Page', help_text=b'Select the page that this item links to.', null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='navigation.Item', help_text=b'This item will be nested inside of the parent item.', null=True, verbose_name=b'Parent navigation item')),
            ],
            options={
                'ordering': ['order_number'],
            },
        ),
    ]
