# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u6587\u5b57')),
            ],
            options={
                'db_table': 'library_text',
                'verbose_name': '\u7d20\u6750\u5e93 - \u6587\u5b57\u8868',
                'verbose_name_plural': '\u7d20\u6750\u5e93 - \u6587\u5b57\u8868',
            },
            bases=(models.Model,),
        ),
    ]
