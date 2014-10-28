# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuleResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plugin_iden', models.CharField(max_length=50, verbose_name='\u54cd\u5e94\u63d2\u4ef6\u6807\u8bc6\u7b26')),
                ('reply_id', models.PositiveIntegerField(default=0, verbose_name='\u54cd\u5e94ID\u53f7')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='\u4f18\u5148\u7ea7')),
                ('status', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('rule', models.ForeignKey(verbose_name='\u6240\u5c5e\u89c4\u5219', to='rule.Rule')),
            ],
            options={
                'db_table': 'wechat_rule_response',
                'verbose_name': '\u5fae\u4fe1\u89c4\u5219\u56de\u590d\u8868',
                'verbose_name_plural': '\u5fae\u4fe1\u89c4\u5219\u56de\u590d\u8868',
            },
            bases=(models.Model,),
        ),
    ]
