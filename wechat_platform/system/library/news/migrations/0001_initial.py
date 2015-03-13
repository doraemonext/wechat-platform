# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plugin_iden', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u63d2\u4ef6\u6807\u8bc6\u7b26')),
                ('title', models.CharField(max_length=100, verbose_name='\u672c\u5730/\u8fdc\u7a0b-\u56fe\u6587\u6807\u9898')),
                ('description', models.TextField(null=True, verbose_name='\u672c\u5730/\u8fdc\u7a0b-\u56fe\u6587\u63cf\u8ff0', blank=True)),
                ('picurl', models.CharField(max_length=1024, null=True, verbose_name='\u8fdc\u7a0b-\u7f29\u7565\u56fe\u56fe\u7247\u5730\u5740', blank=True)),
                ('url', models.CharField(max_length=1024, null=True, verbose_name='\u8fdc\u7a0b-\u8df3\u8f6c\u5730\u5740', blank=True)),
                ('msgid', models.BigIntegerField(default=0, verbose_name='\u672c\u5730-\u516c\u4f17\u5e73\u53f0\u56fe\u6587ID\u53f7')),
                ('author', models.CharField(max_length=100, null=True, verbose_name='\u672c\u5730-\u56fe\u6587\u4f5c\u8005', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u672c\u5730-\u56fe\u6587\u5185\u5bb9', blank=True)),
                ('picid', models.IntegerField(default=0, verbose_name='\u672c\u5730-\u7d20\u6750\u5e93\u4e2d\u7684\u56fe\u7247ID')),
                ('from_url', models.CharField(max_length=1024, null=True, verbose_name='\u672c\u5730-\u6765\u6e90URL', blank=True)),
                ('view_count', models.IntegerField(default=0, verbose_name='\u672c\u5730-\u56fe\u6587\u8bbf\u95ee\u6b21\u6570')),
                ('vote_count', models.IntegerField(default=0, verbose_name='\u672c\u5730-\u56fe\u6587\u70b9\u8d5e\u6570\u76ee')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u672c\u5730-\u56fe\u6587\u65b0\u5efa\u65e5\u671f')),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
                ('parent', models.ForeignKey(verbose_name='\u672c\u5730/\u8fdc\u7a0b-\u7236ID', blank=True, to='news.LibraryNews', null=True)),
                ('picture', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u672c\u5730/\u8fdc\u7a0b-\u56fe\u7247\u5b58\u50a8\u5730\u5740', blank=True, to='media.Media', null=True)),
            ],
            options={
                'db_table': 'library_news',
                'verbose_name': '\u7d20\u6750\u5e93 - \u56fe\u6587\u5e93',
                'verbose_name_plural': '\u7d20\u6750\u5e93 - \u56fe\u6587\u5e93',
            },
            bases=(models.Model,),
        ),
    ]
