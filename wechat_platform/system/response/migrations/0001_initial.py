# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msgid', models.CharField(max_length=50, verbose_name='MsgID\u6216FromUserName+CreateTime')),
                ('target', models.CharField(max_length=50, verbose_name='\u76ee\u6807\u7528\u6237OpenID')),
                ('source', models.CharField(max_length=50, verbose_name='\u6765\u6e90\u7528\u6237OpenID')),
                ('time', models.IntegerField(verbose_name='\u4fe1\u606f\u53d1\u9001\u65f6\u95f4')),
                ('type', models.CharField(max_length=15, verbose_name='\u4fe1\u606f\u7c7b\u578b', choices=[(b'text', '\u6587\u672c\u6d88\u606f'), (b'image', '\u56fe\u7247\u6d88\u606f'), (b'video', '\u89c6\u9891\u6d88\u606f'), (b'voice', '\u8bed\u97f3\u6d88\u606f'), (b'news', '\u56fe\u6587\u6d88\u606f'), (b'music', '\u97f3\u4e50\u6d88\u606f'), (b'waiting', '\u6267\u884c\u4e2d\u6d88\u606f')])),
                ('pattern', models.IntegerField(verbose_name='\u54cd\u5e94\u65b9\u5f0f', choices=[(0, '\u6b63\u5e38XML\u8fd4\u56de\u6a21\u5f0f'), (1, '\u591a\u5ba2\u670d\u8fd4\u56de\u6a21\u5f0f'), (2, '\u6a21\u62df\u767b\u9646\u8fd4\u56de\u6a21\u5f0f'), (3, '\u6267\u884c\u4e2d\u6d88\u606f')])),
                ('raw', models.TextField(verbose_name='\u54cd\u5e94\u4fe1\u606f\u539f\u59cb\u5185\u5bb9')),
                ('plugin_iden', models.CharField(max_length=50, null=True, verbose_name='\u63d2\u4ef6\u6807\u8bc6\u7b26', blank=True)),
                ('reply_id', models.IntegerField(null=True, verbose_name='\u63d2\u4ef6\u56de\u590dID', blank=True)),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
            ],
            options={
                'db_table': 'response',
                'verbose_name': '\u5fae\u4fe1\u670d\u52a1\u5668\u54cd\u5e94\u4fe1\u606f',
                'verbose_name_plural': '\u5fae\u4fe1\u670d\u52a1\u5668\u54cd\u5e94\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
    ]
