# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('iden', models.CharField(max_length=50, serialize=False, verbose_name='\u63d2\u4ef6\u6807\u8bc6\u7b26', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u63d2\u4ef6\u540d\u79f0')),
                ('description', models.TextField(null=True, verbose_name='\u63d2\u4ef6\u63cf\u8ff0', blank=True)),
                ('author', models.CharField(max_length=50, null=True, verbose_name='\u63d2\u4ef6\u4f5c\u8005', blank=True)),
                ('website', models.URLField(null=True, verbose_name='\u63d2\u4ef6\u4f5c\u8005\u7f51\u7ad9', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='\u63d2\u4ef6\u4f5c\u8005\u90ae\u7bb1', blank=True)),
                ('version', models.CharField(max_length=30, null=True, verbose_name='\u63d2\u4ef6\u7248\u672c', blank=True)),
                ('official_account', models.ManyToManyField(to='official_account.OfficialAccount', verbose_name='\u5f00\u542f\u8be5\u63d2\u4ef6\u7684\u516c\u4f17\u53f7\u96c6\u5408')),
            ],
            options={
                'db_table': 'wechat_plugin',
                'verbose_name': '\u63d2\u4ef6\u8868',
                'verbose_name_plural': '\u63d2\u4ef6\u8868',
            },
            bases=(models.Model,),
        ),
    ]
