# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u89c4\u5219\u540d\u79f0')),
                ('reply_pattern', models.IntegerField(default=1, verbose_name='\u56de\u590d\u65b9\u5f0f', choices=[(0, '\u5168\u90e8\u56de\u590d'), (1, '\u968f\u673a\u56de\u590d'), (2, '\u987a\u5e8f\u56de\u590d'), (3, '\u9006\u5e8f\u56de\u590d')])),
                ('status', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('top', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f6e\u9876')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='\u4f18\u5148\u7ea7')),
            ],
            options={
                'db_table': 'wechat_rule',
                'verbose_name': '\u5fae\u4fe1\u89c4\u5219\u8868',
                'verbose_name_plural': '\u5fae\u4fe1\u89c4\u5219\u8868',
            },
            bases=(models.Model,),
        ),
    ]
