# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryVoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plugin_iden', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u63d2\u4ef6\u6807\u8bc6\u7b26')),
                ('fid', models.BigIntegerField(default=0, verbose_name='\u8fdc\u7a0b\u7d20\u6750\u5e93\u4e2d\u7684\u6587\u4ef6ID')),
                ('media_id', models.CharField(max_length=50, null=True, verbose_name='\u8bed\u97f3\u7684\u5a92\u4f53ID', blank=True)),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
                ('voice', models.ForeignKey(verbose_name=b'+', blank=True, to='media.Media', null=True)),
            ],
            options={
                'db_table': 'library_voice',
                'verbose_name': '\u7d20\u6750\u5e93 - \u8bed\u97f3\u5e93',
                'verbose_name_plural': '\u7d20\u6750\u5e93 - \u8bed\u97f3\u5e93',
            },
            bases=(models.Model,),
        ),
    ]
