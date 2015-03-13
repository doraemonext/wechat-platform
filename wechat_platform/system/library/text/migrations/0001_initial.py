# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plugin_iden', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u63d2\u4ef6\u6807\u8bc6\u7b26')),
                ('content', models.TextField(verbose_name='\u6587\u5b57')),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
            ],
            options={
                'db_table': 'library_text',
                'verbose_name': '\u7d20\u6750\u5e93 - \u6587\u5b57\u8868',
                'verbose_name_plural': '\u7d20\u6750\u5e93 - \u6587\u5b57\u8868',
            },
            bases=(models.Model,),
        ),
    ]
