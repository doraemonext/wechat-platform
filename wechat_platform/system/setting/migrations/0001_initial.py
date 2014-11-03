# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u9009\u9879\u540d\u79f0')),
                ('value', models.TextField(verbose_name='\u9009\u9879\u5185\u5bb9')),
            ],
            options={
                'db_table': 'setting',
                'verbose_name': '\u7cfb\u7edf\u8bbe\u7f6e',
                'verbose_name_plural': '\u7cfb\u7edf\u8bbe\u7f6e',
            },
            bases=(models.Model,),
        ),
    ]
