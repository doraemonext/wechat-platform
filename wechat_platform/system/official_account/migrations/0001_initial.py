# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iden', models.CharField(max_length=32, verbose_name='\u516c\u4f17\u53f7\u552f\u4e00\u6807\u8bc6')),
                ('token', models.CharField(max_length=300, verbose_name='\u5fae\u4fe1Token')),
                ('appid', models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1App ID', blank=True)),
                ('appsecret', models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1App Secret', blank=True)),
                ('username', models.CharField(max_length=255, null=True, verbose_name='\u516c\u4f17\u5e73\u53f0\u7528\u6237\u540d', blank=True)),
                ('password', models.CharField(max_length=255, null=True, verbose_name='\u516c\u4f17\u5e73\u53f0\u5bc6\u7801', blank=True)),
                ('is_advanced', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5f00\u542f\u9ad8\u7ea7\u652f\u6301')),
                ('level', models.IntegerField(verbose_name='\u516c\u4f17\u53f7\u7ea7\u522b', choices=[(1, '\u666e\u901a\u8ba2\u9605\u53f7'), (2, '\u8ba4\u8bc1\u8ba2\u9605\u53f7/\u666e\u901a\u670d\u52a1\u53f7'), (3, '\u8ba4\u8bc1\u670d\u52a1\u53f7')])),
                ('name', models.CharField(max_length=100, verbose_name='\u516c\u4f17\u53f7\u540d\u79f0')),
                ('email', models.EmailField(max_length=254, verbose_name='\u516c\u4f17\u53f7\u767b\u5f55\u90ae\u7bb1')),
                ('original', models.CharField(max_length=30, verbose_name='\u516c\u4f17\u53f7\u539f\u59cbID')),
                ('wechat', models.CharField(max_length=100, verbose_name='\u5fae\u4fe1\u53f7')),
                ('introduction', models.TextField(null=True, verbose_name='\u516c\u4f17\u53f7\u4ecb\u7ecd', blank=True)),
                ('address', models.TextField(null=True, verbose_name='\u6240\u5728\u5730\u5740', blank=True)),
                ('cache_access_token', models.CharField(max_length=512, null=True, verbose_name='\u7f13\u5b58access token', blank=True)),
                ('cache_access_token_expires_at', models.BigIntegerField(null=True, verbose_name='\u7f13\u5b58access token\u8fc7\u671f\u65f6\u95f4', blank=True)),
                ('cache_token', models.CharField(max_length=512, null=True, verbose_name='\u7f13\u5b58\u6a21\u62df\u767b\u9646token', blank=True)),
                ('cache_cookies', models.TextField(null=True, verbose_name='\u7f13\u5b58\u6a21\u62df\u767b\u9646cookies', blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'db_table': 'official_account',
            },
            bases=(models.Model,),
        ),
    ]
