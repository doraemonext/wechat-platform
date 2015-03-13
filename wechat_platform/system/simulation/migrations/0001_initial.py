# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulationMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=50, verbose_name='\u7528\u6237OpenID')),
                ('fakeid', models.CharField(max_length=50, verbose_name='\u7528\u6237FakeID')),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
            ],
            options={
                'db_table': 'simulation_match',
                'verbose_name': '\u6a21\u62df\u767b\u9646\u5173\u7cfb\u5bf9\u5e94\u8868',
                'verbose_name_plural': '\u6a21\u62df\u767b\u9646\u5173\u7cfb\u5bf9\u5e94\u8868',
            },
            bases=(models.Model,),
        ),
    ]
