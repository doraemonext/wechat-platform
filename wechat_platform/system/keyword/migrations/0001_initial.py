# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
        ('rule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u5b57')),
                ('status', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('type', models.IntegerField(default=0, verbose_name='\u5173\u952e\u5b57\u7c7b\u578b', choices=[(0, '\u5b8c\u5168\u5339\u914d'), (1, '\u5305\u542b\u5339\u914d'), (2, '\u6b63\u5219\u8868\u8fbe\u5f0f\u5339\u914d')])),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
                ('rule', models.ForeignKey(verbose_name='\u6240\u5c5e\u89c4\u5219', to='rule.Rule')),
            ],
            options={
                'db_table': 'wechat_keyword',
                'verbose_name': '\u5fae\u4fe1\u5173\u952e\u5b57\u8868',
                'verbose_name_plural': '\u5fae\u4fe1\u5173\u952e\u5b57\u8868',
            },
            bases=(models.Model,),
        ),
    ]
